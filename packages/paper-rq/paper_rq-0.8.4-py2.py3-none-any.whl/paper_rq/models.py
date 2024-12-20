import datetime
import logging

from django.db import models
from django.db.models.manager import BaseManager
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _
from django_rq.queues import get_queue
from django_rq.settings import QUEUES_LIST
from rq.exceptions import DeserializationError
from rq.job import Job, JobStatus
from rq.queue import Queue
from rq.results import Result
from rq.worker import Worker

from . import helpers
from .list_queryset import ListQuerySet


class QueueManager(BaseManager):
    def all(self):
        queues = ListQuerySet(self.model)
        for index, config in enumerate(QUEUES_LIST):
            obj = self.model(
                name=config["name"],
                order=index
            )
            queues.append(obj)

        return queues

    def get(self, **kwargs):
        pk = kwargs.pop("pk", None)
        if pk is None:
            pk = kwargs.pop("name", None)

        if pk is not None:
            for index, config in enumerate(QUEUES_LIST):
                if pk == config["name"]:
                    return self.model(
                        name=config["name"],
                        order=index
                    )

        raise self.model.DoesNotExist


class QueueModel(models.Model):
    name = models.TextField(_("name"), primary_key=True)
    order = models.PositiveIntegerField(_("order"), default=0)

    objects = QueueManager()

    class Meta:
        managed = False
        verbose_name = _("queue")
        default_permissions = ()
        permissions = [
            ("manage", "Can manage RQ jobs")
        ]

    def __str__(self):
        return self.name

    @cached_property
    def queue(self) -> Queue:
        return get_queue(self.name)

    @property
    def worker_count(self):
        return Worker.count(queue=self.queue)


class WorkerManager(BaseManager):
    def all(self):
        workers = ListQuerySet(self.model)
        for worker in helpers.get_all_workers():
            obj = self.model.from_worker(worker)
            workers.append(obj)

        return workers

    def get(self, **kwargs):
        pk = kwargs.pop("pk", None)
        if pk is None:
            pk = kwargs.pop("name", None)

        if pk is not None:
            for worker in helpers.get_all_workers():
                if worker.name == pk:
                    return self.model.from_worker(worker)

        raise self.model.DoesNotExist


class WorkerModel(models.Model):
    name = models.TextField(_("name"), primary_key=True)
    pid = models.PositiveIntegerField(_("PID"))
    hostname = models.CharField(_("Hostname"), max_length=128)
    ip_address = models.CharField(_("IP address"), max_length=64)
    birth_date = models.DateTimeField(_("birth date"))
    last_heartbeat = models.DateTimeField(_("last heartbeat"), null=True)

    objects = WorkerManager()

    class Meta:
        managed = False
        verbose_name = _("worker")
        default_permissions = ()

    def __str__(self):
        return self.name

    @classmethod
    def from_worker(cls, worker):
        return cls(
            name=worker.name,
            pid=worker.pid,
            hostname=worker.hostname[:128],
            ip_address=worker.ip_address,
            birth_date=helpers.format_datetime(worker.birth_date),
            last_heartbeat=helpers.format_datetime(getattr(worker, "last_heartbeat", None))
        )

    @cached_property
    def worker(self) -> Worker:
        for worker in helpers.get_all_workers():
            if worker.name == self.name:
                return worker

    @property
    def state(self):
        return self.worker.get_state()


class JobManager(BaseManager):
    def all(self):
        jobs = ListQuerySet(self.model)
        for job in helpers.get_all_jobs():
            try:
                obj = self.model.from_job(job)
            except DeserializationError:
                logging.exception("An error occurred during deserialization the Job “{}”".format(job.id))
                continue
            else:
                jobs.append(obj)

        return jobs

    def get(self, **kwargs):
        pk = kwargs.pop("pk", None)
        if pk is None:
            pk = kwargs.pop("id", None)

        if pk is not None:
            job = helpers.get_job(pk)
            if job is not None:
                return self.model.from_job(job)

        raise self.model.DoesNotExist


