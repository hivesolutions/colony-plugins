# COP-004: Sentry Error Reporting

## Document Information

| Field               | Value                                            |
| ------------------- | ------------------------------------------------ |
| **Document Number** | COP-004                                          |
| **Date**            | 2026-09-11                                       |
| **Author**          | João Magalhães <joamag@hive.pt>                  |
| **Subject**         | Error Reporting to Sentry for MVC Solutions      |
| **Status**          | Implemented                                      |
| **Version**         | 1.0                                              |

## Description

### Problem

Errors raised in any of the layers of an MVC based solution are log and forget. They reach the rotating file handlers, the in memory handler and, whenever enabled, Logstash, but there is no aggregation, no grouping, no deduplication and no alerting. Diagnosing an incident means correlating log lines by hand against the source code, which is slow and loses everything that is not already part of the formatted message.

The gap is widest in two places. Controller exceptions are caught by the `serialized` decorator, logged at warning level without execution information and then swallowed once a serializer is defined, meaning that the exception and its stack trace never travel together. Scheduler tasks fail with nothing but an error log, so a recurring failure in a backup or in a report generation is effectively invisible.

### Solution

Two plugins, one providing the transport and the other the reporting, plus a single notification added to the MVC layer. Nothing is added to the framework core, so the reporting remains optional and both runtime loadable and unloadable.

| Component            | Responsibility                                                                                 |
| -------------------- | ---------------------------------------------------------------------------------------------- |
| `api_sentry`         | DSN parsing, event payload construction, envelope framing, submission and rate limit handling  |
| `diagnostics_sentry` | Log record capturing, request context, breadcrumbs, scrubbing and event assembly               |

The client is deliberately implemented in house rather than through a dependency on the official SDK, both because the framework still declares Python 2.7 support, which the official SDK dropped, and because its automatic instrumentation targets frameworks that Colony is not.

## Capture Surfaces

A logging handler attached to the `colony` logger is the primary capture mechanism. Every layer funnels through that single logger, so one handler covers all of them at once, including the ones that never reach the HTTP stack.

| Surface            | Mechanism                                                                       |
| ------------------ | ------------------------------------------------------------------------------- |
| Controller actions | The `request.exception` event, notified by the `serialized` decorator            |
| REST dispatch      | The `request.end` event, which already carries the exception when one is raised  |
| WSGI entrypoint    | The logging handler, from the error logged when a request fails                  |
| HTTP service       | The logging handler, from the exception processing of the service               |
| Scheduler tasks    | The logging handler, from the error logged when a task fails                     |
| Explicit logging   | The logging handler, at error and critical level by default                      |

The `request.exception` notification is required because the `serialized` decorator does not re-raise once a serializer or an exception handler is defined, meaning that the exception would otherwise never reach any other surface. It is emitted only where the exception is already being handled, so no control flow is changed.

The WSGI entrypoint only became a usable surface once it started logging the exception that prevented a request from being handled. Until then it built the error response for the client and discarded the exception, so the failures raised before the REST layer begins handling a request (a malformed resource path, for example) produced a silent server error that reached neither the observers nor any logging handler.

Lowering `SENTRY_LEVEL` below `ERROR` makes the warning that the `serialized` decorator logs for a handled controller exception a captured event of its own, so that failure is then reported both as a message and as an exception. The default level avoids it and the two events describe the same failure, so the duplication is a cost of the lower verbosity rather than a defect of it.

## Breadcrumbs

The event vocabulary already emitted by the framework maps onto breadcrumbs at no additional instrumentation cost. They are held in a bounded sequence per request and are only attached once an event is effectively reported.

| Event          | Breadcrumb                       |
| -------------- | -------------------------------- |
| `sql.executed` | Query operation, engine and time |
| `orm.begin`    | Kind of operation performed      |
| `template.end` | Template that has been rendered  |

The engines provide the query already encoded using the charset of the data source, and under Python 2 they provide it as the byte string itself. The decoding is therefore performed in a permissive fashion, as these notifications are synchronous and are emitted after the statement has been executed, meaning that an undecodable byte would otherwise turn a successful database operation into an application error.

## Configuration

Every value is read through the standard configuration infra-structure. The plugin is completely inert while no DSN is defined, so loading it in development costs nothing.

