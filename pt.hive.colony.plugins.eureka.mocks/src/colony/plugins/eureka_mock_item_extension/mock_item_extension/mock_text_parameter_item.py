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

__author__ = "Luís Martinho <lmartinho@hive.pt>"
""" The author(s) of the module """

__version__ = "1.0.0"
""" The version of the module """

__revision__ = "$LastChangedRevision: 2072 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2008-10-20 12:02:33 +0100 (Mon, 20 Oct 2008) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import eureka_engine.engine.eureka_item

class MockTextParameterItem(eureka_engine.engine.eureka_item.EurekaItem):
    """
    This class is a sample Eureka item of the text parameter type.
    """

    type = "text_parameter"
    """ TextParameter type Eureka Item are used to represented textual parameters entered by the user. """

    key = "mock_text_parameter"
    title = "Mock Text Parameter"
    keywords = ["mock", "text", "parameter"]
