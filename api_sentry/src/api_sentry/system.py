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
import time
import uuid
import socket
import datetime
import platform
import linecache
import threading
import collections

import colony

from . import exceptions

DEFAULT_CHARSET = "utf-8"
""" The default charset """

DEFAULT_LEVEL = "error"
""" The default level to be used in the submission of
events for which no level is provided """

DEFAULT_PLATFORM = "python"
""" The platform value reported to Sentry, used by it to
decide the way the stack traces are rendered """

DEFAULT_TIMEOUT = 30.0
""" The default timeout (in seconds) that may elapse before
the pending events are flushed to the Sentry endpoint """

DEFAULT_MAX_LENGTH = 1
""" The default number of events that may be buffered before
a flush operation is triggered, note that the default value
implies an immediate submission of every event, as error
events are considered to be of low volume and losing one of
them on an abrupt process termination is not acceptable """

CONTEXT_LINES = 5
""" The number of source code lines gathered before and after
the line of a frame, used to provide context in Sentry """

POST_METHOD_VALUE = "POST"
""" The post method value """

CONTENT_TYPE_VALUE = "application/x-sentry-envelope"
""" The content type used in the submission of envelopes """

SENTRY_VERSION = "7"
""" The version of the Sentry protocol implemented by the client """

CLIENT_NAME = "colony-sentry"
""" The name of the client reported to Sentry, used by it in
the identification of the origin of the events """

CLIENT_VERSION = "1.0.0"
""" The version of the client reported to Sentry """

RATE_LIMIT_CODE = 429
""" The status code returned by Sentry once the rate limit
for the project has been exceeded """

DEFAULT_RETRY_AFTER = 60.0
""" The amount of time (in seconds) the client waits before
submitting again, in case the rate limit response does not
provide an explicit value for it """

TIMESTAMP_FORMAT = "%Y-%m-%dT%H:%M:%S.%fZ"
""" The format used in the serialization of the timestamp
values, as expected by the Sentry endpoint """


class APISentry(colony.System):
    """
    The API Sentry class.
    """

    def create_client(self, api_attributes, open_client=True):
        """
        Creates a client, with the given API attributes.

        :type api_attributes: Dictionary
        :param api_attributes: The API attributes to be used.
        :type open_client: bool
        :param open_client: If the client should be opened.
        :rtype: SentryClient
        :return: The created client.
        """

        # retrieves the client HTTP plugin
        client_http_plugin = self.plugin.client_http_plugin

        # retrieves the JSON plugin
        json_plugin = self.plugin.json_plugin

        # retrieves the various attributes to be used
        # in the construction of the Sentry client
        dsn = api_attributes.get("dsn", None)
        environment = api_attributes.get("environment", None)
        release = api_attributes.get("release", None)
        server_name = api_attributes.get("server_name", None)
        timeout = api_attributes.get("timeout", DEFAULT_TIMEOUT)
        max_length = api_attributes.get("max_length", DEFAULT_MAX_LENGTH)
        in_app_paths = api_attributes.get("in_app_paths", None)

        # creates a new client with the given options, opens
        # it in case it's required and returns the generated
        # client to the caller method
        sentry_client = SentryClient(
            json_plugin,
            client_http_plugin,
            dsn,
            environment=environment,
            release=release,
            server_name=server_name,
            timeout=timeout,
            max_length=max_length,
            in_app_paths=in_app_paths,
        )
        if open_client:
            sentry_client.open()
        return sentry_client


