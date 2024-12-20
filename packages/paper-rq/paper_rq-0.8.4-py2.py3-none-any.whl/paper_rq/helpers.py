import datetime

from django_rq import get_queue, get_scheduler
from django_rq.jobs import get_job_class
from django_rq.queues import get_queue_by_index, get_redis_connection
from django_rq.settings import QUEUES_LIST
from rq.command import send_stop_job_command
from rq.exceptions import NoSuchJobError
from rq.job import Job, JobStatus
from rq.utils import get_version, utcnow
from rq.worker import Worker

from .exceptions import UnsupportedJobStatusError

try:
    import rq_scheduler  # noqa
    RQ_SHEDULER_SUPPORTED = True
except ImportError:
    RQ_SHEDULER_SUPPORTED = False


def format_datetime(value):
    if isinstance(value, datetime.datetime):
        return value.replace(tzinfo=datetime.timezone.utc)
    return value


def supports_redis_streams(connection):
    return get_version(connection) >= (5, 0, 0)


def hashable_dict(dict_value):
    return ",".join(":".join(map(str, pair)) for pair in sorted(dict_value.items()))


def get_all_queues():
    for index, config in enumerate(QUEUES_LIST):
        yield get_queue_by_index(index)


def get_all_connections():
    seen_connections = set()
    for index, config in enumerate(QUEUES_LIST):
        connection = get_redis_connection(config['connection_config'])
        connection_params = hashable_dict(connection.connection_pool.connection_kwargs)
        if connection_params not in seen_connections:
            seen_connections.add(connection_params)
            yield connection


def get_all_workers():
    for connection in get_all_connections():
        yield from Worker.all(connection=connection)


def get_scheduled_jobs():
    """
    Получение задач из rq-scheduler.
    """
    if not RQ_SHEDULER_SUPPORTED:
        return

    for queue in get_all_queues():
        scheduler = get_scheduler(name=queue.name, queue=queue)
        for job in scheduler.get_jobs():
            if job.origin != queue.name:
                continue

            # Избавляемся от дублирования задачи в админке
            if (
                (job in queue.started_job_registry) or
                (job in queue.finished_job_registry) or
                (job in queue.failed_job_registry)
            ):
                continue

            yield job


def get_all_jobs():
    """
    Возвращает все задачи из всех реестров, а также из планировщика задач.
    """
    yield from get_scheduled_jobs()

    for queue in get_all_queues():
        job_ids = queue.get_job_ids()
        for job in queue.job_class.fetch_many(job_ids, connection=queue.connection):
            if job is not None:
                yield job

        registries = [
            queue.started_job_registry,
            queue.deferred_job_registry,
            queue.scheduled_job_registry,
            queue.finished_job_registry,
            queue.failed_job_registry,
            queue.canceled_job_registry,
        ]

        for registry in registries:
            job_ids = registry.get_job_ids()
            for job in registry.job_class.fetch_many(job_ids, connection=registry.connection):
                if job is not None:
                    yield job


def get_job(job_id, job_class=None):
    """
    Получение задачи по ID.

    Может найти задачу, которая удалена из очереди (например, вследствие вывова
    метода `cancel()`).
    """
    job_class = get_job_class(job_class)
    for connection in get_all_connections():
        try:
            return job_class.fetch(job_id, connection=connection)
        except NoSuchJobError:
            pass


def get_job_scheduler(job: Job):
    """
    Пытается найти планировщик для указанной задачи.
    """
    if not RQ_SHEDULER_SUPPORTED:
        return

    scheduler = get_scheduler(job.origin)
    if job in scheduler:
        return scheduler


def get_job_func_repr(job: Job) -> str:
    """
    Возвращает путь и аргументы функции, вызываемой указанным экземпляром Job.
    """
    if job.instance:
        if isinstance(job.instance, type):
            instance_class = job.instance
        else:
            instance_class = job.instance.__class__

        return "{}.{}.{}".format(
            instance_class.__module__,
            instance_class.__qualname__,
            job.get_call_string()
        )

    return job.get_call_string()


def get_job_func_short_repr(job: Job) -> str:
    """
    Возвращает короткое описание функции, вызываемой указанным экземпляром Job.
    """
    if job.instance:
        if isinstance(job.instance, type):
            instance_class = job.instance
        else:
            instance_class = job.instance.__class__

        return "{}.{}(...)".format(
            instance_class.__qualname__,
            job.func_name
        )

    return "{}(...)".format(
        job.func_name.rsplit(".", 1)[-1]
    )


def requeue_job(job: Job):
    """
    Повторный запуск задачи.

    Перезапустить можно только ту задачу, которая имеет статус `failed`, `finished`,
    `canceled`, `stopped` или `scheduled`.
    """
    queue = get_queue(job.origin)
    status = JobStatus(job.get_status())

    if status in {JobStatus.FAILED, JobStatus.FINISHED, JobStatus.CANCELED, JobStatus.STOPPED}:
        if supports_redis_streams(queue.connection):
            with queue.connection.pipeline() as pipe:
                job._remove_from_registries(pipeline=pipe)
                job.started_at = None
                job.ended_at = None
                job.last_heartbeat = None
                pipe.execute()

            # Нельзя включить в pipeline из-за ошибки, связанной с тем,
            # что enqueue_job() вызывает pipeline.multi(), который фейлится
            # из-за того, что в стеке уже есть команды.
            queue.enqueue_job(job)
        else:
            with queue.connection.pipeline() as pipe:
                job.created_at = utcnow()
                job.meta = {"original_job": job.id}
                job._id = None
                new_job = queue.enqueue_job(job)
                pipe.hdel(new_job.key, "result")
                pipe.hdel(new_job.key, "exc_info")
                pipe.execute()
                return new_job
    elif status is JobStatus.SCHEDULED:
        scheduler = get_job_scheduler(job)
        if scheduler:
            scheduler.enqueue_job(job)

    return job


def stop_job(job: Job):
    """
    Остановка / отмена выполнения задачи.
    Если задача повторяющаяся (repeat > 1), то вызов этой функции
    отменит лишь текущий запуск, но не последующие.
    """
    status = JobStatus(job.get_status())
    if status is JobStatus.STARTED:
        send_stop_job_command(job.connection, job.id)
    elif status in {JobStatus.FAILED, JobStatus.FINISHED, JobStatus.CANCELED, JobStatus.STOPPED}:
        # already stopped / cancelled / finished
        raise UnsupportedJobStatusError(
            job_id=job.id,
            status=status.value
        )
    elif status is JobStatus.SCHEDULED:
        scheduler = get_job_scheduler(job)
        if scheduler:
            scheduler.cancel(job)
            job.cancel()
    else:
        job.cancel()
