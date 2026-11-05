# [Colony Framework](http://getcolony.com)
This project contains the base plugins that provide the rich functionality associated with the Colony Framework. Here you'll find everything from the HTTP server, to the Web MVC stack, the Build Automation infrastructure, and everything else we call base.

The Colony Framework is an open-source plugin framework specification. Implementations of the specification offer a runtime component model, allowing plugins to be installed, started, stopped, updated, and uninstalled without requiring the application container to be stopped. The specification relies heavily on the Inversion of control principle, in order to make it easier for application components to discover and interact with each other.

Colony aims to eliminate the complexity typically associated with the creation of modular applications, through a simplified unified model for component development. Practical applications can range from modular enterprise software to application mashing.

## Quick start

* Download [Colony](http://hivesolutions.dyndns.org/integration_public/LATEST_SUCCESS/resources/colony_1.0.0_all.zip).
* Unzip the file, which will create a colony directory.
* Download the [Colony Base Plugins](http://hivesolutions.dyndns.org/integration_public/LATEST_SUCCESS/resources/colony-base-plugins_1.0.0_all.zip).
* Unzip the file's contents into the colony directory.
* Go to colony/scripts/<platform>
* Run the command 'colony'
* Check out that the [Colony Web Server](http://localhost:8080/) is up and running.
* Go to [Colony Manager](http://localhost:8080/manager/plugins#plugins) and manage your plugins.

## Configuration

Every configuration value is read through the configuration infra-structure of Colony, from an environment variable, the `.env` file or the `colony.json` file. The boolean values are enabled by `1`, `true` or `True`, and the string values of the resources may also reference environment variables (eg: `${HOME}`).

### Database

Controls the data source of the entity manager: its engine, the connection to the database, the creation and analysis of its schema and the logging of its queries. The connection values override the connection parameters given to the entity managers, the defaults below being the ones used when neither is set.

| Name                       | Type   | Default                                               | Description                                                                                                                                                                               |
| -------------------------- | ------ | ----------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **DB_ENGINE**              | `str`  | `sqlite`                                              | The engine of the entity managers of the MVC solutions: `sqlite`, `mysql` or `pgsql`.                                                                                                     |
| **DB_URL**                 | `str`  | `None`                                                | The URL of the MySQL database (eg: `mysql://user:password@localhost:3306/name`), setting its host, port, user, password and name at once, each of them still overridden by its own value. |
| **DB_HOST**                | `str`  | `localhost`                                           | The host of the MySQL or PostgreSQL server.                                                                                                                                               |
| **DB_PORT**                | `int`  | `3306`                                                | The port of the MySQL server.                                                                                                                                                             |
| **DB_USER**                | `str`  | `root` (MySQL), `postgres` (PostgreSQL)               | The user of the database server.                                                                                                                                                          |
| **DB_PASSWORD**            | `str`  | `root` (MySQL), `postgres` (PostgreSQL)               | The password of the user of the database server.                                                                                                                                          |
| **DB_NAME**                | `str`  | `DB_PREFIX` and `DB_SUFFIX`, or the entity manager ID | The name of the MySQL or PostgreSQL database.                                                                                                                                             |
| **DB_PREFIX**              | `str`  | `""`                                                  | The prefix of the default name of the database, which is then followed by `DB_SUFFIX` (the ID of the entity manager is used while the prefix is empty).                                   |
| **DB_SUFFIX**              | `str`  | `default`                                             | The suffix of the default name of the database, used only together with `DB_PREFIX`.                                                                                                      |
| **DB_ISOLATION**           | `str`  | `read committed` (MySQL), `serializable` (PostgreSQL) | The isolation level of the transactions of the database.                                                                                                                                  |
| **DB_ENCODING**            | `str`  | `None`                                                | The encoding of the MySQL database, queried from the database itself while unset.                                                                                                         |
| **DB_INSENSITIVE_COLLATE** | `str`  | `DB_COLLATE`                                          | The collation appended to the case insensitive filters of the queries (fallback: `DB_COLLATE`), an empty value leaving it out.                                                            |
| **DB_COLLATE**             | `str`  | `utf8_general_ci` (MySQL), `nocase` (SQLite)          | Same as `DB_INSENSITIVE_COLLATE`.                                                                                                                                                         |
| **DB_FILE**                | `str`  | A temporary file                                      | The path of the file of the SQLite database.                                                                                                                                              |
| **DB_SYNCHRONOUS**         | `int`  | `2`                                                   | The synchronization of the writes of the SQLite database to the disk (its `synchronous` pragma), `0` turning it off (eg: when running the tests on a busy disk).                          |
| **DB_READ_ONLY**           | `bool` | `False`                                               | If the data source is read only, any persistence of the entities raising an error.                                                                                                        |
| **BUILD_SCHEMA**           | `bool` | `True`                                                | If the entity manager creates the definitions (tables) of its entity classes and its generator when it starts.                                                                            |
| **ANALYSE_SCHEMA**         | `bool` | `True`                                                | If the entity manager analyses its entity classes when it starts.                                                                                                                         |
| **DATA_INHERITANCE**       | `str`  | `None`                                                | The inheritance strategy of every entity hierarchy, overriding the one of each class: `class_table` or `concrete_table` (see [COP-002](doc/design/002-concrete_table_inheritance.md)).    |
| **SHOW_SQL**               | `bool` | `False`                                               | If every SQL query is logged at the info level.                                                                                                                                           |
| **SHOW_SLOW_SQL**          | `bool` | `True`                                                | If the SQL queries that take more than 25 ms are logged at the info level.                                                                                                                |
| **DEBUG_SQL**              | `bool` | `True`                                                | If every SQL query is logged at the debug level.                                                                                                                                          |

### Session

Configures the sessions of the REST layer, and so of every MVC solution: the store that keeps them and how long they last. A Redis database is shared by every process that uses it (eg: the instances of a solution), so each solution should have a database of its own.

| Name                    | Type   | Default     | Description                                                                                                                                                                                                                     |
| ----------------------- | ------ | ----------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **SESSION**             | `str`  | `redis`     | The store of the sessions: `redis` or `shelve` (also `file`), the sessions being kept in memory when the store fails to load (eg: no `REDISTOGO_URL` for `redis`).                                                              |
| **REDISTOGO_URL**       | `str`  | `None`      | The URL of the Redis database of the `redis` sessions (eg: `redis://:password@localhost:6379/1`).                                                                                                                               |
| **SESSION_PATH**        | `str`  | `""`        | The directory of the `session.shelve` file of the `shelve` sessions, the working directory while empty.                                                                                                                         |
| **SESSION_TIMEOUT**     | `int`  | `2419200`   | The lifetime in seconds of a session since its last access (twenty eight days).                                                                                                                                                 |
| **SESSION_MAX_TIMEOUT** | `int`  | `154828800` | The maximum lifetime in seconds of a session since its creation, whatever its accesses (sixty four times the default timeout).                                                                                                  |
| **SESSION_FACTOR**      | `int`  | `None`      | The factor applied to `SESSION_TIMEOUT` to obtain the maximum lifetime of a session, overriding `SESSION_MAX_TIMEOUT`.                                                                                                          |
| **SESSION_KEEP**        | `bool` | `False`     | If the sessions are kept when the MVC service plugins are unloaded in development mode (eg: when the process stops), instead of cleared, as clearing a store shared by other processes (eg: Redis) flushes all of its sessions. |

### HTTP

Controls the HTTP service of Colony and the handling of the requests by the REST layer. Defining any of the server values replaces the end points of the service configuration with a single one.

| Name            | Type   | Default | Description                                                                                                                              |
| --------------- | ------ | ------- | ---------------------------------------------------------------------------------------------------------------------------------------- |
| **SERVER_HOST** | `str`  | `""`    | The host (address) to which the HTTP service binds, every interface while empty.                                                         |
| **SERVER_PORT** | `int`  | `8080`  | The port of the HTTP service.                                                                                                            |
| **SERVER_SSL**  | `bool` | `False` | If the HTTP service serves secure (SSL) connections.                                                                                     |
| **FORCE_SSL**   | `bool` | `False` | If the requests received over an insecure connection are redirected to their secure (HTTPS) URL.                                         |
| **BASE_URL**    | `str`  | `None`  | The base URL of the absolute URLs created by the controllers (eg: redirects), deduced from the host and path of the request while unset. |

### WSGI

Controls the CORS and security headers that the WSGI layer adds to every response. Each header is only added while `WSGI_SECURE_HEADERS` is set, an empty value of its own leaving it out.

| Name                      | Type   | Default                                                                                                              | Description                                                                    |
| ------------------------- | ------ | -------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------ |
| **WSGI_SECURE_HEADERS**   | `bool` | `True`                                                                                                               | If the CORS and security headers are added to the responses.                   |
| **WSGI_ALLOW_ORIGIN**     | `str`  | `*`                                                                                                                  | The value of the `Access-Control-Allow-Origin` header (fallback: `WSGI_CORS`). |
| **WSGI_CORS**             | `str`  | `*`                                                                                                                  | Same as `WSGI_ALLOW_ORIGIN`.                                                   |
| **WSGI_ALLOW_HEADERS**    | `str`  | `*, X-Requested-With`                                                                                                | The value of the `Access-Control-Allow-Headers` header.                        |
| **WSGI_ALLOW_METHODS**    | `str`  | `GET, POST, PUT, DELETE, PATCH, HEAD, OPTIONS`                                                                       | The value of the `Access-Control-Allow-Methods` header.                        |
| **WSGI_CONTENT_SECURITY** | `str`  | `default-src * ws://* wss://* data: blob:; script-src * 'unsafe-inline' 'unsafe-eval'; style-src * 'unsafe-inline';` | The value of the `Content-Security-Policy` header.                             |
| **WSGI_FRAME_OPTIONS**    | `str`  | `SAMEORIGIN`                                                                                                         | The value of the `X-Frame-Options` header.                                     |
| **WSGI_XSS_PROTECTION**   | `str`  | `1; mode=block`                                                                                                      | The value of the `X-XSS-Protection` header.                                    |
| **WSGI_CONTENT_OPTIONS**  | `str`  | `nosniff`                                                                                                            | The value of the `X-Content-Type-Options` header.                              |

### Templates

Controls the template engine used by the MVC solutions to render their pages.

| Name                  | Type   | Default | Description                                                                                                                                                       |
| --------------------- | ------ | ------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **TEMPLATE_COMPILER** | `bool` | `True`  | If the templates are compiled into Python bytecode for faster renders, the visitor rendering them otherwise (see [COP-003](doc/design/003-template_compiler.md)). |

### Diagnostics

Controls the collection of diagnostics and the reporting of errors to [Sentry](https://sentry.io), as described in [COP-004](doc/design/004-sentry_error_reporting.md). The Sentry reporting is completely inert while no DSN is defined.

| Name                          | Type    | Default                            | Description                                                                            |
| ----------------------------- | ------- | ---------------------------------- | -------------------------------------------------------------------------------------- |
| **DIAGNOSTICS**               | `bool`  | `False`                            | If the counts and timings of the requests, templates and ORM operations are collected. |
| **SENTRY_DSN**                | `str`   | `None`                             | The DSN of the target project, reporting is disabled while unset.                      |
| **SENTRY_ENVIRONMENT**        | `str`   | The plugin manager environment     | The name of the environment reported with each event.                                  |
| **SENTRY_RELEASE**            | `str`   | The plugin manager version         | The release identifier reported with each event.                                       |
| **SENTRY_SERVER_NAME**        | `str`   | The host name of the machine       | The name of the server reported with each event.                                       |
| **SENTRY_LEVEL**              | `str`   | `ERROR`                            | The minimum level of the log records that are captured.                                |
| **SENTRY_SAMPLE_RATE**        | `float` | `1.0`                              | The fraction of the events that are effectively submitted.                             |
| **SENTRY_SEND_REQUEST**       | `bool`  | `False`                            | If the contents of the request are included in the events.                             |
| **SENTRY_SEND_QUERY**         | `bool`  | `False`                            | If the text of a query is recorded in its breadcrumb.                                  |
| **SENTRY_SEND_USER**          | `bool`  | `True`                             | If the address and the user of the request are included in the events.                 |
| **SENTRY_BREADCRUMBS**        | `bool`  | `True`                             | If the observed events are recorded as breadcrumbs.                                    |
| **SENTRY_MAX_BREADCRUMBS**    | `int`   | `50`                               | The number of breadcrumbs kept for each request.                                       |
| **SENTRY_IGNORED**            | `list`  | `ControllerValidationReasonFailed` | The exception class names that are never reported.                                     |
| **SENTRY_SESSION_ATTRIBUTES** | `list`  | `[]`                               | The session attributes whose values are reported (eg: `system_company`).               |

### AT

Configures the client of the webservices of the Portuguese tax authority (Autoridade Tributária), used to communicate invoices and transport documents (see [COP-001](doc/design/001-at_invoice_api.md) and the [AT resources](api_at/src/api_at/resources/README.md) for the test mode). Each value overrides the attribute of the same name given to the client.

| Name                | Type   | Default                         | Description                                                                                                 |
| ------------------- | ------ | ------------------------------- | ----------------------------------------------------------------------------------------------------------- |
| **AT_TEST_MODE**    | `bool` | `False`                         | If the test webservices of AT are used, together with the test key and certificate bundled with the plugin. |
| **AT_KEY**          | `str`  | The `key` of the client         | The path of the private key file used to authenticate with AT outside of the test mode.                     |
| **AT_CERTIFICATE**  | `str`  | The `certificate` of the client | The path of the certificate file used to authenticate with AT outside of the test mode.                     |
| **AT_CONTENT_TYPE** | `str`  | `utf-8`                         | The charset of the content of the requests sent to AT.                                                      |
| **AT_SSL_VERSION**  | `str`  | `tls`                           | The version of the SSL (TLS) protocol of the connections to AT.                                             |

### Crypton

Controls the signature service of the Crypton plugin.

| Name                         | Type   | Default | Description                                                                        |
| ---------------------------- | ------ | ------- | ---------------------------------------------------------------------------------- |
| **CRYPTON_VALIDATE_API_KEY** | `bool` | `True`  | If the API key of the signature requests is validated against the known consumers. |

### Console

Controls the interactive console of Colony.

| Name         | Type   | Default | Description                                                           |
| ------------ | ------ | ------- | --------------------------------------------------------------------- |
| **TERMINAL** | `bool` | `False` | If the interactive console is started in the terminal of the process. |

## Features

* Build Automation infrastructure.
* Entity Manager ORM.
* Distribution stack for "viral" distribution.
* APNS Client.
* DNS Client.
* HTTP Client.
* LDAP Client.
* mDNS Client.
* SMTP Client.
* i18n stack.
* JSON-RPC Client.
* XML-RPC Client.
* BitTorrent Service.
* DNS Service.
* HTTP Service.
* IRC Service.
* mDNS Service.
* POP Service.
* SMTP Service.
* Telnet Service.
* XMPP Service.
* Thread pool.
* Full-text search infrastructure.
* MVC Stack.
* and more...

## Documentation

Design documents describing technical decisions and implementation details can be found in the [doc/design](doc/design/) directory.

## Contributing

Colony is currently in its early development stages, and we are open to contributions across various areas of work.
The best ways to get involved:

1. Join the [mailing list](http://groups.google.com/group/colony-users).
2. Send pull requests for bug fixes or new features and improvements.
3. Help make the [docs](http://getcolony.com/docs/colony/) better.

## Project information

* Colony Base Source: https://github.com/hivesolutions/colony
* Colony Base Plugins Source: https://github.com/hivesolutions/colony-plugins
* Web: http://getcolony.com
* Docs: http://getcolony.com/docs/colony/
* Mailing list: http://groups.google.com/group/colony-users
* Twitter: http://twitter.com/colonyframework

## License

Colony is currently licensed under the [Apache License, Version 2.0](http://www.apache.org/licenses/).

## Build Automation

[![Build Status](https://github.com/hivesolutions/colony-plugins/workflows/Main%20Workflow/badge.svg)](https://github.com/hivesolutions/colony-plugins/actions)
[![Coverage Status](https://coveralls.io/repos/hivesolutions/colony-plugins/badge.png?branch=master)](https://coveralls.io/r/hivesolutions/colony-plugins?branch=master)
