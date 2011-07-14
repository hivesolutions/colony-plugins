#!/usr/bin/python
# -*- coding: utf-8 -*-

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

__revision__ = "$LastChangedRevision: 7681 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2010-03-24 18:27:03 +0000 (qua, 24 Mar 2010) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import os

class BusinessDummyEntityBundle:
    """
    The business dummy entity bundle class
    """

    business_dummy_entity_bundle_plugin = None
    """ The business dummy entity bundle plugin """

    entity_bundle = []
    """ The bundle containing the entity classes """

    entity_bundle_map = {}
    """ The map associating the entity classes with their names """

    def __init__(self, business_dummy_entity_bundle_plugin):
        """
        Constructor of the class

        @type business_dummy_entity_bundle_plugin: BusinessDummyEntityBundlePlugin
        @param business_dummy_entity_bundle_plugin: The business dummy entity bundle plugin
        """

        self.business_dummy_entity_bundle_plugin = business_dummy_entity_bundle_plugin

        self.entity_bundle = []
        self.entity_bundle_map = {}

    def generate_classes(self):
        # retrieves the business helper plugin
        business_helper_plugin = self.business_dummy_entity_bundle_plugin.business_helper_plugin

        # retrieves the base directory name
        base_directory_name = self.get_path_directory_name()

        # imports the class module
        business_dummy_entity_bundle_classes = business_helper_plugin.import_class_module_target("business_dummy_entity_bundle_classes", globals(), locals(), [], base_directory_name, "business_dummy_entity_bundle_classes")

        # sets the entity bundle
        self.entity_bundle = business_dummy_entity_bundle_classes.ENTITY_CLASSES

        # generates the entity bundle map from the entity bundle
        self.entity_bundle_map = business_helper_plugin.generate_bundle_map(self.entity_bundle)

    def get_entity_bundle(self):
        return self.entity_bundle

    def get_entity_bundle_map(self):
        return self.entity_bundle_map

    def get_path_directory_name(self):
        return os.path.dirname(__file__)
