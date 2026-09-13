#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Colony Framework
# Copyright (c) 2008-2024 Hive Solutions Lda.
#
# This file is part of Hive Colony Framework.
#
# Hive Colony Framework is free software: you can redistribute it and/or modify
# it under the terms of the Apache License as published by the Apache
# Foundation, either version 2.0 of the License, or (at your option) any
# later version.
#
# Hive Colony Framework is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# Apache License for more details.
#
# You should have received a copy of the Apache License along with
# Hive Colony Framework. If not, see <http://www.apache.org/licenses/>.

__author__ = "João Magalhães <joamag@hive.pt>"
""" The author(s) of the module """

__copyright__ = "Copyright (c) 2008-2024 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "Apache License, Version 2.0"
""" The license for the module """

import os
import re
import sys
import time
import random
import hashlib
import logging
import threading
import collections

import colony

DEFAULT_LOGGER = "colony"
""" The name of the logger to which the handler responsible
for the capturing of the events is attached """

DEFAULT_LEVEL = "ERROR"
""" The default minimum level of the log records that are
going to be captured and reported """

DEFAULT_EVENT_LEVEL = "error"
""" The severity level associated with the events for which
no level may be determined """

DEFAULT_SAMPLE_RATE = 1.0
""" The default fraction of the events that are effectively
submitted to the Sentry endpoint """

DEFAULT_MAX_BREADCRUMBS = 50
""" The default number of breadcrumbs kept for each one of
the requests being handled """

DEFAULT_IGNORED = ["ControllerValidationReasonFailed"]
""" The names of the exception classes that are never reported,
as they are part of the expected control flow """

DEFAULT_SESSION_ATTRIBUTES = []
""" The names of the session attributes whose values are reported by
default, none as they are specific to each one of the solutions """

USER_NAMES = dict(
    id=("user_id", "object_id"),
    username=("username", "user_name", "login"),
    email=("email", "user_email"),
)
""" The map associating each one of the values that identify the user
with the names under which they are commonly stored, looked up by trial
and error in the session and then in the user object stored in it, as
each one of the solutions uses its own naming """

USER_OBJECT_NAMES = ("user", "account")
""" The names of the session attributes that commonly hold the object
representing the user, in which the values that identify the user are
looked up whenever they are not stored directly in the session """

OBJECT_NAMES = ("object_id", "id", "name", "username", "email")
""" The names of the attributes that identify an object stored in the
session (eg: the company of the user), the only ones reported for it
as the remaining ones may hold personal or even tax information """

LOCALE_NAMES = ("_locale", "locale", "language")
""" The names of the session attributes under which the locale of the
session is commonly stored, looked up by trial and error """

SESSION_TYPES = dict(RESTSession="memory", ShelveSession="file", RedisSession="redis")
""" The map associating the name of each one of the session classes
with the type of the storage in which its sessions are kept """

LEVELS_MAP = dict(
    DEBUG="debug", INFO="info", WARNING="warning", ERROR="error", CRITICAL="fatal"
)
""" The map that associates the name of the logging levels with
the severity levels understood by Sentry """

SCRUB_KEYS = (
    "authorization",
    "card",
    "cookie",
    "credential",
    "cvv",
    "iban",
    "key",
    "nib",
    "password",
    "secret",
    "session",
    "token",
)
""" The sequence of (lower cased) tokens that, once contained in
the name of a field, imply the scrubbing of its value """

SCRUBBED_VALUE = "[Filtered]"
""" The value that replaces the one of the fields considered to
be sensitive, mimics the one used by the official clients """

ADDRESS_HEADERS = ("forwarded", "x-client-ip", "x-forwarded-for", "x-real-ip")
""" The sequence of (lower cased) names of the headers that carry the
address of the client, only sent in case the user is to be sent """

MAX_QUERY_LENGTH = 1024
""" The maximum number of characters of a query kept in the
breadcrumb that describes it """

MAX_VALUE_LENGTH = 1024
""" The maximum number of characters of a value of the request kept
in the event, so that a large value (eg: an uploaded file) never leads
to the rejection of the complete event by the endpoint """

UNKNOWN_OPERATION = "UNKNOWN"
""" The operation reported for a query from which no leading
keyword may be determined """

ERROR_STATUS_CODE = 500
""" The status code reported for a request that failed with an
exception that does not define one of its own """

SESSION_HASH_LENGTH = 12
""" The number of characters of the hash of the session identifier
reported, enough to correlate the events of a session while never
exposing the identifier itself, as it's a credential """

ENV_NAMES = ("SERVER_NAME", "SERVER_PORT", "SERVER_PROTOCOL")
""" The names of the variables of the (WSGI) environment of a request
that describe the server by which it has been received """

BOT_REGEX = re.compile(
    r"bot|crawler|spider|scraper|slurp|facebookexternalhit", re.IGNORECASE
)
""" The regular expression that matches the user agents of the bots and
crawlers, verified before the remaining types of device as their user
agents may also contain the keywords of those types """

TABLET_REGEX = re.compile(r"iPad|Android(?!.*Mobile)|Tablet", re.IGNORECASE)
""" The regular expression that matches the user agents of the tablets,
verified before the mobile one as the tablets may include its keywords """

