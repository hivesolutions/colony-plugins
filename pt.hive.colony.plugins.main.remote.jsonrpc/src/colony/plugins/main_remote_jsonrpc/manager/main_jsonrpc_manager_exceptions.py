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

__revision__ = "$LastChangedRevision: 2120 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2008-10-21 16:01:47 +0100 (Ter, 21 Out 2008) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

class ServiceException(Exception):
    pass

class ServiceRequestNotTranslatable(ServiceException):
    pass

class BadServiceRequest(ServiceException):
    pass

class InvalidNumberArguments(BadServiceRequest):

    def __init__(self, message):
        BadServiceRequest.__init__(self)
        self.message = message

    def __str__(self):
       return "Invalid number of arguments: %s" % self.message

class InvalidMethod(BadServiceRequest):

    def __init__(self, message):
        BadServiceRequest.__init__(self)
        self.message = message

    def __str__(self):
       return "Invalid Method: %s" % self.message

class JSONEncodeException(Exception):

    def __init__(self, obj):
        Exception.__init__(self)
        self.obj = obj

    def __str__(self):
       return "Object not encodeable: %s" % self.obj

class JSONDecodeException(Exception):

    def __init__(self, message):
        Exception.__init__(self)
        self.message = message

    def __str__(self):
       return self.message
