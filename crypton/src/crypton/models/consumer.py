#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Colony Framework
# Copyright (C) 2008-2012 Hive Solutions Lda.
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

__author__ = "João Magalhães <joamag@hive.pt> & Tiago Silva <tsilva@hive.pt>"
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

import root_entity

root_entity = root_entity

class Consumer(root_entity.RootEntity):
    """
    The consumer class, which represents a generic
    consumer client with an api key.
    """

    STATUS_ACTIVE = 1
    """ The consumer status active """
    
    STATUS_INACTIVE = 2
    """ The consumer status inactive """
    
    STATUS_ENUM = (
        STATUS_ACTIVE,
        STATUS_INACTIVE
    )
    """ The status enumeration """
    
    name = {
        "data_type" : "text",
        "mandatory" : True,
        "secure" : True
    }
    """ The consumers's name """

    api_key = {
        "data_type" : "text",
        "mandatory" : True,
        "secure" : True
    }
    """ The consumers's value """

    status = {
        "data_type" : "integer",
        "mandatory" : True,
        "secure" : True
    }
    """ The consumers's status (1 - active, 2 - inactive) """

    def __init__(self):
        """
        Constructor of the class.
        """

        root_entity.RootEntity.__init__(self)
        self.name = None
        self.api_key = None
        self.status = Consumer.STATUS_INACTIVE

    def set_validation(self):
        """
        Sets the validation structures for the
        current structure.
        """

        # adds the inherited validations
        root_entity.RootEntity.set_validation(self)

        # adds the validation methods to the name attribute
        self.add_validation_method("name", "not_none", True)
        self.add_validation_method("name", "not_empty")

        # adds the validation methods to the api key attribute
        self.add_validation_method("api_key", "not_none", True)
        self.add_validation_method("api_key", "not_empty")

        # adds the validation methods to the status attribute
        self.add_validation_method("status", "not_none", True)
        self.add_validation_method("status", "in_enumeration", properties = {"values" : Consumer.STATUS_ENUM})

    def _generate_api_key(self):
        # retrieves the random plugin
        random_plugin = self.crypton_plugin.random_plugin

        # generates a random string value for
        # the api key
        api_key = random_plugin.generate_random_sha256_string()

        # returns the (generated) api key
        return api_key
