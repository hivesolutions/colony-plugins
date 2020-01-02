#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Colony Framework
# Copyright (c) 2008-2020 Hive Solutions Lda.
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

__copyright__ = "Copyright (c) 2008-2020 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "Apache License, Version 2.0"
""" The license for the module """

import colony

class NangerPlugin(colony.Plugin):
    """
    The main class for the Nanger plugin.
    """

    id = "pt.hive.colony.plugins.nanger"
    name = "Nanger"
    description = "Plugin that provides a simple web interface for colony"
    version = "1.0.0"
    author = "Hive Solutions Lda. <development@hive.pt>"
    platforms = [
        colony.CPYTHON_ENVIRONMENT
    ]
    capabilities = [
        "mvc_service"
    ]
    dependencies = [
        colony.PluginDependency("pt.hive.colony.plugins.diagnostics"),
        colony.PluginDependency("pt.hive.colony.plugins.mvc.utils"),
        colony.PluginDependency("pt.hive.colony.plugins.misc.json")
    ]
    main_modules = [
        "nanger"
    ]

    def load_plugin(self):
        colony.Plugin.load_plugin(self)
        import nanger
        self.nanger = nanger.Nanger(self)

    def end_load_plugin(self):
        colony.Plugin.end_load_plugin(self)
        self.nanger.load_components()

    def unload_plugin(self):
        colony.Plugin.unload_plugin(self)
        self.nanger.unload_components()

    def get_patterns(self):
        """
        Retrieves the tuple of regular expressions to be used as patterns,
        to the mvc service. The tuple should relate the route with the handler
        method/function.

        :rtype: Tuple
        :return: The tuple of regular expressions to be used as patterns,
        to the mvc service.
        """

        return self.nanger.get_patterns()

    def get_resource_patterns(self):
        """
        Retrieves the tuple of regular expressions to be used as resource patterns,
        to the mvc service. The tuple should relate the route with the base
        file system path to be used.

        :rtype: Tuple
        :return: The tuple of regular expressions to be used as resource patterns,
        to the mvc service.
        """

        return self.nanger.get_resource_patterns()
