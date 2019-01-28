#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Colony Framework
# Copyright (c) 2008-2019 Hive Solutions Lda.
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

__version__ = "1.0.0"
""" The version of the module """

__revision__ = "$LastChangedRevision$"
""" The revision number of the module """

__date__ = "$LastChangedDate$"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008-2019 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "Apache License, Version 2.0"
""" The license for the module """

import colony

class ConsoleInterfacePlugin(colony.Plugin):
    """
    The main class for the Console Interface plugin.
    """

    id = "pt.hive.colony.plugins.console.interface"
    name = "Console Interface"
    description = "The console plugin that controls the console interface"
    version = "1.0.0"
    author = "Hive Solutions Lda. <development@hive.pt>"
    platforms = [
        colony.CPYTHON_ENVIRONMENT,
        colony.JYTHON_ENVIRONMENT,
        colony.IRON_PYTHON_ENVIRONMENT
    ]
    capabilities = [
        "main"
    ]
    dependencies = [
        colony.PluginDependency("pt.hive.colony.plugins.console")
    ]
    main_modules = [
        "console_interface"
    ]

    def load_plugin(self):
        colony.Plugin.load_plugin(self)
        import console_interface
        self.system = console_interface.ConsoleInterface(self)
        self.release_ready_semaphore()

    def end_load_plugin(self):
        colony.Plugin.end_load_plugin(self)
        self.system.load_console()

    def unload_plugin(self):
        colony.Plugin.unload_plugin(self)
        self.system.unload_console()

    def end_unload_plugin(self):
        colony.Plugin.end_unload_plugin(self)
        self.release_ready_semaphore()

    @colony.set_configuration_property
    def set_configuration_property(self, property_name, property):
        colony.Plugin.set_configuration_property(self, property_name, property)

    @colony.unset_configuration_property
    def unset_configuration_property(self, property_name):
        colony.Plugin.unset_configuration_property(self, property_name)

    @colony.set_configuration_property_method("configuration")
    def configuration_set_configuration_property(self, property_name, property):
        self.system.set_configuration_property(property)

    @colony.unset_configuration_property_method("configuration")
    def configuration_unset_configuration_property(self, property_name):
        self.system.unset_configuration_property()