class SentryClient(object):
    """
    The Sentry client class, responsible for the construction
    of the event payloads and for their delivery to the Sentry
    ingestion endpoint using the envelope based protocol.

    The client buffers the events that are submitted to it and
    flushes them once either the maximum number of buffered
    events or the flush timeout has been reached.
    """

    json_plugin = None
    """ The JSON plugin, used in the serialization of both the
    envelope headers and the event payloads """

    client_http_plugin = None
    """ The client HTTP plugin, used in the submission of the
    envelopes to the Sentry endpoint """

    dsn = None
    """ The DSN (data source name) string that identifies both
    the target project and the credentials to be used """

    environment = None
    """ The name of the environment associated with the events
    submitted by the client (eg: production) """

    release = None
    """ The release identifier associated with the events
    submitted by the client, used by Sentry to determine the
    version in which a certain issue was introduced """

    server_name = None
    """ The name of the server associated with the events
    submitted by the client """

    timeout = None
    """ The amount of time (in seconds) that may elapse before
    the buffered events are flushed """

    max_length = None
    """ The number of events that may be buffered before a
    flush operation is triggered """

    in_app_paths = None
    """ The sequence of file system paths considered to contain
    application code, used in the classification of the frames """

    http_client = None
    """ The HTTP client currently in use, created in a lazy
    fashion once the first submission is performed """

    modules = None
    """ The map associating the name of each installed package
    with its version, built in a lazy fashion once the first
    event is built as it remains the same for the process """

    dsn_structure = None
    """ The structure resulting from the parsing of the DSN,
    containing both the endpoint URL and the public key """

    events = None
    """ The sequence of events pending submission to the
    Sentry endpoint """

    def __init__(
        self,
        json_plugin=None,
        client_http_plugin=None,
        dsn=None,
        environment=None,
        release=None,
        server_name=None,
        timeout=DEFAULT_TIMEOUT,
        max_length=DEFAULT_MAX_LENGTH,
        in_app_paths=None,
    ):
        """
        Constructor of the class.

        :type json_plugin: Plugin
        :param json_plugin: The JSON plugin to be used.
        :type client_http_plugin: Plugin
        :param client_http_plugin: The client HTTP plugin to be used.
        :type dsn: String
        :param dsn: The DSN string identifying the target project.
        :type environment: String
        :param environment: The name of the environment to be reported.
        :type release: String
        :param release: The release identifier to be reported.
        :type server_name: String
        :param server_name: The name of the server to be reported,
        defaulting to the host name of the current machine.
        :type timeout: float
        :param timeout: The flush timeout (in seconds).
        :type max_length: int
        :param max_length: The number of events that may be buffered.
        :type in_app_paths: List
        :param in_app_paths: The paths considered to contain application code.
        """

        self.json_plugin = json_plugin
        self.client_http_plugin = client_http_plugin
        self.dsn = dsn
        self.environment = environment
        self.release = release
        self.server_name = server_name or socket.gethostname()
        self.timeout = timeout
        self.max_length = max_length
        self.in_app_paths = in_app_paths or []
        self.dsn_structure = self.parse_dsn(dsn) if dsn else None
        self.events = collections.deque()
        self._last_flush = time.time()
        self._retry_after = 0.0
        self._flush_lock = threading.RLock()

    def open(self):
        """
        Opens the Sentry client.
        """

        pass

    def close(self):
        """
        Closes the Sentry client, flushing any pending event so
        that no information is lost in the process.
        """

        # flushes the pending events so that the complete set of
        # them reaches the Sentry endpoint, note that the flush
        # operation swallows any submission error by itself
        self.flush()

        # in case an HTTP client is defined closes it, releasing
        # the underlying connection
        if self.http_client:
            self.http_client.close({})
            self.http_client = None

    def parse_dsn(self, dsn):
        """
        Parses the provided DSN string, retrieving the structure that
        describes both the Sentry endpoint and the credentials that
        are going to be used in the submission of the events.

        :type dsn: String
        :param dsn: The DSN string to be parsed.
        :rtype: Dictionary
        :return: The structure describing the Sentry endpoint.
        """

        # parses the DSN using the URL infra-structure and retrieves
        # both the public key and the identifier of the project, note
        # that the project identifier is the last component of the path
        parsed = colony.legacy.urlparse(dsn)
        public_key = parsed.username
        path, _slash, project_id = parsed.path.rpartition("/")

        # verifies that the complete set of mandatory components is
        # present, raising an exception in case it's not, as no event
        # may be submitted using an incomplete DSN
        if not parsed.scheme or not parsed.hostname or not public_key:
            raise exceptions.InvalidDsn(dsn)
        if not project_id:
            raise exceptions.InvalidDsn(dsn)

        # rebuilds the network location taking into account the possible
        # existence of an explicit port in the provided DSN, note that an
        # IPv6 literal must be kept enclosed in brackets so that it remains
        # distinguishable from the port that may follow it
        netloc = parsed.hostname
        if ":" in netloc:
            netloc = "[%s]" % netloc
        if parsed.port:
            netloc += ":%d" % parsed.port

        # creates the envelope URL from the various components, note that
        # the path prefix is kept so that on-premises installations served
        # under a sub-path are properly supported
        envelope_url = "%s://%s%s/api/%s/envelope/" % (
            parsed.scheme,
            netloc,
            path,
            project_id,
        )
        return dict(
            public_key=public_key, project_id=project_id, envelope_url=envelope_url
        )

    def is_enabled(self):
        """
        Verifies if the client is in a state that allows the submission
        of events, meaning that a valid DSN has been provided and that
        the rate limit imposed by the endpoint has not been reached.

        :rtype: bool
        :return: If the client is able to submit events.
        """

        if not self.dsn_structure:
            return False
        if time.time() < self._retry_after:
            return False
        return True

    def build_frame(self, file_path, lineno, function):
        """
        Builds the structure that describes a single frame of a stack
        trace, gathering the source code around the referenced line so
        that proper context is provided in Sentry.

        :type file_path: String
        :param file_path: The path to the file of the frame.
        :type lineno: int
        :param lineno: The number of the line of the frame.
        :type function: String
        :param function: The name of the function of the frame.
        :rtype: Dictionary
        :return: The structure describing the frame.
        """

        # gathers the complete set of lines of the file of the frame
        # and uses the line number to determine the range of lines that
        # is going to be sent as the context of the frame
        lines = linecache.getlines(file_path)
        index = lineno - 1
        start = max(index - CONTEXT_LINES, 0)

        # builds the frame structure with the basic information about
        # it, note that the in app flag is used by Sentry to decide
        # which of the frames are highlighted in the interface
        frame = dict(
            filename=os.path.basename(file_path),
            abs_path=file_path,
            function=function,
            lineno=lineno,
            in_app=self.is_in_app(file_path),
        )

        # in case there are lines available for the file, sets the
        # context of the frame, stripping the newline characters that
        # would otherwise be displayed in the interface
        if lines and 0 <= index < len(lines):
            frame["context_line"] = lines[index].rstrip("\n")
            frame["pre_context"] = [value.rstrip("\n") for value in lines[start:index]]
            frame["post_context"] = [
                value.rstrip("\n")
                for value in lines[index + 1 : index + 1 + CONTEXT_LINES]
            ]

        return frame

    def build_stacktrace(self, traceback_list):
        """
        Builds the structure that describes a complete stack trace from
        the provided traceback object, iterating over the complete set
        of frames that compose it.

        :type traceback_list: Traceback
        :param traceback_list: The traceback object to be converted.
        :rtype: Dictionary
        :return: The structure describing the stack trace.
        """

        # iterates over the complete set of frames of the traceback
        # building the structure that describes each one of them, note
        # that the frames are sent from the oldest to the newest one
        frames = []
        while traceback_list:
            frame = traceback_list.tb_frame
            code = frame.f_code
            frames.append(
                self.build_frame(
                    code.co_filename, traceback_list.tb_lineno, code.co_name
                )
            )
            traceback_list = traceback_list.tb_next

        return dict(frames=frames)

    def is_in_app(self, file_path):
        """
        Verifies if the provided file path is considered to belong to
        the application, meaning that it's contained in one of the
        paths provided in the construction of the client.

        :type file_path: String
        :param file_path: The path of the file to be verified.
        :rtype: bool
        :return: If the file is considered to belong to the application.
        """

        # verifies the containment of the file in each of the application
        # paths, note that the separator is appended to the path so that a
        # sibling directory sharing the same prefix is not considered to be
        # contained in it (eg: "/opt/application" in "/opt/app")
        if not self.in_app_paths:
            return False
        file_path = os.path.abspath(file_path)
        for in_app_path in self.in_app_paths:
            in_app_path = os.path.abspath(in_app_path)
            if file_path == in_app_path:
                return True
            if file_path.startswith(in_app_path + os.sep):
                return True
        return False

    def build_os(self):
        """
        Builds the structure that describes the operating system under
        which the client is running, as expected by the Sentry endpoint
        for the operating system context.

        :rtype: Dictionary
        :return: The structure describing the operating system.
        """

        return dict(
            name=platform.system(),
            version=platform.release(),
            build=platform.version(),
            raw_description=platform.platform(),
        )

    def build_modules(self):
        """
        Builds the map that associates the name of each of the packages
        installed in the running environment with its version, so that
        the version of the libraries in use (eg: appier) is known in the
        analysis of each one of the events.

        Note that the map is only built for the Python versions that
        provide the metadata infra-structure of the import system.

        :rtype: Dictionary
        :return: The map associating the name of each installed package
        with its version.
        """

        # tries to import the metadata infra-structure, which is not
        # available for the older Python versions, in which case an
        # empty map is returned as no package information is gathered
        try:
            import importlib.metadata as metadata
        except ImportError:
            return dict()

        # iterates over the complete set of installed distributions to
        # gather their versions, skipping the ones whose metadata is not
        # valid (eg: an incomplete installation) as they have no name
        return dict(
            (distribution.metadata.get("Name"), distribution.version)
            for distribution in metadata.distributions()
            if distribution.metadata.get("Name")
        )

    def build_event(
        self,
        level=DEFAULT_LEVEL,
        logger=None,
        message=None,
        exception=None,
        stacktrace=None,
        request=None,
        user=None,
        tags=None,
        extra=None,
        breadcrumbs=None,
        contexts=None,
    ):
        """
        Builds the event payload from the provided components, setting
        only the ones that have been provided so that no empty values
        are sent to the Sentry endpoint.

        :type level: String
        :param level: The severity level of the event.
        :type logger: String
        :param logger: The name of the logger that originated the event.
        :type message: String
        :param message: The message associated with the event.
        :type exception: Exception
        :param exception: The exception that originated the event.
        :type stacktrace: Dictionary
        :param stacktrace: The stack trace associated with the event.
        :type request: Dictionary
        :param request: The description of the request being handled.
        :type user: Dictionary
        :param user: The description of the user of the request.
        :type tags: Dictionary
        :param tags: The tags to be associated with the event.
        :type extra: Dictionary
        :param extra: The extra information to be associated with the event.
        :type breadcrumbs: List
        :param breadcrumbs: The breadcrumbs that preceded the event.
        :type contexts: Dictionary
        :param contexts: The contexts to be associated with the event,
        extending (or overriding) the ones describing the environment.
        :rtype: Dictionary
        :return: The event payload ready to be submitted.
        """

        # creates the base event structure with the values that are
        # always present, note that the event identifier must be an
        # hexadecimal string of thirty two characters
        now = datetime.datetime.utcnow()
        event = dict(
            event_id=uuid.uuid4().hex,
            timestamp=now.strftime(TIMESTAMP_FORMAT),
            platform=DEFAULT_PLATFORM,
            level=level,
            server_name=self.server_name,
            contexts=dict(
                runtime=dict(name="python", version=platform.python_version()),
                os=self.build_os(),
            ),
        )

        # sets the values that describe the origin of the event, these
        # are only set in case they have been provided
        if logger:
            event["logger"] = logger
        if self.environment:
            event["environment"] = self.environment
        if self.release:
            event["release"] = self.release
        if message:
            event["message"] = dict(formatted=message)

        # in case an exception is provided builds the structure that
        # describes it, associating the stack trace with it so that
        # Sentry is able to group the event properly
        if exception:
            value = dict(
                type=exception.__class__.__name__,
                value=colony.legacy.UNICODE(exception),
            )
            if stacktrace:
                value["stacktrace"] = stacktrace
            event["exception"] = dict(values=[value])
        elif stacktrace:
            event["stacktrace"] = stacktrace

        # sets the remaining optional components of the event, note
        # that the breadcrumbs are wrapped in the structure expected
        # by the Sentry endpoint
        if request:
            event["request"] = request
        if user:
            event["user"] = user
        if tags:
            event["tags"] = tags
        if extra:
            event["extra"] = extra
        if breadcrumbs:
            event["breadcrumbs"] = dict(values=list(breadcrumbs))
        if contexts:
            event["contexts"].update(contexts)

        # sets the versions of the installed packages, building them only
        # once as they remain the same for the complete lifetime of the
        # process, note that a failure in their gathering must never be
        # the reason for an event not being built (and reported)
        if self.modules == None:
            try:
                self.modules = self.build_modules()
            except Exception:
                self.modules = dict()
        if self.modules:
            event["modules"] = self.modules

        return event

    def submit_event(self, event, raise_e=False):
        """
        Submits the provided event to the Sentry endpoint, buffering it
        until either the maximum number of buffered events or the flush
        timeout has been reached.

        :type event: Dictionary
        :param event: The event payload to be submitted.
        :type raise_e: bool
        :param raise_e: If an exception should be raised in case the
        flush operation fails.
        :rtype: bool
        :return: If the event has been accepted for submission.
        """

        # in case the client is not in a state that allows the submission
        # of events returns immediately in error, note that this also
        # covers the situation where the rate limit has been reached
        if not self.is_enabled():
            return False

        # buffers the event and determines if a flush operation should be
        # triggered, either because too many events are pending or because
        # too much time has elapsed since the last flush operation
        with self._flush_lock:
            self.events.append(event)
            event_overflow = len(self.events) >= self.max_length
            time_overflow = time.time() - self._last_flush > self.timeout
        should_flush = event_overflow or time_overflow
        if should_flush:
            try:
                self.flush(raise_e=raise_e)
            except Exception:
                if raise_e:
                    raise

        return True

    def flush(self, raise_e=False):
        """
        Flushes the complete set of pending events to the Sentry endpoint,
        submitting one envelope per event as required by the protocol.

        :type raise_e: bool
        :param raise_e: If an exception should be raised in case the
        submission of one of the events fails.
        """

        # swaps the sequence of pending events with an empty one and updates
        # the last flush timestamp, this is done before the actual submission
        # to avoid duplicated events being sent by concurrent threads
        with self._flush_lock:
            events = self.events
            if not events:
                return
            self.events = collections.deque()
            self._last_flush = time.time()

        # submits each of the pending events, note that this is a blocking
        # operation and runs outside of the lock so that other threads are
        # not prevented from buffering new events, in case one of the events
        # is refused the remaining ones are discarded as no useful purpose
        # is served by insisting on a endpoint that is refusing the events
        for event in events:
            try:
                if not self.submit_envelope(event):
                    break
            except Exception:
                if raise_e:
                    raise

    def build_envelope(self, event):
        """
        Builds the envelope payload for the provided event, following the
        newline delimited structure expected by the Sentry endpoint.

        :type event: Dictionary
        :param event: The event payload to be wrapped in an envelope.
        :rtype: String
        :return: The complete envelope payload.
        """

        # serializes the event payload as it's required to determine the
        # length of the item that is going to be sent in the item header
        now = datetime.datetime.utcnow()
        payload = self.json_plugin.dumps(event)

        # creates both the envelope header, identifying the event and the
        # target project, and the item header, describing the payload
        header = self.json_plugin.dumps(
            dict(
                event_id=event["event_id"],
                sent_at=now.strftime(TIMESTAMP_FORMAT),
                dsn=self.dsn,
            )
        )
        item_header = self.json_plugin.dumps(
            dict(type="event", length=len(colony.legacy.bytes(payload, force=True)))
        )

        # joins the various components of the envelope using the newline
        # character as the delimiter, as defined by the protocol
        return "\n".join((header, item_header, payload))

    def submit_envelope(self, event):
        """
        Submits the provided event to the Sentry endpoint, wrapping it in
        an envelope and handling the possible rate limiting imposed by it.

        :type event: Dictionary
        :param event: The event payload to be submitted.
        :rtype: bool
        :return: If the event has been accepted by the endpoint.
        """

        # builds both the envelope payload and the headers that authenticate
        # the client against the target project
        envelope = self.build_envelope(event)
        headers = {
            "X-Sentry-Auth": "Sentry sentry_version=%s, sentry_client=%s/%s, sentry_key=%s"
            % (
                SENTRY_VERSION,
                CLIENT_NAME,
                CLIENT_VERSION,
                self.dsn_structure["public_key"],
            )
        }

        # submits the envelope to the endpoint and verifies if the rate limit
        # has been reached, in which case the moment after which the client
        # may submit again is stored, avoiding further (useless) submissions
        http_response = self._fetch_url(
            self.dsn_structure["envelope_url"], envelope, headers
        )
        status_code = getattr(http_response, "status_code", None)
        if status_code == RATE_LIMIT_CODE:
            self._retry_after = time.time() + self._retry_delay(http_response)
            return False

        # verifies that the endpoint has effectively accepted the event, as
        # otherwise (eg: invalid credentials or rejected payload) the event
        # has been lost and the caller must not be told otherwise
        return self.is_success(status_code)

    def is_success(self, status_code):
        """
        Verifies if the provided status code is one that indicates that the
        event has been accepted by the endpoint.

        :type status_code: int
        :param status_code: The status code to be verified.
        :rtype: bool
        :return: If the status code indicates a successful submission.
        """

        if status_code == None:
            return False
        return status_code >= 200 and status_code < 300

    def _retry_delay(self, http_response):
        """
        Determines the amount of time the client should wait before
        submitting again, using the value provided by the endpoint
        whenever it's available.

        :type http_response: HTTPResponse
        :param http_response: The response from which the delay is
        going to be retrieved.
        :rtype: float
        :return: The amount of time (in seconds) to wait.
        """

        headers_map = getattr(http_response, "headers_map", None) or {}
        retry_after = headers_map.get("Retry-After", None)
        if retry_after == None:
            return DEFAULT_RETRY_AFTER
        try:
            return float(retry_after)
        except (TypeError, ValueError):
            return DEFAULT_RETRY_AFTER

    def _fetch_url(self, url, contents, headers):
        """
        Submits the provided contents to the given URL using the POST
        method and the provided set of headers.

        :type url: String
        :param url: The URL to be fetched.
        :type contents: String
        :param contents: The contents to be sent in the request.
        :type headers: Dictionary
        :param headers: The headers to be used in the request.
        :rtype: HTTPResponse
        :return: The resulting HTTP response.
        """

        # retrieves the HTTP client and uses it to submit the contents
        # to the provided URL, returning the response to the caller
        http_client = self._get_http_client()
        http_response = http_client.fetch_url(
            url,
            POST_METHOD_VALUE,
            headers=headers,
            content_type=CONTENT_TYPE_VALUE,
            content_type_charset=DEFAULT_CHARSET,
            contents=contents,
        )
        return http_response

    def _get_http_client(self):
        """
        Retrieves the HTTP client currently in use (in case it's created)
        if not created creates the HTTP client.

        :rtype: HTTPClient
        :return: The retrieved HTTP client.
        """

        # in case no HTTP client exists
        if not self.http_client:
            # creates the HTTP client
            self.http_client = self.client_http_plugin.create_client({})

            # opens the HTTP client
            self.http_client.open({})

        # returns the HTTP client
        return self.http_client