| Name                    | Type   | Default                             | Description                                                             |
| ----------------------- | ------ | ----------------------------------- | ----------------------------------------------------------------------- |
| `SENTRY_DSN`            | `str`  | `None`                              | The DSN of the target project, reporting is disabled while unset        |
| `SENTRY_ENVIRONMENT`    | `str`  | The plugin manager environment      | The name of the environment reported with each event                    |
| `SENTRY_RELEASE`        | `str`  | The plugin manager version          | The release identifier reported with each event                         |
| `SENTRY_SERVER_NAME`    | `str`  | The host name of the machine        | The name of the server reported with each event                         |
| `SENTRY_LEVEL`          | `str`  | `ERROR`                             | The minimum level of the log records that are captured                  |
| `SENTRY_SAMPLE_RATE`    | `float`| `1.0`                               | The fraction of the events that are effectively submitted               |
| `SENTRY_SEND_REQUEST`   | `bool` | `False`                             | If the contents of the request are included in the events               |
| `SENTRY_SEND_QUERY`     | `bool` | `False`                             | If the text of a query is recorded in its breadcrumb                    |
| `SENTRY_SEND_USER`      | `bool` | `True`                              | If the address and the user of the request are included in the events   |
| `SENTRY_BREADCRUMBS`    | `bool` | `True`                              | If the observed events are recorded as breadcrumbs                      |
| `SENTRY_MAX_BREADCRUMBS`| `int`  | `50`                                | The number of breadcrumbs kept for each request                         |
| `SENTRY_IGNORED`        | `list` | `ControllerValidationReasonFailed`  | The exception class names that are never reported                       |

## Scrubbing

The default posture is to scrub. A solution built on the framework may carry payment data, personal information and tax identifiers, so nothing that could hold those values leaves the process unless it has been explicitly enabled.

Always sent: the type, the value and the stack frames of the exception with the surrounding source lines, the logger name, the level, the path, the method, the status code, the address of the connection, the user of the session, the environment, the release, the server name, the runtime and operating system contexts, the versions of the installed packages, the version, release, build, modes and start time of the plugin manager, the identifiers of the process and of the thread, and the location of the logging call that originated a record.

Withheld unless `SENTRY_SEND_REQUEST` is enabled: the fields of the request. Even once enabled, every field whose name suggests that it holds a credential, a token, a card, a cookie or a session is replaced by a filtered marker, and the maps and sequences nested under a name that is not itself sensitive are descended into so that the same filtering applies below the top level. The local variables of a frame are never sent, as in a controller they routinely hold entity instances with complete customer records.

Withheld unless `SENTRY_SEND_QUERY` is enabled: the text of the queries recorded as breadcrumbs. The engines embed the values of the entities directly in the statements they execute, so the text of an insert or of an update carries the very values that the remaining rules withhold. Only the operation of the query is recorded by default, together with the engine and the timing.

## Implementation Details

### Delivery

Events are buffered and flushed once either the maximum number of buffered events or the flush timeout is reached, following the approach already used for Logstash. The buffer defaults to a single event, meaning that each one is submitted immediately, as error events are of low volume and losing one of them on an abrupt termination is not acceptable. Closing the client flushes whatever is still pending.

Once the endpoint answers with a rate limit response the moment after which the client may submit again is stored and every event raised until then is discarded without a request being performed, honouring the delay indicated by the endpoint whenever one is provided.

Only a successful response is taken as an acceptance of the event, so a rejected payload or an invalid credential is reported back to the caller instead of the event being silently considered delivered. A refused submission also stops the remaining events of a buffered flush, as no useful purpose is served by insisting on an endpoint that is refusing them.

The flush triggered by the timeout is only evaluated when an event is submitted, so a lone buffered event waits for the next one or for the closing of the client. This mirrors the behavior of the Logstash handler and is inert under the default buffer of a single event, where every event is submitted immediately.

### Safety

The reporting must never interfere with the operation that originated the event. Notifications propagate to the code being observed, so the reporting performed from an observer is wrapped and degrades silently. The capturing is additionally guarded against recursion, as an error logged by the reporting process itself would otherwise trigger an infinite loop when the configured level is low enough for it to be captured.

### Frames

Each frame carries the file, the function, the line and the source lines around it. A frame is flagged as belonging to the application whenever its file sits under one of the plugin paths, which is what decides the frames that are highlighted in the interface and the grouping of the events. The containment is tested at a directory boundary, so a sibling directory that merely shares the prefix of a plugin path is not taken for a descendant of it.

The traceback of an exception reported from an observer is taken from the exception itself and, under Python 2 where it does not carry one, from the execution information of the current thread, which is still the one of the exception being handled as these notifications are synchronous. Without it the events of the main MVC path would reach Sentry with no frames at all, losing both the failing location and the grouping that depends on it.

## References

* [Sentry Envelopes](https://develop.sentry.dev/sdk/envelopes/)
* [Sentry Event Payloads](https://develop.sentry.dev/sdk/event-payloads/)
* [Sentry Rate Limiting](https://develop.sentry.dev/sdk/rate-limiting/)
