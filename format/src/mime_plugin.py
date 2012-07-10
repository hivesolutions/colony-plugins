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

import colony.base.system
import colony.base.decorators

class MimePlugin(colony.base.system.Plugin):
    """
    The main class for the Mime plugin.
    """

    id = "pt.hive.colony.plugins.format.mime"
    name = "Mime"
    description = "The plugin that offers the mime format support"
    version = "1.0.0"
    author = "Hive Solutions Lda. <development@hive.pt>"
    platforms = [
        colony.base.system.CPYTHON_ENVIRONMENT,
        colony.base.system.JYTHON_ENVIRONMENT,
        colony.base.system.IRON_PYTHON_ENVIRONMENT
    ]
    capabilities = [
        "format.mime"
    ]
    main_modules = [
        "format.mime.system"
    ]

    mime = None
    """ The mime """

    def load_plugin(self):
        colony.base.system.Plugin.load_plugin(self)
        import format.mime.system
        self.mime = format.mime.system.Mime(self)

    @colony.base.decorators.set_configuration_property
    def set_configuration_property(self, property_name, property):
        colony.base.system.Plugin.set_configuration_property(self, property_name, property)

    @colony.base.decorators.unset_configuration_property
    def unset_configuration_property(self, property_name):
        colony.base.system.Plugin.unset_configuration_property(self, property_name)

    def create_message(self, parameters):
        return self.mime.create_message(parameters)

    def create_message_part(self, parameters):
        return self.mime.create_message_part(parameters)

    def get_mime_type_file_name(self, file_name):
        return self.mime.get_mime_type_file_name(file_name)

    @colony.base.decorators.set_configuration_property_method("configuration")
    def configuration_set_configuration_property(self, property_name, property):
        self.mime.set_configuration_property(property)

    @colony.base.decorators.unset_configuration_property_method("configuration")
    def configuration_unset_configuration_property(self, property_name):
        self.mime.unset_configuration_property()
