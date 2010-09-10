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

__revision__ = "$LastChangedRevision$"
""" The revision number of the module """

__date__ = "$LastChangedDate$"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import colony.base.plugin_system

class MainLogPlugin(colony.base.plugin_system.Plugin):
    """
    The main class for the Log Main plugin
    """

    id = "pt.hive.colony.plugins.main.log"
    name = "Log Main Plugin"
    short_name = "Log Main"
    description = "Log Main Plugin"
    version = "1.0.0"
    author = "Hive Solutions Lda. <development@hive.pt>"
    loading_type = colony.base.plugin_system.EAGER_LOADING_TYPE
    platforms = [colony.base.plugin_system.CPYTHON_ENVIRONMENT]
    attributes = {"build_automation_file_path" : "$base{plugin_directory}/main_log/log/resources/baf.xml"}
    capabilities = ["log", "build_automation_item"]
    capabilities_allowed = []
    dependencies = []
    events_handled = []
    events_registrable = []
    main_modules = ["main_log.log.main_log_system"]

    loggers_map = {}

    def load_plugin(self):
        colony.base.plugin_system.Plugin.load_plugin(self)
        global main_log
        import main_log.log.main_log_system

    def get_logger(self, logger_name):
        if not logger_name in self.loggers_map:
            logger = main_log.log.main_log_system.DefaultLogger(logger_name)
            self.loggers_map[logger_name] = logger

        return self.loggers_map[logger_name]

    def get_default_handler(self):
        return main_log.log.main_log_system.DefaultHandler()

    def get_composite_handler(self):
        return main_log.log.main_log_system.CompositeHandler()
