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

__revision__ = "$LastChangedRevision: 2688 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2009-04-16 12:24:34 +0100 (qui, 16 Abr 2009) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import colony.base.plugin_system

class SecurityCaptchaPlugin(colony.base.plugin_system.Plugin):
    """
    The main class for the Security Captcha plugin.
    """

    id = "pt.hive.colony.plugins.security.captcha"
    name = "Security Captcha Plugin"
    short_name = "Security Captcha"
    description = "A plugin to generate captcha values"
    version = "1.0.0"
    author = "Hive Solutions Lda. <development@hive.pt>"
    loading_type = colony.base.plugin_system.EAGER_LOADING_TYPE
    platforms = [
        colony.base.plugin_system.CPYTHON_ENVIRONMENT,
        colony.base.plugin_system.JYTHON_ENVIRONMENT,
        colony.base.plugin_system.IRON_PYTHON_ENVIRONMENT
    ]
    attributes = {
        "build_automation_file_path" : "$base{plugin_directory}/security_captcha/captcha/resources/baf.xml"
    }
    capabilities = [
        "startup",
        "security_captcha",
        "build_automation_item"
    ]
    dependencies = [
        colony.base.plugin_system.PackageDependency("Python Imaging Library (PIL)", "PIL", "1.1.x", "http://www.pythonware.com/products/pil")
    ]
    main_modules = [
        "security_captcha.captcha.security_captcha_system"
    ]

    security_captcha = None
    """ The security captcha """

    def load_plugin(self):
        colony.base.plugin_system.Plugin.load_plugin(self)
        global security_captcha
        import security_captcha.captcha.security_captcha_system
        self.security_captcha = security_captcha.captcha.security_captcha_system.SecurityCaptcha(self)

    def end_load_plugin(self):
        colony.base.plugin_system.Plugin.end_load_plugin(self)

    def unload_plugin(self):
        colony.base.plugin_system.Plugin.unload_plugin(self)

    def end_unload_plugin(self):
        colony.base.plugin_system.Plugin.end_unload_plugin(self)

    def load_allowed(self, plugin, capability):
        colony.base.plugin_system.Plugin.load_allowed(self, plugin, capability)

    def unload_allowed(self, plugin, capability):
        colony.base.plugin_system.Plugin.unload_allowed(self, plugin, capability)

    def dependency_injected(self, plugin):
        colony.base.plugin_system.Plugin.dependency_injected(self, plugin)

    def generate_captcha(self, string_value, properties):
        return self.security_captcha.generate_captcha(string_value, properties)

    def generate_captcha_string_value(self, properties):
        return self.security_captcha.generate_captcha_string_value(properties)
