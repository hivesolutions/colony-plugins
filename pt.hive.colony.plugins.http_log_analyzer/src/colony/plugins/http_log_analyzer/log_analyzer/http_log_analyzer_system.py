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

import os

import http_log_analyzer_exceptions

NOT_AVAILABLE_VALUE = "n/a"
""" The not available value """

ROTATION_LOG_FILE_NAME_FORMAT = "%s.%d"
""" The rotation log file name format """

class HttpLogAnalyzer:
    """
    The http log analyzer class.
    """

    http_log_analyzer_plugin = None
    """ The log analyzer plugin """

    http_log_parser_plugins_map = {}
    """ The http log parser plugins map """

    def __init__(self, http_log_analyzer_plugin):
        """
        Constructor of the class.

        @type http_log_analyzer_plugin: HttpLogAnalyzerPlugin
        @param http_log_analyzer_plugin: The http log analyzer plugin.
        """

        self.http_log_analyzer_plugin = http_log_analyzer_plugin
        self.log_parser_plugins_map = {}

    def http_log_parser_plugin_load(self, log_parser_plugin):
        # retrieves the log type
        log_type = log_parser_plugin.get_log_type()

        # sets the log parser plugin in the log parser plugins map
        self.log_parser_plugins_map[log_type] = log_parser_plugin

    def http_log_parser_plugin_unload(self, log_parser_plugin):
        # retrieves the log type
        log_type = log_parser_plugin.get_log_type()

        # unsets the log parser plugin from the log parser plugins map
        del self.log_parser_plugins_map[log_type]

    def analyze_log(self, log_file_path, log_type):
        # retrieves the log parser plugin for the log type
        log_parser_plugin = self.log_parser_plugins_map.get(log_type, None)

        # raises an exception in case the specified log parser plugin was not found
        if not log_parser_plugin:
            # raises the log not found exception
            raise http_log_analyzer_exceptions.LogParserNotFoundException("log parser not found")

        # retrieves the log file paths including rotation logs
        log_file_paths = self.get_log_file_paths(log_file_path)

        # initializes the analyzis map
        analyzis_map = {}

        # parses and analyzes all log files
        for log_file_path in log_file_paths:
            # retrieves the log parser
            log_parser = log_parser_plugin.create_log_parser()

            # opens the log parser
            log_parser.open({"log_file_path" : log_file_path})

            # analyzes all log entries
            while True:
                # retrieves the next log entries
                log_entries = log_parser.get_next_log_entries()

                # in case no log entries were retrieved
                if not log_entries:
                    # breaks the loop
                    break

                # analyzes the log entries
                self.analyze_log_entries(log_entries, analyzis_map)

            # closes the log parser
            log_parser.close({})

        # returns the analyzis map
        return analyzis_map

    def get_log_file_paths(self, log_file_path):
        # initializes the log file paths
        log_file_paths = [log_file_path]

        # initializes the rotation index
        rotation_index = 1

        # collects the rotation log file paths
        while True:
            # defines the rotation log file path
            rotation_log_file_path = ROTATION_LOG_FILE_NAME_FORMAT % (log_file_path, rotation_index)

            # returns the log file paths in case the rotation log doesn't exist
            if not os.path.exists(rotation_log_file_path):
                return log_file_paths

            # appends the rotation log file path to the log file paths
            log_file_paths.append(rotation_log_file_path)

            # increases the rotation index
            rotation_index += 1

    def analyze_log_entries(self, log_entries, log_analyzer_map):
        # performs analyzis by ip address
        self._analyze_log_entries_ip_addresses(log_entries, log_analyzer_map)

        # performs analyzis by file type
        self._analyze_log_entries_file_types(log_entries, log_analyzer_map)

        # performs analyzis by time
        self._analyze_log_entries_times(log_entries, log_analyzer_map)

        # performs analyzis by status code
        self._analyze_log_entries_status_codes(log_entries, log_analyzer_map)

        # returns the log analyzer map
        return log_analyzer_map

    def _analyze_log_entries_ip_addresses(self, log_entries, log_analyzer_map):
        # retrieves the ip addresses map
        ip_addresses_map = log_analyzer_map.get("ip_addresses", {})

        # updates the file type maps
        for log_entry_map in log_entries:
            # retrieves the log entry attributes
            ip_address = log_entry_map["ip_address"]
            size = log_entry_map["size"]

            # retrieves the ip address map
            ip_address_map = ip_addresses_map.get(ip_address, {})

            # retrieves the ip address' attributes
            ip_address_total_size = ip_address_map.get("total_size", 0)
            ip_address_hits = ip_address_map.get("hits", 0)

            # updates the ip address' attributes
            ip_address_total_size += size
            ip_address_hits += 1

            # sets the updated attributes in the ip address map
            ip_address_map["total_size"] = ip_address_total_size
            ip_address_map["hits"] = ip_address_hits

            # sets the updated ip address map in the ip addresses map
            ip_addresses_map[ip_address] = ip_address_map

        # sets the updated ip addresses map in the log analyzer map
        log_analyzer_map["ip_addresses"] = ip_addresses_map

    def _analyze_log_entries_file_types(self, log_entries, log_analyzer_map):
        # retrieves the file types map
        file_types_map = log_analyzer_map.get("file_types", {})

        # updates the file type maps
        for log_entry_map in log_entries:
            # retrieves the log entry attributes
            size = log_entry_map["size"]
            request = log_entry_map["request"]
            request_path = request["path"]

            # retrieves the request file type
            _request_base_path, request_file_type = os.path.splitext(request_path)

            # sets the request file type as not available in case none was found
            request_file_type = request_file_type and request_file_type or NOT_AVAILABLE_VALUE

            # retrieves the file type map
            file_type_map = file_types_map.get(request_file_type, {})

            # retrieves the file type total size
            file_type_total_size = file_type_map.get("total_size", 0)
            file_type_hits = file_type_map.get("hits", 0)

            # updates the file type attributes
            file_type_total_size += size
            file_type_hits += 1

            # sets the updated attributes in the file type map
            file_type_map["total_size"] = file_type_total_size
            file_type_map["hits"] = file_type_hits

            # sets the updated file type map in the file types map
            file_types_map[request_file_type] = file_type_map

        # sets the updated file types map in the log analyzer map
        log_analyzer_map["file_types"] = file_types_map

    def _analyze_log_entries_times(self, log_entries, log_analyzer_map):
        # retrieves the temporal maps
        times_map = log_analyzer_map.get("times", {})
        months_map = times_map.get("months", {})
        week_days_map = times_map.get("week_days", {})

        # updates the temporal maps
        for log_entry_map in log_entries:
            # retrieves the log entry attributes
            finish_time = log_entry_map["finish_time"]
            size = log_entry_map["size"]

            # retrieves the finish time attributes
            month = finish_time.month
            day = finish_time.isoweekday()

            # retrieves the month and day
            month_map = months_map.get(month, {})
            week_day_map = week_days_map.get(day, {})

            # retrieves the attributes
            month_total_size = month_map.get("total_size", 0)
            month_hits = month_map.get("hits", 0)
            day_total_size = week_day_map.get("total_size", 0)
            day_hits = week_day_map.get("hits", 0)

            # updates the attributes
            month_total_size += size
            month_hits += 1
            day_total_size += size
            day_hits += 1

            # sets the total sizes in the temporal maps
            month_map["total_size"] = month_total_size
            month_map["hits"] = month_hits
            week_day_map["total_size"] = day_total_size
            week_day_map["hits"] = day_hits

            # sets the updated month and day maps
            months_map[month] = month_map
            week_days_map[day] = week_day_map

        # sets the updated temporal maps in the log analyzer map
        times_map["week_days"] = week_days_map
        times_map["months"] = months_map
        log_analyzer_map["times"] = times_map

    def _analyze_log_entries_status_codes(self, log_entries, log_analyzer_map):
        # retrieves the status code maps from the log analyzer map
        status_codes_map = log_analyzer_map.get("status_codes", {})

        # counts the status codes in the log entries
        for log_entry_map in log_entries:
            # retrieves the log entry attributes
            status_code = log_entry_map["status_code"]
            size = log_entry_map["size"]

            # retrieves the status code map
            status_code_map = status_codes_map.get(status_code, {})

            # retrieves the status code total size
            status_code_total_size = status_code_map.get("total_size", 0)
            status_code_hits = status_code_map.get("hits", 0)

            # updates the status code attributes
            status_code_total_size += size
            status_code_hits += 1

            # sets the updated attributes in the status code map
            status_code_map["total_size"] = status_code_total_size
            status_code_map["hits"] = status_code_hits

            # sets the updated status code map in the status codes map
            status_codes_map[status_code] = status_code_map

        # sets the updated status code map in the log analyzer map
        log_analyzer_map["status_codes"] = status_codes_map
