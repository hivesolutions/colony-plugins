#!/usr/bin/python
# -*- coding: Cp1252 -*-

# Hive Colony Framework
# Copyright (C) 2008 Hive Solutions Lda.
#
# This file is part of Hive Colony Framework.
#
# Hive Colony Framework is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Hive Colony Framework is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Hive Colony Framework. If not, see <http://www.gnu.org/licenses/>.

__author__ = "Tiago Silva <tsilva@hive.pt>"
""" The author(s) of the module """

__version__ = "1.0.0"
""" The version of the module """

__revision__ = "$LastChangedRevision: 12670 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2011-01-13 13:08:29 +0000 (qui, 13 Jan 2011) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import re
import datetime

import http_log_parser_common_exceptions

COMMON_VALUE = "common"
""" The common value """

LOG_FILE_ENCODING = "Cp1252"
""" The log file encoding """

COMMON_LOG_FILE_ENTRY_REGEX = re.compile(
    "(?P<ip_address>[a-fA-F0-9\.\:]*) (?P<identity>.*) (?P<user_id>[a-zA-Z0-9_\-].*) " \
    "\[(?P<finish_time_day>\d\d)/(?P<finish_time_month>[A-Z][a-z][a-z])/(?P<finish_time_year>\d\d\d\d)\:(?P<finish_time_hours>\d\d)\:(?P<finish_time_minutes>\d\d)\:(?P<finish_time_seconds>\d\d) (?P<finish_time_timezone>[\+\-]\d\d\d\d)\] " \
    "\"(?P<request_type>[a-zA-Z]*) (?P<request_path>(\/[^\?#]+)+\/?(\?([^#])*)?(#(.*))?) (?P<request_protocol>HTTP/[0-9\.]+)\" " \
    "(?P<status_code>\d+) (?P<size>[\d\-]+)"
)
""" Common log file entry regex """

READ_CHUNK_SIZE = 10485760
""" The read chunk size in bytes """

LOG_FILE_LINE_ENDING = "\n"
""" The log file line ending """

MONTHS_MAP = {
    "Jan" : 1,
    "Feb" : 2,
    "Mar" : 3,
    "Apr" : 4,
    "May" : 5,
    "Jun" : 6,
    "Jul" : 7,
    "Aug" : 8,
    "Sep" : 9,
    "Oct" : 10,
    "Nov" : 11,
    "Dec" : 12
}
""" The months map """

class HttpLogParserCommon:
    """
    The log parser common class.
    """

    log_parser_common_plugin = None
    """ The log parser common plugin """

    def __init__(self, log_parser_common_plugin):
        """
        Constructor of the class.

        @type log_parser_common_plugin: LogParserCommonPlugin
        @param log_parser_common_plugin: The log parser common plugin.
        """

        self.log_parser_common_plugin = log_parser_common_plugin

    def get_log_type(self):
        return COMMON_VALUE

    def create_log_parser(self):
        # returns a common log parser instance
        return CommonLogParser()

class CommonLogParser:

    buffer = ""
    """ The parser's buffer """

    def __init__(self):
        self.buffer = ""

    def open(self, parameters):
        # retrieves the log file path form the parameters
        log_file_path = parameters["log_file_path"]

        # opens the log file
        self.log_file = open(log_file_path, "rb")

        # initializes the buffer
        self.buffer = ""

    def close(self, parameters):
        # closes the log file
        self.log_file.close()

    def get_next_log_entries(self):
        # initializes the log entries list
        log_entries = []

        # reads the log file data
        log_file_data = self.log_file.read(READ_CHUNK_SIZE)

        # decodes the log file data
        log_file_data = log_file_data.decode(LOG_FILE_ENCODING)

        # returns in case the end of the file has been reached
        if not log_file_data:
            return

        # adds the log file data to the buffer
        self.buffer += log_file_data

        # retrieves the log file lines
        log_lines = self.buffer.split(LOG_FILE_LINE_ENDING)

        # retrieves the last log line
        last_log_line = log_lines[-1]

        # clears the buffer in case the last line is complete
        if COMMON_LOG_FILE_ENTRY_REGEX.match(last_log_line):
            self.buffer = ""
        else:
            # keeps the last line in the buffer in case it's not complete
            self.buffer = last_log_line

            # removes the last log line from the log lines
            log_lines = log_lines[:-1]

        # collects the log entries
        for log_line in log_lines:
            # matches the log line against the common log file entry regex
            common_log_file_entry_match = COMMON_LOG_FILE_ENTRY_REGEX.match(log_line)

            # raises an exception in case the log file is not in the expected format
            if not common_log_file_entry_match:
                # raises the log parser common exception
                raise http_log_parser_common_exceptions.InvalidLogEntryFormat("log file is not in the expected common log file format")

            # retrieves the common log file entry attributes
            ip_address = common_log_file_entry_match.group("ip_address")
            identity = common_log_file_entry_match.group("identity")
            user_id = common_log_file_entry_match.group("user_id")
            finish_time_day = common_log_file_entry_match.group("finish_time_day")
            finish_time_month = common_log_file_entry_match.group("finish_time_month")
            finish_time_year = common_log_file_entry_match.group("finish_time_year")
            finish_time_hours = common_log_file_entry_match.group("finish_time_hours")
            finish_time_minutes = common_log_file_entry_match.group("finish_time_minutes")
            finish_time_seconds = common_log_file_entry_match.group("finish_time_seconds")
            request_type = common_log_file_entry_match.group("request_type")
            request_path = common_log_file_entry_match.group("request_path")
            request_protocol = common_log_file_entry_match.group("request_protocol")
            status_code = common_log_file_entry_match.group("status_code")
            size = common_log_file_entry_match.group("size")

            # converts not available attributes
            identity = identity == "-" and None or identity
            user_id = user_id == "-" and None or user_id
            size = not size == "-" and size or 0

            # converts attributes to the appropriate data types
            status_code = int(status_code)
            size = int(size)
            finish_time_year = int(finish_time_year)
            finish_time_month = MONTHS_MAP[finish_time_month]
            finish_time_day = int(finish_time_day)
            finish_time_hours = int(finish_time_hours)
            finish_time_minutes = int(finish_time_minutes)
            finish_time_seconds = int(finish_time_seconds)
            finish_datetime = datetime.datetime(finish_time_year, finish_time_month, finish_time_day, finish_time_hours, finish_time_minutes, finish_time_seconds)

            # defines the log entry map
            log_entry_map = {
                "ip_address" : ip_address,
                "identity" : identity,
                "user_id" : user_id,
                "finish_time" : finish_datetime,
                "request" : {
                    "type" : request_type,
                    "path" : request_path,
                    "protocol" : request_protocol
                },
                "status_code" : status_code,
                "size" : size
            }

            # appends the log entry map to the log entries list
            log_entries.append(log_entry_map)

        # returns the log entries
        return log_entries
