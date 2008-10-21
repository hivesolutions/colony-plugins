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

__author__ = "Tiago Silva <tsilva@hive.pt>"
""" The author(s) of the module """

__version__ = "1.0.0"
""" The version of the module """

__revision__ = "$LastChangedRevision$"
""" The revision number of the module """

__date__ = "$LastChangedDate$"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

class TextInputOutput:

    entity_class_map = {}
    file = None

    def open_file(self, path):
        self.file = open(path,"w")

    def close_file(self):
        self.file.close()

    def flush(self):
        """
        Flushes all the previous operations down the stream of the I/O plugin
        """
        return self.file.flush()

    #@todo: implement
    def delete(self, object):
        """
        Deletes an object from the datastore
        
        @param object: Entity instance to delete from the datastore
        """
        pass

    def save(self, object):
        """
        Saves an object to the datastore
        
        @param object: Entity instance to save to the datastore
        """
        attributes = dir(object)
        for attribute in attributes:
            if not attribute[0:2] == "__" and not attribute[-2:0] == "__":
                self.file.write(attribute + " = " + str(getattr(object,attribute)) + " ; ")
        self.file.write("\n")

    #@todo: implement
    def query(self, object):
        """
        Returns a set of objects from the datastore
        
        @param object: Entity whose instances one wants to retrieve
        @return: Retrieved entity instances 
        """
        return []

    def bind(self, entity_class_map):
        """
        Sets the information necessary to bind entities to tables and classes
        
        @param entity_class_map: Dictionary associating entities to class references
        """
        self.entity_class_map = entity_class_map
