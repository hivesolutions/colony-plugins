#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Colony Framework
# Copyright (c) 2008-2015 Hive Solutions Lda.
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

__copyright__ = "Copyright (c) 2008-2015 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import colony

class EntityManagerAnalyser(object):
    """
    Entity manager analyser class responsible for the
    analysis/verifier/recommendation support of an entity
    manager. Should provide ways to improve performance
    and structure for the data layer.
    """

    plugin = None
    """ The top level plugin that is going to be used as
    the owner for the logger operations, etc. """

    entity_manager = None
    """ The reference to the owner/reference to entity
    manager for which the analyser is going to run """

    def __init__(self, entity_manager):
        self.entity_manager = entity_manager
        self.plugin = entity_manager.entity_manager_plugin

    def analyse_all(self):
        entities_map = self.entity_manager.entities_map
        for entity_class in colony.legacy.itervalues(entities_map):
            self.analyse_entity(entity_class)

    def analyse_entity(self, entity_class):
        self.analyse_definition(entity_class)

    def analyse_definition(self, entity_class):
        # in case the entity class to be created is abstract there is
        # no need to create it (no data source definition required)
        if entity_class.is_abstract(): return
        if self.entity_manager.exists(entity_class): return
        self.plugin.warning("No definition for class '%s' exists" % entity_class.__name__)
