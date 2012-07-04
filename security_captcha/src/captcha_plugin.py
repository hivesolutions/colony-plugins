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

class CaptchaPlugin(colony.base.system.Plugin):
    """
    The main class for the Captcha plugin.
    """

    id = "pt.hive.colony.plugins.security.captcha"
    name = "Security Captcha"
    description = "A plugin to generate captcha values"
    version = "1.0.0"
    author = "Hive Solutions Lda. <development@hive.pt>"
    platforms = [
        colony.base.system.CPYTHON_ENVIRONMENT,
        colony.base.system.JYTHON_ENVIRONMENT,
        colony.base.system.IRON_PYTHON_ENVIRONMENT
    ]
    capabilities = [
        "startup",
        "security_captcha"
    ]
    dependencies = [
        colony.base.system.PackageDependency("Python Imaging Library (PIL)", "PIL", "1.1.x", "http://www.pythonware.com/products/pil")
    ]
    main_modules = [
        "captcha.system"
    ]

    captcha = None
    """ The captcha """

    def load_plugin(self):
        colony.base.system.Plugin.load_plugin(self)
        import captcha.system
        self.captcha = captcha.system.Captcha(self)

    def generate_captcha(self, string_value, properties):
        return self.captcha.generate_captcha(string_value, properties)

    def generate_captcha_string_value(self, properties):
        return self.captcha.generate_captcha_string_value(properties)
