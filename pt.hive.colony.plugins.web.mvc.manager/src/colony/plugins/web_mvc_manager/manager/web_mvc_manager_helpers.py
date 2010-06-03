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

__author__ = "João Magalhães <joamag@hive.pt>"
""" The author(s) of the module """

__version__ = "1.0.0"
""" The version of the module """

__revision__ = "$LastChangedRevision: 421 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2008-11-20 15:16:53 +0000 (Qui, 20 Nov 2008) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

DEFAULT_ENCODING = "utf-8"
""" The default encoding value """

class SearchHelper:
    """
    The search helper.
    """

    web_mvc_manager_plugin = None
    """ The web mvc manager plugin """

    web_mvc_manager = None
    """ The web mvc manager """

    def __init__(self, web_mvc_manager_plugin, web_mvc_manager):
        """
        Constructor of the class.

        @type web_mvc_manager_plugin: WebMvcManagerPlugin
        @param web_mvc_manager_plugin: The web mvc manager plugin.
        @type web_mvc_manager: WebMvcManager
        @param web_mvc_manager: The web mvc manager.
        """

        self.web_mvc_manager_plugin = web_mvc_manager_plugin
        self.web_mvc_manager = web_mvc_manager

    def partial_filter(self, rest_request, contents_list):
        # processes the form data
        form_data_map = self.process_form_data(rest_request, DEFAULT_ENCODING)

        # retrieves the form data attributes
        start_record = int(form_data_map["start_record"])
        number_records = int(form_data_map["number_records"])

        # retrieves the partial contents list
        partial_contents_list = contents_list[start_record:start_record + number_records]

        # retrieves the total number of records from the contents list
        total_number_records = len(contents_list)

        # in case the total number of records is smaller
        # than the request number of records
        if total_number_records < number_records:
            # the number of records is set to the total number of records
            number_records = total_number_records

        # creates the filter contents tuple
        filter_contents = (partial_contents_list, start_record, number_records, total_number_records)

        # returns the filter contents tuple
        return filter_contents
