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

__revision__ = "$LastChangedRevision: 2100 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2008-10-21 13:24:05 +0100 (Ter, 21 Out 2008) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import sys
import copy
import string
import os
import sqlalchemy
import sqlalchemy.orm as orm
import sqlalchemy.ext.declarative as declarative

#@todo: review and comment this file
class Domain:
    """
    Defines the object relational model classes that interface with the output databsae
    """
    
    lists = []
    """ List with the references to the entity list of each class defined in this domain """
    
    class_name_map = {}
    """ Dictionary relating classes with their names """
    
    name_class_map = {}
    """ Dictionary relating class names with class definitions """

    def __init__(self, base):
        """
        Class constructors
        
        @param base: Base object inherited by all ORM classes 
        """
        self.lists = []
        globals()["Base"] = base
     
    def add_domain_entity_instance(self, domain_entity_name, domain_entity_instance):
        """
        Adds a domain entity instance to its respective domain entity list
        
        @param domain_entity_name: Name of the domain entity
        @param domain_entity_instance: The domain entity instance
        """
        domain_entity_list = getattr(self, domain_entity_name + "_list")
        domain_entity_list.append(domain_entity_instance)

    def define_classes(self, domain_entities):
        """
        Defines the object relation model classes on the fly by using the output configuration
        
        @param domain_entities: List of domain entities defined in the output configuration
        """
        
        # load the class template from a file to a string
        unchanged_class = open(os.path.join(os.path.dirname(__file__), "unchanged_class"), "r")        
        class_string = ""
        line = unchanged_class.readline()
        class_string = line
        while not line == "":
            line = unchanged_class.readline()
            class_string += line
        
        # for each domain entity defined in the output configuration
        # create a correspondent ORM class by filling out the missing
        # information in the class template, and declaring the class
        # on-the-fly
        for domain_entity in domain_entities:
            class_name = domain_entity.name
            class_string_copy = copy.deepcopy(class_string)
            class_string_copy = self.define_class(domain_entity, class_string)
            for domain_entity in domain_entities:
                field = "@" + domain_entity.name + "_table"
                class_string_copy = string.replace(class_string_copy, field, domain_entity.table)
            exec class_string_copy in globals()
            self.class_name_map[globals()[class_name]] = class_name
            self.name_class_map[class_name] = globals()[class_name]
            list_name = class_name + "_list"
            setattr(self, list_name, [])
            self.lists.append(getattr(self, list_name))
        
        # define the classes relations in a method so they can be setup later                        
        for domain_entity in domain_entities:
            self.define_class_relations(domain_entity)
                
    def define_class(self, domain_entity, class_string):
        """
        Fills out the class template with the class information defined by the output configuration
        
        @param domain_entity: Domain entity object from the output adapter configuration
        @param class_string: Template class definition that needs to be filled out
        @return: Returns the filled out class definition
        """
        class_name = domain_entity.name
        table_name = domain_entity.table
        inherited_class_name = None
        if domain_entity.parent:
            inherited_class_name = domain_entity.parent
            parent_class_name_same_other = domain_entity.parent
            parent_class_name_none_other = domain_entity.parent
        else:
            parent_class_name_same_other = class_name
            parent_class_name_none_other = "None"
        
        if inherited_class_name == None:
            inherited_class_name = "Base"

            if domain_entity.has_children():
                class_string = string.replace(class_string, "@discriminator", 'discriminator = declarative.Column("discriminator", sqlalchemy.String(31))\n')
                class_string = string.replace(class_string, "@mapper_args", '__mapper_args__ = {"polymorphic_on" : discriminator, "polymorphic_identity" : "'+string.lower(class_name)+'"}\n')

        else:           
            class_string = string.replace(class_string, "@mapper_args", '__mapper_args__ = {"polymorphic_identity" : "' + string.lower(class_name) + '"}')
            
        class_string = string.replace(class_string, "@discriminator", "")
        class_string = string.replace(class_string, "@mapper_args", "")
        class_string = string.replace(class_string, "@inherited_class_name", inherited_class_name)
        class_string = string.replace(class_string, "@class_name", class_name)
        class_string = string.replace(class_string, "@table_name", table_name)
        class_string = string.replace(class_string, "@parent_class_name_same_other", parent_class_name_same_other)
        class_string = string.replace(class_string, "@parent_class_name_none_other", parent_class_name_none_other)
        class_string = string.replace(class_string, "@attribute_list", self.define_class_attributes(domain_entity))
        return class_string
    
    def define_class_attributes(self, domain_entity):
        """
        Returns a string with the attribute list to fill in the class template
        
        @param domain_entity: Domain entity object from the output adapter configuration
        @return: A string with the attribute list to fill in the class template
        """
        domain_attribute_list = domain_entity.get_domain_attribute_list()
        attributes = ""
        for domain_attribute in domain_attribute_list:
                attribute_name = domain_attribute.name
                if domain_attribute.referenced_domain_entity:
                    name = string.lower(domain_attribute.referenced_domain_entity.name)
                    attributes += "    " + name + ' = None\n';
                    if not attribute_name == "id":
                        attribute_name += "_id"
                
                attribute = '    @attribute_name = declarative.Column("@attribute_name", sqlalchemy.@variable_type'
                attribute = string.replace(attribute, "@attribute_name", attribute_name)
                attribute = string.replace(attribute, "@variable_type", domain_attribute.type)
                if domain_attribute.referenced_domain_entity:
                    attribute += ', sqlalchemy.ForeignKey("@'+domain_attribute.referenced_domain_entity.name+'_table.id")';
                if domain_attribute.primary_key:
                    attribute += ', primary_key = True'
                attribute += ")"
                attributes += attribute
                attributes += "\n"
        return attributes
        
    def define_class_relations(self, domain_entity):
        """
        Sets the class relations (meant to be invoked after all classes have been defined)
        
        @param domain_entity: Domain entity object from the output adapter configuration
        """
        domain_attribute_list = domain_entity.get_domain_attribute_list()
        for domain_attribute in domain_attribute_list:
            if domain_attribute.referenced_domain_entity:
                name = domain_attribute.referenced_domain_entity.name
                referenced_domain_entity_class = globals()[name]
                domain_entity_class = globals()[domain_entity.name]
                if not domain_attribute.referenced_domain_entity.name == domain_entity.parent:
                    field = getattr(domain_entity_class, string.lower(name) + "_id")
                    setattr(globals()[domain_entity.name], string.lower(name), orm.relation(referenced_domain_entity_class, primaryjoin = field == referenced_domain_entity_class.id))
     
    def get_class(self, class_name):
        """
        Returns the a class definition by providing the class's name
        
        @param class_name: Class name
        @return: Class definition
        """
        return self.name_class_map[class_name]
    
    def get_class_name(self, class_definition):
        """
        Returns a class's name by providing it's definition
        
        @param class_definition: Class definition
        @return: Class name
        """
        return self.class_name_map[class_definition]
        
    def print_domain(self):
        """
        Prints out the contents of every ORM class instance
        """
        for entity_list in lists:
            print "---------------- %s -----------------" % entity_list.__name__
            for entity in entity_list:
                self.print_entity(entity)
                
    def print_entity(entity_object):
        """
        Prints the contents of a given domain entity instance
        
        @param entity_object: The domain entity instance whose contents should be printed
        """
        print entity_object.__class__.__name__
        list_all = dir(entity_object)
        list_exclusion = [ attribute for attribute in list_all if not attribute in entity_object.exclusion_list ]
        for attribute in list_exclusion:
            attribute_value = getattr(entity_object, attribute)
            print "\t %s = %s\n" % (attribute, attribute_value)
