#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Colony Framework
# Copyright (c) 2008-2012 Hive Solutions Lda.
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

__revision__ = "$LastChangedRevision$"
""" The revision number of the module """

__date__ = "$LastChangedDate$"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008-2012 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import sys

import colony

import base

mvc_utils = colony.__import__("mvc_utils")

class MainController(base.BaseController):

    def index(self, rest_request):
        # generates and processes the template with the provided values
        # changing the current rest request accordingly, note that there's
        # a defined partial page and a base template value defined
        self._template(
            rest_request = rest_request,
            template = "general/index.html.tpl",
            title = "Colony Framework",
            area = "home"
        )

    def plugins(self, rest_request):
        # generates and processes the template with the provided values
        # changing the current rest request accordingly, note that there's
        # a defined partial page and a base template value defined
        self._template(
            rest_request = rest_request,
            template = "general/plugins.html.tpl",
            title = "Plugins",
            area = "plugins"
        )

    def console(self, rest_request):
        # retrieves the reference to the plugin manager running
        # in the current context
        plugin_manager = self.plugin.manager

        # retrieves the current system information map to be used to
        # expose the system information to the console then retrieves
        # the python interpreter information from the system module
        system_information_map = plugin_manager.get_system_information_map()
        version = sys.version

        # generates and processes the template with the provided values
        # changing the current rest request accordingly, note that there's
        # a defined partial page and a base template value defined
        self._template(
            rest_request = rest_request,
            template = "general/console.html.tpl",
            title = "Console",
            area = "console",
            version = version,
            information = system_information_map
        )

    def log(self, rest_request):
        # retrieves the reference to the plugin manager running
        # in the current context
        plugin_manager = self.plugin.manager

        # tries to retrieve the provided count parameter that will
        # condition the amount of lines retrieved, defaulting to
        # the default value in case none is provided
        count = self.get_field(
            rest_request,
            "count",
            default = 3000,
            cast_type = int
        )

        # retrieves the memory handler installed in the current
        # plugin manager and then uses it to retrieve the sequence
        # containing the latest messages stored in it
        memory_handler = plugin_manager.get_log_handler("memory")
        latest = memory_handler.get_latest(count = count)
        latest.reverse()

        # generates and processes the template with the provided values
        # changing the current rest request accordingly, note that there's
        # a defined partial page and a base template value defined
        self._template(
            rest_request = rest_request,
            template = "general/log.html.tpl",
            title = "Log",
            area = "log",
            latest = latest
        )

    def about(self, rest_request):
        # retrieves the reference to the plugin manager running
        # in the current context
        plugin_manager = self.plugin.manager

        # retrieves the current system information map to be used to
        # expose the system information to the console then retrieves
        # the python interpreter information from the system module
        system_information_map = plugin_manager.get_system_information_map()
        version = sys.version

        # generates and processes the template with the provided values
        # changing the current rest request accordingly, note that there's
        # a defined partial page and a base template value defined
        self._template(
            rest_request = rest_request,
            template = "general/about.html.tpl",
            title = "About",
            area = "about",
            manager = plugin_manager,
            version = version,
            information = system_information_map
        )
