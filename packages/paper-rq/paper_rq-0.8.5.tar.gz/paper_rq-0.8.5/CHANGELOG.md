# Change Log

## [0.8.5](https://github.com/dldevinc/paper-rq/tree/v0.8.5) - 2024-12-20

### Features

-   Added `Duration` field.
-   Minor refactoring.

## [0.8.4](https://github.com/dldevinc/paper-rq/tree/v0.8.4) - 2024-12-19

### Bug Fixes

-   Fixed job's stdout duplication.

## [0.8.3](https://github.com/dldevinc/paper-rq/tree/v0.8.3) - 2024-01-13

### Bug Fixes

-   Fixed job's stdout logging.

## [0.8.2](https://github.com/dldevinc/paper-rq/tree/v0.8.2) - 2023-12-13

### Bug Fixes

-   Fixed job timeout for scheduled jobs.

## [0.8.1](https://github.com/dldevinc/paper-rq/tree/v0.8.1) - 2023-10-11

### Bug Fixes

-   The format of the `stdout` field has been updated.
-   Fixed an issue with custom Job classes.

## [0.8.0](https://github.com/dldevinc/paper-rq/tree/v0.8.0) - 2023-10-11

### Features

-   Added custom Job class to collect stdout messages.

## [0.7.3](https://github.com/dldevinc/paper-rq/tree/v0.7.3) - 2023-08-22

### Bug Fixes

-   Timezone fixes in admin interface.

## [0.7.2](https://github.com/dldevinc/paper-rq/tree/v0.7.2) - 2023-08-22

### Bug Fixes

-   Fixed icons.

## [0.7.1](https://github.com/dldevinc/paper-rq/tree/v0.7.1) - 2023-08-22

### Bug Fixes

-   Added missing migration file.

## [0.7.0](https://github.com/dldevinc/paper-rq/tree/v0.7.0) - 2023-08-21

### Features

-   Added support for Python 3.11.
-   Added support for Django 4.2.
-   Droped support for Django 2.2, 3.0, 3.1.
-   Droped support for Python 3.6.
-   Added support for `rq` >= 1.12.0.
-   Added `job` decorator.
-   Added `started_at` field to admin interface.

## [0.6.1](https://github.com/dldevinc/paper-rq/tree/v0.6.1) - 2022-11-18

### Features

-   The `helpers.stop_job()` function now shows a message for unstoppable jobs.

## [0.6.0](https://github.com/dldevinc/paper-rq/tree/v0.6.0) - 2022-11-09

### Features

-   Added new `helpers.stop_job()` function.
-   Added correct redirect after stopping and requeuing the job.

### Bug Fixes

-   `rq>=1.11` fixes an issue related to deleting a stopped job from 
    the `FailedJobRegistry`.

## [0.5.8](https://github.com/dldevinc/paper-rq/tree/v0.5.8) - 2022-10-18

### Features

-   Add tests against Django 4.1

## [0.5.7](https://github.com/dldevinc/paper-rq/tree/v0.5.7) - 2022-06-17

### Features

-   Display worker IP, hostname and date of last heartbeat.

## [0.5.6](https://github.com/dldevinc/paper-rq/tree/v0.5.6) - 2022-06-16

### Bug Fixes

-   Fixed an issue when Redis server is configured without port.

## [0.5.5](https://github.com/dldevinc/paper-rq/tree/v0.5.5) - 2022-04-19

### Features

-   Display job function.
-   Display jobs that raises `DeserializationError`.
-   Changed default job ordering.

### Bug Fixes

-   Fixed an issue with requeuing scheduled jobs.

## [0.5.4](https://github.com/dldevinc/paper-rq/tree/v0.5.4) - 2022-04-12

### Features

-   Add custom scheduler class.

### Bug Fixes

-   Fix an issue with expired jobs in the queue.
-   Ignore jobs that raise a `DeserializationError`.

## [0.5.3](https://github.com/dldevinc/paper-rq/tree/v0.5.3) - 2022-03-23

### Bug Fixes

-   Prevent scheduled jobs from changing status after they first run.

## [0.5.2](https://github.com/dldevinc/paper-rq/tree/v0.5.2) - 2022-03-16

### Bug Fixes

-   Fixed job search.

## [0.5.1](https://github.com/dldevinc/paper-rq/tree/v0.5.1) - 2022-03-15

### Features

-   Add `Stop job` button to the Job changeform.

### Bug Fixes

-   Fixed canceling scheduled jobs.

## [0.5.0](https://github.com/dldevinc/paper-rq/tree/v0.5.0) - 2022-03-14

### ⚠ BREAKING CHANGES

-   Drop support for Django 2.1.

### Features

-   Add ability to stop a job execution.
-   Add support for `stopped` and `cancelled` jobs.

### Bug Fixes

-   Fixed a bug that did not allow filtering jobs by status value.
-   Fixed issue with deleting a stopped jobs.

## [0.4.0](https://github.com/dldevinc/paper-rq/tree/v0.4.0) - 2022-01-13

### ⚠ BREAKING CHANGES

-   Add support for Python 3.10 and Django 4.0.

### Features

-   Add `scheduled_on` field for scheduled jobs.

## [0.3.3](https://github.com/dldevinc/paper-rq/tree/v0.3.3) - 2021-12-09

### Bug Fixes

-   Fixed issue with queue name other than `default`.

## [0.3.2](https://github.com/dldevinc/paper-rq/tree/v0.3.2) - 2021-10-14

### Features

-   Add support for `rq-scheduler`.

## [0.3.1](https://github.com/dldevinc/paper-rq/tree/v0.3.1) - 2021-10-13

### Features

-   Improve display of `callable` field in admin UI for class methods.
-   Added `timeout` field in admin UI.

## [0.3.0](https://github.com/dldevinc/paper-rq/tree/v0.3.0) - 2021-08-19

### ⚠ BREAKING CHANGES

-   Requires `paper-admin` >= 3.0

## [0.2.0](https://github.com/dldevinc/paper-rq/tree/v0.2.0) - 2021-04-13

### Features

-   Add an ability to search jobs by `ID`, `callable` string, `result`
    and `exception`.

### Bug Fixes

-   Fix multiple column ordering.

## [0.1.0](https://github.com/dldevinc/paper-rq/tree/v0.1.0) - 2021-04-12

-   First release
