#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Colony Framework
# Copyright (c) 2008-2023 Hive Solutions Lda.
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

__copyright__ = "Copyright (c) 2008-2023 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "Apache License, Version 2.0"
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
        if entity_class.is_abstract(): return
        if not entity_class.is_ready(): return
        if self.entity_manager.exists(entity_class): return
        self.plugin.warning("No definition for class '%s' exists" % entity_class.__name__)