MOBILE_REGEX = re.compile(
    r"Mobile|iPhone|iPod|Android.*Mobile|Windows Phone", re.IGNORECASE
)
""" The regular expression that matches the user agents of the mobile
devices, any user agent not matched by the regular expressions of the
remaining types of device is considered to be the one of a desktop """

IDENTIFIER_REGEX = re.compile(r"^\d+(?=\.|$)")
""" The regular expression that matches a numeric identifier in a segment
of the path of a request (optionally followed by an extension), replaced
in the name of the transaction so that the requests to the same endpoint
share the same name """


class DiagnosticsSentry(colony.System):
    """
    The diagnostics Sentry class, responsible for the gathering of
    the errors raised in the various layers of the infra-structure
    and for their reporting to a Sentry compatible endpoint.

    The capturing of the errors is performed by a logging handler
    attached to the colony logger, meaning that every layer that
    logs an error is covered, including the ones (like the task
    scheduler) that never reach the HTTP stack.
    """

    client = None
    """ The Sentry client used in the submission of the events """

    handler = None
    """ The logging handler responsible for the capturing of the
    log records that originate the events """

    def __init__(self, plugin):
        colony.System.__init__(self, plugin)
        self.dsn = colony.conf("SENTRY_DSN", None)
        self.environment = colony.conf("SENTRY_ENVIRONMENT", None)
        self.release = colony.conf("SENTRY_RELEASE", None)
        self.server_name = colony.conf("SENTRY_SERVER_NAME", None)
        self.level = colony.conf("SENTRY_LEVEL", DEFAULT_LEVEL)
        self.sample_rate = colony.conf(
            "SENTRY_SAMPLE_RATE", DEFAULT_SAMPLE_RATE, cast=float
        )
        self.send_request = colony.conf("SENTRY_SEND_REQUEST", False, cast=bool)
        self.send_query = colony.conf("SENTRY_SEND_QUERY", False, cast=bool)
        self.send_user = colony.conf("SENTRY_SEND_USER", True, cast=bool)
        self.breadcrumbs = colony.conf("SENTRY_BREADCRUMBS", True, cast=bool)
        self.max_breadcrumbs = colony.conf(
            "SENTRY_MAX_BREADCRUMBS", DEFAULT_MAX_BREADCRUMBS, cast=int
        )
        self.ignored = colony.conf("SENTRY_IGNORED", DEFAULT_IGNORED, cast=list)
        self.session_attributes = colony.conf(
            "SENTRY_SESSION_ATTRIBUTES", DEFAULT_SESSION_ATTRIBUTES, cast=list
        )
        self.client = None
        self.handler = None
        self._local = threading.local()

    def start(self):
        """
        Starts the reporting process, creating the Sentry client and
        attaching both the logging handler and the observers that
        gather the context of the requests being handled.

        This operation is a no operation in case no DSN is defined,
        keeping the plugin completely inert by default.
        """

        if not self.dsn:
            return

        self.client = self.create_client()
        self.handler = SentryHandler(self, level=self._level())
        logging.getLogger(DEFAULT_LOGGER).addHandler(self.handler)

        colony.register_g("request.begin", self.request_begin)
        colony.register_g("request.end", self.request_end)
        colony.register_g("request.exception", self.request_exception)
        colony.register_g("template.end", self.template_end)
        colony.register_g("orm.begin", self.orm_begin)
        colony.register_g("sql.executed", self.sql_executed)

    def stop(self):
        """
        Stops the reporting process, detaching both the logging handler
        and the observers and flushing any event still pending, so that
        no information is lost in the unloading of the plugin.
        """

        if not self.client:
            return

        colony.unregister_g("request.begin", self.request_begin)
        colony.unregister_g("request.end", self.request_end)
        colony.unregister_g("request.exception", self.request_exception)
        colony.unregister_g("template.end", self.template_end)
        colony.unregister_g("orm.begin", self.orm_begin)
        colony.unregister_g("sql.executed", self.sql_executed)

        logging.getLogger(DEFAULT_LOGGER).removeHandler(self.handler)
        self.handler = None

        self.client.close()
        self.client = None

    def create_client(self):
        """
        Creates the Sentry client to be used in the submission of the
        events, using the configuration gathered from the environment
        and the information provided by the plugin manager.

        :rtype: SentryClient
        :return: The created Sentry client.
        """

        # retrieves the plugin manager and uses it to determine both the
        # default release and the paths considered to contain application
        # code, used in the classification of the frames of a stack trace
        plugin_manager = self.plugin.manager
        release = self.release or plugin_manager.get_version()
        environment = self.environment or plugin_manager.get_environment()

        # retrieves the Sentry API plugin and uses it to create the client
        # with the complete set of gathered attributes
        api_sentry_plugin = self.plugin.api_sentry_plugin
        return api_sentry_plugin.create_client(
            dict(
                dsn=self.dsn,
                environment=environment,
                release=release,
                server_name=self.server_name,
                in_app_paths=plugin_manager.get_plugin_paths(),
            )
        )

    def request_begin(self, request):
        """
        Handles the beginning of a request, storing it as the context of
        the current thread so that the events reported while it's being
        handled are properly described.

        :type request: RESTRequest
        :param request: The request that started being handled.
        """

        context = self._context()
        context.request = request
        context.breadcrumbs = collections.deque(maxlen=self.max_breadcrumbs)
        context.begin = time.time()

    def request_end(self, request, exception=None):
        """
        Handles the end of a request, reporting the exception that caused
        it to fail whenever one is provided and releasing the context
        associated with the current thread.

        :type request: RESTRequest
        :param request: The request that finished being handled.
        :type exception: Exception
        :param exception: The exception that caused the request to fail.
        """

        if exception:
            self.capture_safe(
                exception=exception,
                traceback_list=self.resolve_traceback(exception),
                request=request,
            )

        context = self._context()
        context.request = None
        context.breadcrumbs = None
        context.begin = None

    def request_exception(self, request, exception, exception_map=None):
        """
        Handles an exception that has been caught and handled by the MVC
        layer, reporting it as it would otherwise never reach any of the
        remaining error handling surfaces.

        :type request: RESTRequest
        :param request: The request under which the exception was raised.
        :type exception: Exception
        :param exception: The exception that has been handled.
        :type exception_map: Dictionary
        :param exception_map: The map describing the exception, as built
        by the MVC layer.
        """

        self.capture_safe(
            exception=exception,
            traceback_list=self.resolve_traceback(exception),
            request=request,
        )

    def resolve_traceback(self, exception):
        """
        Retrieves the traceback associated with the provided exception, note
        that the observers are notified while the handling of the exception
        is still in progress, meaning that the execution information is
        still available for the current thread.

        :type exception: Exception
        :param exception: The exception whose traceback is going to be
        retrieved.
        :rtype: Traceback
        :return: The traceback associated with the exception or an invalid
        value in case it may not be determined.
        """

        # tries to obtain the traceback directly from the exception, as
        # this is the most reliable source of it, note that under Python 2
        # the exceptions do not carry their own traceback
        traceback_list = getattr(exception, "__traceback__", None)
        if traceback_list:
            return traceback_list

        # falls back to the execution information of the current thread,
        # using it only in case it refers the very same exception so that
        # the traceback of an unrelated one is never reported
        _type, value, traceback_list = sys.exc_info()
        if value == exception:
            return traceback_list
        return None

    def template_end(self, identifier, template_file=None):
        """
        Handles the end of the rendering of a template, recording it as
        a breadcrumb of the request currently being handled.

        :type identifier: int
        :param identifier: The identifier of the rendering operation.
        :type template_file: TemplateFile
        :param template_file: The template file that has been rendered.
        """

        file_path = template_file and template_file.file_path
        self.add_breadcrumb("template", "template", dict(file_path=file_path))

    def orm_begin(self, identifier, operation, options=None):
        """
        Handles the beginning of an ORM operation, recording it as a
        breadcrumb of the request currently being handled.

        :type identifier: int
        :param identifier: The identifier of the ORM operation.
        :type operation: String
        :param operation: The kind of operation being performed.
        :type options: Dictionary
        :param options: The options of the operation.
        """

        self.add_breadcrumb("orm", operation, dict(operation=operation))

    def sql_executed(self, query, engine, time):
        """
        Handles the execution of a query, recording it as a breadcrumb
        of the request currently being handled.

        :type query: String
        :param query: The query that has been executed.
        :type engine: String
        :param engine: The name of the engine that executed the query.
        :type time: int
        :param time: The amount of time (in milliseconds) taken.
        """

        # decodes the query in a permissive fashion as the engines provide
        # it already encoded using the charset of the data source, meaning
        # that an undecodable byte must never break the operation that has
        # just been performed (the notification is a synchronous one)
        is_bytes = type(query) == colony.legacy.BYTES
        query = query.decode("utf-8", "replace") if is_bytes else query

        # determines the message of the breadcrumb, note that the text of
        # the query is only used in case it has been explicitly requested,
        # as the engines embed the values of the entities in it
        if self.send_query:
            message = query[:MAX_QUERY_LENGTH]
        else:
            message = self.query_operation(query)

        self.add_breadcrumb("query", message, dict(engine=engine, time=time))

    def query_operation(self, query):
        """
        Retrieves the operation of the provided query, meaning the leading
        keyword of it, to be used in the breadcrumbs whenever the text of
        the query itself may not be recorded.

        :type query: String
        :param query: The query whose operation is going to be retrieved.
        :rtype: String
        :return: The operation of the provided query.
        """

        query = query.strip()
        if not query:
            return UNKNOWN_OPERATION
        return query.split(None, 1)[0].upper()

    def add_breadcrumb(self, category, message, data=None):
        """
        Adds a breadcrumb to the sequence of the ones associated with the
        request currently being handled, note that the sequence is bounded
        meaning that the oldest breadcrumbs are discarded.

        :type category: String
        :param category: The category of the breadcrumb.
        :type message: String
        :param message: The message of the breadcrumb.
        :type data: Dictionary
        :param data: The extra data of the breadcrumb.
        """

        if not self.breadcrumbs:
            return
        breadcrumbs = self._context().breadcrumbs
        if breadcrumbs == None:
            return
        breadcrumbs.append(dict(category=category, message=message, data=data or {}))

    def capture_record(self, record):
        """
        Captures the provided log record, unpacking the exception
        information contained in it whenever it's available.

        :type record: LogRecord
        :param record: The log record to be captured.
        :rtype: bool
        :return: If the event has been accepted for submission.
        """

        # unpacks the execution information of the record in case it's
        # present, so that both the exception and its stack trace are
        # reported instead of the plain message
        exception = None
        traceback_list = None
        if record.exc_info:
            _type, exception, traceback_list = record.exc_info

        # captures the record together with the location of the logging
        # call that originated it, as it's the only reference to the code
        # responsible for the event whenever no stack trace is available
        return self.capture(
            exception=exception,
            traceback_list=traceback_list,
            message=record.getMessage(),
            level=LEVELS_MAP.get(record.levelname, DEFAULT_EVENT_LEVEL),
            logger=record.name,
            extra=dict(
                path=record.pathname, lineno=record.lineno, function=record.funcName
            ),
        )

    def capture(
        self,
        exception=None,
        traceback_list=None,
        message=None,
        level=None,
        logger=None,
        request=None,
        extra=None,
    ):
        """
        Captures the provided exception or message, building the complete
        event from it and from the context of the request currently being
        handled and submitting it to the Sentry endpoint.

        :type exception: Exception
        :param exception: The exception to be reported.
        :type traceback_list: Traceback
        :param traceback_list: The traceback associated with the exception.
        :type message: String
        :param message: The message to be reported.
        :type level: String
        :param level: The severity level of the event.
        :type logger: String
        :param logger: The name of the logger that originated the event.
        :type request: RESTRequest
        :param request: The request under which the event was originated,
        defaulting to the one associated with the current thread.
        :type extra: Dictionary
        :param extra: The extra information to be associated with the event.
        :rtype: bool
        :return: If the event has been accepted for submission.
        """

        # verifies that the reporting is enabled and that the event is
        # neither ignored nor discarded by the sampling process
        if not self.client:
            return False
        if self.is_ignored(exception):
            return False
        if not self.is_sampled():
            return False

        # verifies that the current thread is not already reporting an
        # event, as otherwise an error logged by the reporting process
        # itself would trigger an infinite recursion
        context = self._context()
        if context.capturing:
            return False

        # builds the stack trace from the traceback whenever one has been
        # provided and determines the request that provides the context
        stacktrace = (
            self.client.build_stacktrace(traceback_list) if traceback_list else None
        )
        request = request or context.request

        # builds the complete event and submits it to the endpoint, note
        # that the breadcrumbs are only sent together with the event
        context.capturing = True
        try:
            event = self.client.build_event(
                level=level or DEFAULT_EVENT_LEVEL,
                logger=logger,
                message=message,
                exception=exception,
                stacktrace=stacktrace,
                request=self.build_request(request),
                user=self.build_user(request),
                tags=self.build_tags(request, exception=exception),
                extra=extra,
                breadcrumbs=context.breadcrumbs,
                contexts=self.build_contexts(request, exception=exception),
                transaction=self.resolve_transaction(request),
            )
            return self.client.submit_event(event)
        finally:
            context.capturing = False

    def capture_safe(self, *args, **kwargs):
        """
        Captures an event in a safe fashion, meaning that any error raised
        in the reporting process is swallowed, as the reporting must never
        interfere with the operation that originated the event.

        :rtype: bool
        :return: If the event has been accepted for submission.
        """

        try:
            return self.capture(*args, **kwargs)
        except Exception:
            return False

    def build_request(self, request):
        """
        Builds the structure that describes the provided request, taking
        into account the configuration that controls the sending of the
        (possibly sensitive) contents of it.

        :type request: RESTRequest
        :param request: The request to be described.
        :rtype: Dictionary
        :return: The structure describing the request.
        """

        if not request:
            return None

        # gathers the basic description of the request, these values are
        # never considered sensitive and as such are always sent, note that
        # the URL is made absolute as only such an URL is presented by Sentry
        data = dict(method=request.get_method(), url=self.resolve_url(request))
        headers = self.build_headers(request)
        if headers:
            data["headers"] = headers
        env = self.build_env(request)
        if env:
            data["env"] = env

        # in case the sending of the contents of the request has not been
        # explicitly enabled returns immediately, avoiding the leaking of
        # any kind of sensitive information (the default posture)
        if not self.send_request:
            return data

        # gathers both the query string and the contents of the request, note
        # that the attributes of a request using the get method are the values
        # of its query string, so they are only reported as contents otherwise
        # and that their map is built as none is exposed by the request
        query_string = self.build_query_string(request)
        if query_string:
            data["query_string"] = query_string
        if not request.is_get():
            attributes = dict(
                (name, request.get_attribute(name))
                for name in request.get_attributes_list()
            )
            data["data"] = self.scrub_map(attributes)
        return data

    def resolve_url(self, request):
        """
        Resolves the absolute URL of the provided request, giving priority to
        the scheme and host forwarded by a proxy (if any) over the ones of the
        connection effectively established with the server.

        :type request: RESTRequest
        :param request: The request whose URL is going to be resolved.
        :rtype: String
        :return: The absolute URL of the request, or its path in case its
        host can not be determined.
        """

        # retrieves the host and the scheme of the request in a safe fashion,
        # as they may not be available for some of the more exotic kinds of
        # request, in which case the path is used as the URL of the request
        path = request.get_path()
        try:
            host = request.get_header("X-Forwarded-Host") or request.get_header("Host")
            scheme = request.get_header("X-Forwarded-Proto")
            secure = request.is_secure()
        except Exception:
            return path
        if not host:
            return path

        # uses only the first one of the values of the forwarded headers, as a
        # chain of proxies sets one value for each one of them, the first value
        # being the one of the request as received by the first proxy
        host = host.split(",", 1)[0].strip()
        scheme = scheme.split(",", 1)[0].strip() if scheme else None
        scheme = scheme or ("https" if secure else "http")
        return "%s://%s%s" % (scheme, host, path)

    def build_headers(self, request):
        """
        Builds the map of the headers of the provided request, filtering the
        values of the ones that carry credentials (eg: cookies), removing the
        ones that carry the address of the client in case the user is not to
        be sent and removing the query string of the referer, as it may carry
        tokens (eg: the one of a password reset).

        :type request: RESTRequest
        :param request: The request whose headers are going to be described.
        :rtype: Dictionary
        :return: The map of the headers of the request.
        """

        try:
            headers = request.get_headers()
        except Exception:
            headers = None
        if not headers:
            return None

        scrubbed = dict()
        for name, value in colony.legacy.items(headers):
            name_l = name.lower()
            if name_l in ADDRESS_HEADERS and not self.send_user:
                continue
            if self.is_sensitive(name):
                scrubbed[name] = SCRUBBED_VALUE
                continue
            value = self.scrub_value(value)
            if name_l == "referer":
                value = value.split("?", 1)[0]
            scrubbed[name] = value
        return scrubbed

    def build_env(self, request):
        """
        Builds the map describing the environment in which the provided
        request has been received, namely the connection effectively
        established with the server (commonly by a proxy) and the server
        itself, using the names of the variables of the CGI specification.

        :type request: RESTRequest
        :param request: The request whose environment is going to be described.
        :rtype: Dictionary
        :return: The map describing the environment of the request.
        """

        env = dict()

        # gathers the address of the connection effectively established with
        # the server, without resolving the forwarded headers, only sent in
        # case the user is to be sent as it may be the address of the client
        if self.send_user:
            try:
                address, port = request.get_connection_address(resolve=False)
            except Exception:
                address, port = None, None
            if address:
                env["REMOTE_ADDR"] = address
            if port:
                env["REMOTE_PORT"] = port

        # gathers the description of the server, completing it with the values
        # of the lower level request (eg: the WSGI environment) whenever they
        # are available for the kind of request that is being handled
        try:
            server_software = request.get_server_software()
            lower_request = request.get_request()
        except Exception:
            server_software, lower_request = None, None
        if server_software:
            env["SERVER_SOFTWARE"] = server_software
        environ = getattr(lower_request, "environ", None) or dict()
        for name in ENV_NAMES:
            if environ.get(name, None):
                env[name] = environ[name]
        protocol_version = getattr(lower_request, "protocol_version", None)
        if protocol_version and "SERVER_PROTOCOL" not in env:
            env["SERVER_PROTOCOL"] = protocol_version
        return env

    def build_query_string(self, request):
        """
        Builds the sequence of name and value pairs of the query string of the
        provided request, with the values of the sensitive names filtered.

        :type request: RESTRequest
        :param request: The request whose query string is going to be described.
        :rtype: List
        :return: The sequence of name and value pairs of the query string.
        """

        try:
            lower_request = request.get_request()
        except Exception:
            lower_request = None
        query_string = getattr(lower_request, "query_string", None)
        if not query_string:
            return None

        pairs = []
        query = colony.legacy.parse_qs(query_string, keep_blank_values=True)
        for name, values in sorted(colony.legacy.items(query)):
            for value in values:
                sensitive = self.is_sensitive(name)
                value = SCRUBBED_VALUE if sensitive else self.scrub_value(value)
                pairs.append([name, value])
        return pairs

    def build_user(self, request):
        """
        Builds the structure that describes the user of the provided
        request, using both the address of the connection and the
        values that identify the user stored in the session.

        :type request: RESTRequest
        :param request: The request whose user is going to be described.
        :rtype: Dictionary
        :return: The structure describing the user.
        """

        if not self.send_user:
            return None
        if not request:
            return None

        # gathers the address of the connection, note that this is done
        # in a safe fashion as the resolution of it may fail for some of
        # the more exotic kinds of request
        user = dict()
        try:
            address = request.get_address()
        except Exception:
            address = None
        if address:
            user["ip_address"] = address

        # tries to resolve the values that identify the user from the session
        # of the request, note that no session may exist for it and that the
        # resolution is performed in a safe fashion as it may fail
        try:
            session = request.get_session()
            values = self.resolve_user(session) if session else dict()
        except Exception:
            values = dict()
        user.update(values)

        return user or None

    def resolve_user(self, session):
        """
        Resolves the values that identify the user of the provided session by
        trial and error, looking them up under the names commonly used, first
        directly in the session and then in the object representing the user
        stored in it, considering only the values already loaded in the object.

        :type session: RESTSession
        :param session: The session whose user is going to be resolved.
        :rtype: Dictionary
        :return: The map of the values that identify the user.
        """

        user = dict()
        user_object = self._session_value(session, USER_OBJECT_NAMES)
        for key, names in colony.legacy.items(USER_NAMES):
            for name in names:
                value = session.get_attribute(name)
                if not self._is_scalar(value):
                    value = self._loaded_value(user_object, name)
                if not self._is_scalar(value):
                    continue
                user[key] = value
                break
        return user

    def build_tags(self, request, exception=None):
        """
        Builds the map of tags to be associated with the event, these
        are the values by which the events may be searched and grouped
        in the Sentry interface.

        :type request: RESTRequest
        :param request: The request that provides the context.
        :type exception: Exception
        :param exception: The exception that originated the event, used in
        the determination of the status code of the request.
        :rtype: Dictionary
        :return: The map of tags of the event.
        """

        if not request:
            return None

        tags = dict(method=request.get_method())
        status_code = self.resolve_status_code(request, exception)
        if status_code:
            tags["status_code"] = str(status_code)
        device_type = self.resolve_device_type(request)
        if device_type:
            tags["device_type"] = device_type
        return tags

    def resolve_device_type(self, request):
        """
        Resolves the type of the device from which the provided request has
        been sent (bot, tablet, mobile or desktop), using the keywords that
        are commonly present in its user agent.

        :type request: RESTRequest
        :param request: The request whose device is going to be resolved.
        :rtype: String
        :return: The type of the device, or an invalid value in case the
        request has no user agent.
        """

        try:
            user_agent = request.get_header("User-Agent")
        except Exception:
            user_agent = None
        if not user_agent:
            return None

        if BOT_REGEX.search(user_agent):
            return "bot"
        if TABLET_REGEX.search(user_agent):
            return "tablet"
        if MOBILE_REGEX.search(user_agent):
            return "mobile"
        return "desktop"

    def resolve_status_code(self, request, exception=None):
        """
        Determines the status code that is going to be reported for the
        provided request, note that in case an exception is provided the
        status code is derived from it, as the one of the request has not
        been assigned by the upper layers yet.

        :type request: RESTRequest
        :param request: The request whose status code is going to be
        determined.
        :type exception: Exception
        :param exception: The exception that originated the event.
        :rtype: int
        :return: The status code to be reported for the request.
        """

        # in case an exception is provided the status code is taken from it
        # defaulting to the internal error one, this is required as the
        # observers are notified before the upper layers assign the status
        # code of the error response to the request
        if exception:
            status_code = getattr(exception, "status_code", ERROR_STATUS_CODE)
            try:
                return int(status_code)
            except (TypeError, ValueError):
                return ERROR_STATUS_CODE

        # otherwise uses the one currently set in the request, note that the
        # retrieval is performed in a safe fashion as it may not be available
        # for some of the more exotic kinds of request
        try:
            return request.get_status_code()
        except Exception:
            return None

    def resolve_transaction(self, request):
        """
        Resolves the name of the transaction of the provided request, composed
        by its method and path, with the numeric identifiers of the path replaced
        so that the requests to the same endpoint share the same name.

        :type request: RESTRequest
        :param request: The request whose transaction is going to be resolved.
        :rtype: String
        :return: The name of the transaction of the request.
        """

        if not request:
            return None

        segments = request.get_path().split("/")
        segments = [IDENTIFIER_REGEX.sub("{id}", segment) for segment in segments]
        return "%s %s" % (request.get_method(), "/".join(segments))

    def build_contexts(self, request=None, exception=None):
        """
        Builds the contexts that describe the environment under which
        the event has been originated, namely the plugin manager and the
        process (and thread) in which it's running, together with both
        the session and the response of the request (if any).

        :type request: RESTRequest
        :param request: The request under which the event was originated.
        :type exception: Exception
        :param exception: The exception that originated the event.
        :rtype: Dictionary
        :return: The map of contexts to be associated with the event.
        """

        # gathers the information about the plugin manager, using the same
        # set of values exposed in the status of the system, note that the
        # information may not be available in case the event is originated
        # before the plugin manager has completed its start
        plugin_manager = self.plugin.manager
        system_information = plugin_manager.get_system_information_map() or dict()
        colony_context = dict(
            layout_mode=system_information.get("layout_mode", None),
            run_mode=system_information.get("run_mode", None),
            start_timestamp=system_information.get("timestamp", None),
            version=system_information.get("version", None),
            release=system_information.get("release", None),
            build=system_information.get("build", None),
            release_date_time=system_information.get("release_date_time", None),
            environment=system_information.get("environment", None),
        )

        # gathers the identifiers of the process and of the thread in which
        # the event has been originated, the same that are sent together with
        # each one of the records of the logging infra-structure
        thread = threading.current_thread()
        process_context = dict(pid=os.getpid(), tid=thread.ident, thread=thread.name)

        # gathers the contexts that describe both the session and the response
        # of the request, only available for the events that are originated
        # while a request is being handled
        contexts = dict(colony=colony_context, process=process_context)
        session_context = self.build_session(request)
        if session_context:
            contexts["session"] = session_context
        response_context = self.build_response(request, exception=exception)
        if response_context:
            contexts["response"] = response_context
        return contexts

    def build_session(self, request):
        """
        Builds the structure that describes the session of the provided
        request, namely the type of its storage, the hash of its identifier,
        its creation and expire times, its locale, the names of its attributes
        and the values of the ones configured to be reported.

        :type request: RESTRequest
        :param request: The request whose session is going to be described.
        :rtype: Dictionary
        :return: The structure describing the session.
        """

        if not request:
            return None

        # retrieves the session of the request in a safe fashion, as it may not
        # be possible to load it, note that many of the requests have no session
        try:
            session = request.get_session()
        except Exception:
            session = None
        if not session:
            return None

        # describes the storage and the lifetime of the session, together with
        # its locale and the names (never the values) of its attributes, note
        # that the storage is not described under the type name, as such name
        # is reserved by Sentry for the identification of the kind of context,
        # and that no creation time exists for the sessions created before it
        # was kept, as well as for the ones of the older versions of sessions
        name = session.get_name()
        context = dict(
            storage=SESSION_TYPES.get(name, name),
            creation_time=getattr(session, "creation_time", None),
            expire_time=session.get_expire_time(),
            locale=self._session_value(session, LOCALE_NAMES),
            attributes=sorted(session.attributes_map.keys()),
        )

        # reports the hash of the identifier of the session and never the
        # identifier itself, as it's the credential that grants access to it
        session_id = session.get_session_id()
        if session_id:
            session_id = colony.legacy.bytes(session_id, force=True)
            session_hash = hashlib.sha256(session_id).hexdigest()
            context["id_hash"] = session_hash[:SESSION_HASH_LENGTH]

        # in case the user is not to be sent returns immediately, as the values
        # of the attributes configured to be reported identify the operator of
        # the solution (eg: its company or its employee)
        if not self.send_user:
            return context

        values = dict()
        for name in self.session_attributes:
            value = session.get_attribute(name)
            if value == None:
                continue
            sensitive = self.is_sensitive(name)
            values[name] = SCRUBBED_VALUE if sensitive else self.describe_value(value)
        if values:
            context["values"] = values
        return context

    def build_response(self, request, exception=None):
        """
        Builds the structure that describes the response to the provided
        request as determined at the moment of the event, together with the
        time elapsed since the beginning of the handling of the request.

        :type request: RESTRequest
        :param request: The request whose response is going to be described.
        :type exception: Exception
        :param exception: The exception that originated the event, used in
        the determination of the status code of the response.
        :rtype: Dictionary
        :return: The structure describing the response.
        """

        if not request:
            return None

        response = dict()
        status_code = self.resolve_status_code(request, exception)
        if status_code:
            response["status_code"] = status_code

        # retrieves both the content type and the encoder of the response in a
        # safe fashion, as they are only defined once the response is built
        try:
            content_type = request.get_content_type()
            encoder_name = request.get_encoder_name()
        except Exception:
            content_type, encoder_name = None, None
        if content_type:
            response["content_type"] = content_type
        if encoder_name:
            response["encoder"] = encoder_name

        # calculates the time elapsed since the beginning of the handling of the
        # request, only possible for the request that is being handled by the
        # current thread, as the beginning of it is kept in its context
        context = self._context()
        if context.request == request and context.begin:
            response["elapsed"] = time.time() - context.begin

        return response or None

    def describe_value(self, value):
        """
        Describes the provided value of an attribute of the session, reporting
        it as is in case it's a scalar and only the attributes that identify it
        in case it's a map or an object (eg: an entity), as the remaining ones
        may hold personal or even tax information.

        :type value: Object
        :param value: The value of the attribute to be described.
        :rtype: Object
        :return: The description of the value.
        """

        if self._is_scalar(value):
            return self.scrub_value(value)

        description = dict()
        for name in OBJECT_NAMES:
            _value = self._loaded_value(value, name)
            if self._is_scalar(_value):
                description[name] = _value
        return description

    def scrub_map(self, values_map):
        """
        Scrubs the provided map, replacing the values of the fields whose
        name suggests that they contain sensitive information.

        :type values_map: Dictionary
        :param values_map: The map to be scrubbed.
        :rtype: Dictionary
        :return: The scrubbed version of the provided map.
        """

        if not values_map:
            return {}

        scrubbed = dict()
        for name, value in colony.legacy.items(values_map):
            scrubbed[name] = (
                SCRUBBED_VALUE if self.is_sensitive(name) else self.scrub_value(value)
            )
        return scrubbed

    def scrub_value(self, value):
        """
        Scrubs the provided value, descending into it in case it's a
        container so that a sensitive field nested under a name that is
        not itself sensitive is scrubbed as expected.

        :type value: Object
        :param value: The value to be scrubbed.
        :rtype: Object
        :return: The scrubbed version of the provided value.
        """

        # in case the value is a map descends into it, reusing the scrubbing
        # of the maps so that the names of the nested fields are verified
        if isinstance(value, dict):
            return self.scrub_map(value)

        # in case the value is a sequence scrubs each of its items, note that
        # the strings are excluded as they are the scalar values themselves
        if isinstance(value, (list, tuple)):
            return [self.scrub_value(item) for item in value]

        # converts the (scalar) value into its textual representation, as the
        # payload of the event must be serializable, truncating it in case it's
        # too large so that the event is never rejected because of its size
        value = colony.legacy.UNICODE(value)
        if len(value) > MAX_VALUE_LENGTH:
            value = value[:MAX_VALUE_LENGTH] + "..."
        return value

    def is_sensitive(self, name):
        """
        Verifies if the field with the provided name is considered to
        contain sensitive information.

        :type name: String
        :param name: The name of the field to be verified.
        :rtype: bool
        :return: If the field is considered to be sensitive.
        """

        name = colony.legacy.UNICODE(name).lower()
        for key in SCRUB_KEYS:
            if key in name:
                return True
        return False

    def is_ignored(self, exception):
        """
        Verifies if the provided exception is one of the ones that are
        never reported, as they are part of the expected control flow.

        :type exception: Exception
        :param exception: The exception to be verified.
        :rtype: bool
        :return: If the exception should be ignored.
        """

        if not exception:
            return False
        return exception.__class__.__name__ in self.ignored

    def is_sampled(self):
        """
        Verifies if the event should be submitted taking into account
        the sampling rate currently defined.

        :rtype: bool
        :return: If the event should be submitted.
        """

        if self.sample_rate >= 1.0:
            return True
        return random.random() < self.sample_rate

    def _context(self):
        """
        Retrieves the context associated with the current thread,
        initializing it in case it has not been initialized yet.

        :rtype: Object
        :return: The context of the current thread.
        """

        if not hasattr(self._local, "request"):
            self._local.request = None
            self._local.breadcrumbs = None
            self._local.capturing = False
            self._local.begin = None
        return self._local

    def _level(self):
        """
        Converts the configured level into the numeric value expected
        by the logging infra-structure.

        :rtype: int
        :return: The numeric value of the configured level.
        """

        return logging.getLevelName(self.level.upper())

    def _session_value(self, session, names):
        """
        Retrieves the value of the first one of the attributes of the provided
        session, under the given names, that is defined.

        :type session: RESTSession
        :param session: The session from which the value is retrieved.
        :type names: Tuple
        :param names: The names of the attributes to be looked up, by order.
        :rtype: Object
        :return: The value of the first attribute defined, or an invalid value
        in case none of the attributes is defined.
        """

        for name in names:
            value = session.get_attribute(name)
            if not value == None:
                return value
        return None

    def _loaded_value(self, value, name):
        """
        Retrieves the value of the attribute with the provided name from the
        given map or object, considering only the values already loaded in an
        object, so that no access to the data source is triggered for an entity
        whose attributes are loaded in a lazy fashion.

        :type value: Object
        :param value: The map or object from which the value is retrieved.
        :type name: String
        :param name: The name of the attribute to be retrieved.
        :rtype: Object
        :return: The value of the attribute, or an invalid value in case it's
        not defined (or not loaded).
        """

        if isinstance(value, dict):
            return value.get(name, None)
        values = getattr(value, "__dict__", None) or dict()
        return values.get(name, None)

    def _is_scalar(self, value):
        """
        Verifies if the provided value is a (non empty) scalar value, that may
        be reported as is, as opposed to a container or an object.

        :type value: Object
        :param value: The value to be verified.
        :rtype: bool
        :return: If the value is a non empty scalar value.
        """

        if not isinstance(value, colony.legacy.STRINGS + colony.legacy.INTEGERS):
            return False
        return not value == ""


class SentryHandler(logging.Handler):
    """
    Logging handler that reports the log records that reach it to a
    Sentry compatible endpoint, this is the mechanism that provides
    coverage over the complete set of layers of the infra-structure.
    """

    owner = None
    """ The system object that owns the handler and that performs
    the effective capturing of the records """

    def __init__(self, owner, level=logging.ERROR):
        logging.Handler.__init__(self, level=level)
        self.owner = owner

    def emit(self, record):
        """
        Emit a record, reporting it to the Sentry endpoint whenever
        it's considered to describe an error.

        :type record: Record
        :param record: The log record to be reported.
        """

        # in case the record to be emitted has been marked as being
        # part of a stack (traceback) then ignores it (noise)
        if hasattr(record, "stack") and record.stack:
            return

        try:
            self.owner.capture_record(record)
        except Exception:
            # handles the error in the proper manner, note that an
            # error in the reporting must never propagate to the
            # code that originated the log record
            self.handleError(record)