class JobModel(models.Model):
    id = models.CharField(_("ID"), max_length=48, primary_key=True)
    queue = models.TextField(_("queue"))
    description = models.TextField(_("description"))
    timeout = models.TextField(_("timeout"))
    callable = models.TextField(_("callable"))
    result = models.TextField(_("result"))
    exception = models.TextField(_("exception"))
    meta = models.TextField(_("meta"))
    created_at = models.DateTimeField(_("created at"))
    enqueued_at = models.DateTimeField(_("enqueued at"), null=True)
    started_at = models.DateTimeField(_("started at"), null=True)
    ended_at = models.DateTimeField(_("ended at"), null=True)

    # флаг, устанавливаемый при ошибках десериализации задач
    invalid = models.BooleanField(_("invalid"), default=False, editable=False)

    objects = JobManager()

    class Meta:
        managed = False
        verbose_name = _("job")
        default_permissions = ()

    def __str__(self):
        return self.id

    @classmethod
    def from_job(cls, job):
        invalid = False

        try:
            job._deserialize_data()
        except DeserializationError:
            invalid = True
            job_callable = None
        else:
            job_callable = helpers.get_job_func_repr(job)

        return cls(
            id=job.id,
            queue=job.origin,
            description=job.description,
            timeout=_("Infinite") if job.timeout is None else str(job.timeout),
            callable=job_callable,
            result=job.result,
            exception=job.exc_info,
            meta=job.meta,
            created_at=helpers.format_datetime(job.created_at),
            enqueued_at=helpers.format_datetime(job.enqueued_at),
            started_at=helpers.format_datetime(job.started_at),
            ended_at=helpers.format_datetime(job.ended_at),
            invalid=invalid
        )

    @cached_property
    def job(self) -> Job:
        return helpers.get_job(self.id)

    @property
    def status(self):
        return JobStatus(self.job.get_status(refresh=False))

    @property
    def enqueue_time(self):
        return (
            self.enqueued_at
            or helpers.format_datetime(datetime.datetime(datetime.MINYEAR, 1, 1))
        )

    def latest_results(self):
        """
        Возвращает последние 10 результатов.
        """
        job_results_key = Result.get_key(self.job.id)
        response = self.job.connection.xrevrange(job_results_key, '+', '-', count=10)
        return [
            ResultModel.from_result(
                Result.restore(
                    self.job.id,
                    result_id.decode(),
                    payload,
                    connection=self.job.connection,
                    serializer=self.job.serializer
                )
            )
            for result_id, payload in response
        ]


class ResultModel(models.Model):
    TYPE_CHOICES = (
        (Result.Type.SUCCESSFUL, _("Successful")),
        (Result.Type.FAILED, _("Failed")),
        (Result.Type.STOPPED, _("Stopped")),
    )
    id = models.CharField(_("ID"), max_length=32, primary_key=True)
    job_id = models.CharField(_("Job"), max_length=48)
    type = models.SmallIntegerField(_("type"), choices=TYPE_CHOICES)
    stdout = models.TextField(_("stdout"))
    result = models.TextField(_("result"))
    exception = models.TextField(_("exception"))
    created_at = models.DateTimeField(_("created at"))

    class Meta:
        managed = False
        verbose_name = _("result")
        default_permissions = ()

    def __str__(self):
        return "Result(id={id}, type={type})".format(
            id=self.id,
            type=self.get_type_display()
        )

    @classmethod
    def from_result(cls, result: Result):
        return cls(
            id=result.id,
            job_id=result.job_id,
            type=result.type,
            stdout=getattr(result, "stdout", ""),
            result=result.return_value,
            exception=result.exc_string,
            created_at=result.created_at,
        )

    @cached_property
    def job(self) -> Job:
        return helpers.get_job(self.job_id)
