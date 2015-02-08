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
    
    def __init__(self, entity_manager):
        self.entity_manager = entity_manager
        
    def analyse_all(self):
        entities_map = self.entity_manager.entities_map
        for entity_class in colony.legacy.itervalues(entities_map):
            self.analyse_entity(entity_class)
    
    def analyse_entity(self, entity_class):
        self.indirect_relations(entity_class)
    
    def indirect_relations(self, entity_class):
        indirect_relations = entity_class.get_indirect_relations_map()
        
        for tobias, rabeton in indirect_relations.items():
            print(tobias)
            print(rabeton)
        
        
        
        
        
        
