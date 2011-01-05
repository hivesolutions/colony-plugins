#!/usr/bin/python
# -*- coding: Cp1252 -*-

# Pecway Payment Gateway
# Copyright (C) 2010 Hive Solutions Lda.
#
# This file is part of Pecway Payment Gateway.
#
# Pecway Payment Gateway is confidential and property of Hive Solutions Lda.,
# its usage is constrained by the terms of the Hive Solutions
# Confidential Usage License.
#
# Pecway Payment Gateway should not be distributed under any circumstances,
# violation of this may imply legal action.
#
# If you have any questions regarding the terms of this license please
# refer to <http://www.hive.pt/licenses/>.

__author__ = "João Magalhães <joamag@hive.pt> & Tiago Silva <tsilva@hive.pt>"
""" The author(s) of the module """

__version__ = "1.0.0"
""" The version of the module """

__revision__ = "$LastChangedRevision: 421 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2008-11-20 15:16:53 +0000 (Qui, 20 Nov 2008) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2010 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "Hive Solutions Confidential Usage License (HSCUL)"
""" The license for the module """

import colony.libs.importer_util

BASE_ENTITY_MODULE_VALUE = "base_entity"
""" The base entity module value """

# imports the base entity classes
base_entity = colony.libs.importer_util.__importer__(BASE_ENTITY_MODULE_VALUE)

class RootEntity(base_entity.EntityClass):
    """
    The root entity class, inherited by other entities
    in order for them to have a global unique identifier.
    """

    object_id = {"id" : True, "data_type" : "numeric", "generated" : True, "generator_type" : "table", "table_generator_field_name" : "RootEntity"}
    """ The object id of the comment """

    def __init__(self):
        """
        Constructor of the class.
        """

        self.object_id = None

class Consumer(RootEntity):
    """
    The consumer class, which represents a generic
    consumer client with an api key.
    """

    name = {"data_type" : "text"}
    """ The consumers's name """

    api_key = {"data_type" : "text"}
    """ The consumers's value """

    status = {"data_type" : "numeric"}
    """ The consumers's status (1 - active, 2 - inactive) """

    def __init__(self):
        """
        Constructor of the class.
        """

        RootEntity.__init__(self)
        self.name = None
        self.api_key = None
        self.status = None

    def set_validation(self):
        """
        Sets the validation structures for the
        current structure.
        """

        # validates that a non empty name was set
        self.add_validation_method("name", "not_empty", {})

        # validates that a non empty api key was set
        self.add_validation_method("api_key", "not_empty", {})

        # validates that an status greater than zero was set
        self.add_validation_method("status", "greater_than_zero", {})
