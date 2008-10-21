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

class OutputConfiguration:
    """ 
    Stores the information defined by the output configuration file and provides an easy way to retrieve it. 
    """
    
    domain_entity_map = {} 
    """ Dictionary relating domain entity names with DomainEntity objects. """
        
    def __init__(self):
        self.domain_entity_map = {}
        
    def add_domain_entity(self, domain_entity):
        """
        Adds a domain entity object to this output configuration.
        
        @param domain_entity: DomainEntity object to add to the configuration.
        """
        self.domain_entity_map[domain_entity.get_name()] = domain_entity
        self.flag_children_bearing_domain_entities()
    
    def get_domain_entity_name(self, internal_entity_name):
        """
        Gets an internal entity name's correspondent domain entity name.
        
        @param internal_entity_name: Name of the internal entity for which one wants the correspondent domain entity's name.
        @return: String indicating the name of the correspondent domain entity.
        """ 
        for key in self.domain_entity_map:
            if self.domain_entity_map[key].get_internal_entity_name() == internal_entity_name:
                return self.domain_entity_map[key].get_domain_entity_name()
    
    def get_domain_entity_list(self):
        """
        Returns a list of domain entity objects with the ones without a parent in the first positions.
        
        @return: List of DomainEntity objects.
        """
        domain_entity_list = self.domain_entity_map.values()
        sorted_entity_list = []
        for domain_entity in domain_entity_list:
            if domain_entity.parent == None:
                sorted_entity_list.append(domain_entity)
                domain_entity_list.remove(domain_entity)
        for domain_entity in domain_entity_list:
            sorted_entity_list.append(domain_entity)
        return sorted_entity_list
    
    def get_domain_entity_handler_list(self, domain_entity_name):
        """
        Gets a domain entity's list of handler functions.
        
        @param domain_entity_name: Name of the domain entity for which one wants the correspondent handler functions.
        @return: List with handler function references.
        """
        return self.domain_entity_map[domain_entity_name].get_handler_list()
    
    def add_domain_entity_handler(self, domain_entity_name, handler):
        """
        Adds an handler function to a certain domain entity.
        
        @param domain_entity_name: Name of the domain entity to which one wants to add an handler function.
        @param handler: Handler function reference to add to the domain entity.
        """
        self.domain_entity_map[domain_entity_name].add_handler(handler)
        
    def add_domain_attribute_handler(self, domain_entity_name, domain_attribute_name, exception_handler):
        """
        Adds an handler function to a certain domain entity attribute.
        
        @param domain_entity_name: Name of the domain entity that contains the targeted domain entity attribute.
        @param domain_attribute_name: Name of the domain attribute to which one wants to add an handler function.
        @param handler: Handler function reference to add to the domain attribute.
        """
        self.domain_entity_map[domain_entity_name].add_domain_attribute_handler(domain_attribute_name, exception_handler)
    
    def get_parent_domain_entity_name_list(self, domain_entity_name):
        """
        Gets a list with the name of provided domain entity and of all it's parents.
        
        @param domain_entity_name: Name of the domain entity for which one wants a full hierarchy list.
        @return: List of strings with the names of all the domain entities in the provided domain entity's inheritance hierarchy.
        """
        domain_entity_name_list = [domain_entity_name]
        while self.domain_entity_map[domain_entity_name].get_parent_domain_entity_name():
            domain_entity_name = self.domain_entity_map[domain_entity_name].get_parent_domain_entity_name()
            domain_entity_name_list.append(domain_entity_name)
        return domain_entity_name_list
        
    def get_parent_domain_attribute_map(self, domain_entity_name):
        """
        Gets a map with the attributes of the specified domain entity as well with all it's inherited ones.
        
        @param domain_entity_name: Name of the domain entity for which one wants a full domain attribute map.
        @return: Dictionary in the following format: {domain attribute name -> domain attribute}. 
        """
        domain_entity_name_list = self.get_parent_domain_entity_name_list(domain_entity_name)
        parent_domain_attribute_map = {}
        for domain_entity_name in domain_entity_name_list:
            domain_attribute_list = self.domain_entity_map[domain_entity_name].get_domain_attribute_list()
            for domain_attribute in domain_attribute_list:
                parent_domain_attribute_map[domain_attribute.get_name()] = domain_attribute
        return parent_domain_attribute_map
    
    def get_internal_entity_name(self, domain_entity_name):
        """
        Gets an domain entity name's correspondent internal entity name.
        
        @param domain_entity_name: Name of the internal entity for which one wants the correspondent internal entity's name.
        @return: String indicating the name of the correspondent internal entity.
        """ 
        return self.domain_entity_map[domain_entity_name].get_internal_entity_name()
            
    def get_internal_attribute_name(self, domain_entity_name, domain_attribute_name):
        """
        Retrieves the name of the internal attribute associated with the provided domain attribute name.
        
        @param domain_entity_name: Name of the domain entity to which domain_attribute_name parameter belongs to.
        @param domain_attribute_name: Name of the domain entity attribute for which one wants the correspondent internal attribute name.
        @return: String with the name of the internal attribute that corresponds to the provided domain entity attribute.
        """
        domain_entity_name_list = self.get_parent_domain_entity_name_list(domain_entity_name)
        for domain_entity_name in domain_entity_name_list:
            internal_attribute_name = self.domain_entity_map[domain_entity_name].get_internal_attribute_name(domain_attribute_name)
            if internal_attribute_name:
                return internal_attribute_name
            
    def get_referenced_domain_entity_name(self, domain_entity_name, domain_attribute_name):
        """
        Retrieves the name of the domain entity that the provided domain attribute references.

        @param domain_entity_name: Name of the domain entity to which domain_attribute_name parameter belongs to.
        @param domain_attribute_name: Name of the domain entity attribute for which one wants the references domain entity's name.
        @return: String with the name of the domain entity referenced by the provided domain attribute.
        """
        domain_attribute_map = self.get_parent_domain_attribute_map(domain_entity_name)
        return domain_attribute_map[domain_attribute_name].get_referenced_domain_entity_name()

    def get_reference_multiplicity(self, domain_entity_name, domain_attribute_name):
        """
        Returns the multiplicity of the reference held by a specified domain entity attribute.
        
        @param domain_entity_name: Name of the domain entity to which domain_attribute_name parameter belongs to.
        @param domain_attribute_name: Name of the domain entity attribute for which one wants it's reference multiplicity.
        @return: String indicating the multiplicity of the relation (one-to-one, one-to-many, many-to-many), None in case it is a normal attribute.
        """
        domain_attribute_map = self.get_parent_domain_attribute_map(domain_entity_name)
        return domain_attribute_map[domain_attribute_name].get_reference_multiplicity()

    def get_domain_attribute_handler_list(self, domain_entity_name, domain_attribute_name):
        """
        Retrieves a list of handler functions for the specified domain entity attribute.
        
        @param domain_entity_name: Name of the domain entity to which domain_attribute_name parameter belongs to.
        @param domain_attribute_name: Name of the domain entity attribute for which one wants it's list of handler functions.
        @return: List of handler function references.
        """
        domain_attribute_map = self.get_parent_domain_attribute_map(domain_entity_name)
        return domain_attribute_map[domain_attribute_name].get_handler_list()
    
    def get_domain_attribute_name_list(self, domain_entity_name):
        """
        Retrieves a list with the names of the domain attributes that belong to the specified domain entity and all the domain entities it inherits.
        
        @param domain_entity_name: Name of the domain entity for which one wants a full list of domain attributes.
        @return: List of domain entity attribute names.
        """
        domain_attribute_map = self.get_parent_domain_attribute_map(domain_entity_name)
        return domain_attribute_map.keys()
    
    def get_domain_relation_attribute_name_list(self, domain_entity_name):
        """
        Retrieves a list with the names of the relation attributes that belong to the specified domain entity and all the domain entities it inherits.
        
        @param domain_entity_name: Name of the domain entity for which one wants a full list of domain attributes that hold references to other domain entities.
        @return: List of domain entity attribute names.
        """
        domain_attribute_map = self.get_parent_domain_attribute_map(domain_entity_name)
        return [key for key in domain_attribute_map if domain_attribute_map[key].is_domain_relation_attribute()]
    
    def get_domain_exception_attribute_name_list(self, domain_entity_name):
        """
        Retrieves a list with the names of the exception attributes that belong to the specified domain entity and all the domain entities it inherits.
        
        @param domain_entity_name: Name of the domain entity for which one wants a full list of domain attributes that hold references to other domain entities.
        @return: List of domain entity attribute names.
        """
        domain_attribute_map = self.get_parent_domain_attribute_map(domain_entity_name)
        return [key for key in domain_attribute_map if domain_attribute_map[key].is_domain_exception_attribute()]
    
    def is_domain_relation_attribute(self, domain_entity_name, domain_attribute_name):
        """
        Indicates if the specified domain attribute holds a reference to another domain entity.
        
        @param domain_entity_name: Name of the domain entity to which domain_attribute_name parameter belongs to.
        @param domain_attribute_name: Name of the domain entity attribute one wants to figure out if it holds a reference. 
        @return: Boolean indicating if this is a relation attribute.
        """
        domain_attribute_map = self.get_parent_domain_attribute_map(domain_entity_name)
        return domain_attribute_map[domain_attribute_name].is_domain_relation_attribute()
    
    def flag_children_bearing_domain_entities(self):
        """
        Marks all the domain entities that are inherited by others as having children.
        """
        for domain_entity in self.domain_entity_map.values():
            for domain_entity2 in self.domain_entity_map.values():
                if domain_entity.get_parent_domain_entity_name() == domain_entity2.get_name():
                    domain_entity2.children = True
        
class DomainEntity:
    """
    Stores information about a domain entity and how it should be treated
    """
    
    name = None
    """ Name of the domain entity """

    table = None
    """ Name of the table this domain entity corresponds to in the database """
    
    internal_entity = None
    """ Name of the correspondent internal entity """
    
    parent = None
    """ Name of the parent domain entity, in case this one inherits another """
    
    domain_attribute_map = {}
    """ Dictionary relating domain entity attribute names with Attribute objects """
    
    handler_list = []
    """ List of handlers to process when before this domain entity is processed """
    
    children = False
    """ Flag indicating if this domain entity is inherited by others """
    
    def __init__(self):
        self.domain_attribute_map = {}
        self.handler_list = []
    
    def add_handler(self, handler):
        """
        Adds an handler function to this domain entity.
        
        @param handler: Handler function to add to this domain entity.
        """
        self.handler_list.append(handler)
            
    def add_domain_attribute(self, domain_attribute):
        """
        Adds a domain entity attribute to this domain entity.
        
        @param domain_attribute: DomainEntityAttribute object to add to this domain entity.
        """
        self.domain_attribute_map[domain_attribute.get_name()] = domain_attribute
        
    def add_domain_attribute_handler(self, domain_attribute_name, handler):
        """
        Adds an handler function to a specified domain entity attribute.
        
        @param domain_attribute_name: Name of the domain entity attribute one wants to add an handler function to.
        @param handler: Handler function to add to this domain entity attribute.
        """
        self.domain_attribute_map[domain_attribute_name].add_handler(handler)

    def get_parent_domain_entity_name(self):
        """
        Returns the name of the parent domain entity.
        
        @return: String with the name of the parent domain entity, or None if it has no parent.
        """
        return self.parent
    
    def get_domain_attribute_list(self):
        """
        Returns a list of domain entity attributes that belong to this domain entity.
        
        @return: List of DomainEntityAttribute objects.
        """
        return self.domain_attribute_map.values()
    
    def get_name(self):
        """
        Returns the name of this domain entity.
        
        @return: String with the name of this domain entity.
        """
        return self.name
    
    def get_internal_entity_name(self):
        """
        Returns the name of the internal entity that corresponds to this domain entity.
        
        @return: String with the name of the correspondent internal entity.
        """
        return self.internal_entity
    
    def get_handler_list(self):
        """
        Retrieves the list of handler functions for this domain entity.
        
        @return: List of handler function references.
        """
        return self.handler_list
        
    def get_domain_attribute_name_list(self):
        """
        Retrieves a list with the names of the attributes that belong to this domain entity.
        
        @return: List of strings with the names of this domain entity's attributes.
        """
        return self.domain_attribute_map.keys()
    
    def get_domain_attribute_handler_list(self, domain_attribute_name):
        """
        Retrieves a list of handler functions associated with the provided domain entity attribute.
        
        @param domain_attribute_name: Name of the domain entity attribute for which one wants its handler functions.
        @return: List of handler functions references.
        """
        if domain_attribute_name in self.domain_attribute_map:
            return self.domain_attribute_map[domain_attribute_name].get_handler_list()     
    
    def get_internal_attribute_name(self, domain_attribute_name):
        """
        Retrieves the name of the correspondent attribute in the internal structure.
        
        @param domain_attribute_name: Name of the domain entity attribute for which one wants the correspondent internal entity attribute.
        @return: String with the name of the correspondent attribute in the internal structure. 
        """
        if domain_attribute_name in self.domain_attribute_map:
            return self.domain_attribute_map[domain_attribute_name].get_internal_attribute_name()
    
    def get_referenced_domain_entity_name(self, domain_attribute_name):
        """
        Retrieves the name of the referenced domain entity, in case this is a attribute holds a reference.
        
        @param domain_attribute_name: Name of the domain entity attribute for which one wants the referenced domain entity name.
        @return: Name of the referenced domain entity, or None in case this is a normal attribute.
        """
        if domain_attribute_name in self.domain_attribute_map:
            return self.domain_attribute_map[domain_attribute_name].get_referenced_domain_entity_name()
    
    def get_reference_multiplicity(self, domain_attribute_name):
        """
        Indicates the multiplicity of the specified domain entity attribute's reference in case it is a relation attribute.
        
        @return: String indicating the multiplicity of the relation (one-to-one, one-to-many, many-to-many), None in case it is a normal attribute.
        """
        if domain_attribute_name in self.domain_attribute_map:
            return self.domain_attribute_map[domain_attribute_name].get_reference_multiplicity()
    
    def is_domain_relation_attribute(self, domain_attribute_name):
        """
        Indicates if the specified domain entity attribute holds a reference to another domain entity.
        
        @param domain_attribute_name: Name of the domain entity attribute one wants to know if it holds a relation.
        @return: Boolean indicating if it is a relation attribute or not.
        """
        domain_relation_attribute_list = self.get_domain_relation_attribute_name_list()
        return domain_attribute_name in domain_relation_attribute_list
    
    def has_children(self):
        """
        Indicates if this domain entity has others that inherit its properties.
        
        @return: Boolean indicating if this domain entity is parent to other domain entities.
        """
        return self.children
        
    def __repr__(self):
        """
        Prints out a string representation of this object when it is used as a parameter for the print() function,
        or returns this string representation if the method itself is invoked.
        
        @return: String representation of this object.
        """ 
        return_string = ""
        return_string += "name = %s\n" % self.name
        return_string += "internal_entity = %s\n" % self.internal_entity       
        for handler in self.handlers:
            return_string += "<handler>"
            return_string += handler.__repr__()
            return_string += "<\\handler>\n"   
        for attribute in self.attributes:
            return_string += "<attribute>"
            return_string += attribute.__repr__()
            return_string += "<\\attribute>\n"
        return return_string

class DomainEntityAttribute:
    """
    Stores information about a domain entity attribute and how it should be treated.
    """
    
    name = None
    """ Name of the domain entity attribute. """
    
    internal_attribute = None
    """ Name of the internal entity attribute name correspondent to this domain entity attribute. """
    
    referenced_domain_entity = None
    """ Name of the referenced domain entity (in case this attribute is a foreign key). """
    
    type = None
    """ Type of variable stored by this attribute. """
    
    primary_key = False
    """ Indicates if this attribute is part of a primary key. """
    
    handler_list = []
    """ List of handler functions to be invoked for this domain entity attribute. """
    
    def __init__(self):
        self.handler_list = []
        
    def add_handler(self, handler):
        """
        Adds an handler function to this domain entity attribute.
        
        @param handler: Handler function reference to add to this domain entity attribute.
        """
        self.handler_list.append(handler)
    
    def get_reference_multiplicity(self):
        """
        Returns the multiplicity of the reference held by a specified domain entity attribute.
        
        @return: String indicating the multiplicity of the relation (one-to-one, one-to-many, many-to-many), None in case it is a normal attribute.
        """
        if self.referenced_domain_entity:
            return self.referenced_domain_entity.get_reference_multiplicity()
        
    def get_handler_list(self):
        """
        Retrieves a list of handler functions associated with this domain entity attribute.
        
        @return: List of handler functions references.
        """
        return self.handler_list
    
    def get_referenced_domain_entity_name(self):
        """
        Retrieves the name of the referenced domain entity, in case this is a attribute holds a reference.
        
        @return: Name of the referenced domain entity, or None in case this is a normal attribute.
        """
        if self.referenced_domain_entity:
            return self.referenced_domain_entity.get_name()
    
    def get_name(self):
        """
        Retrieves the name of this domain entity attribute.
        
        @return: String with the name of this domain entity attribute.
        """
        return self.name
    
    def get_internal_attribute_name(self):
        """
        Retrieves the name of the correspondent attribute in the internal structure.
        
        @return: String with the name of the correspondent attribute in the internal structure. 
        """
        return self.internal_attribute
    
    def is_domain_relation_attribute(self):
        """
        Indicates if this domain entity attribute holds a reference to another domain entity.
        
        @return: Boolean indicating if it is a relation attribute or not.
        """
        return not self.referenced_domain_entity == None
        
    def __repr__(self):
        """
        Prints out a string representation of this object when it is used as a parameter for the print() function,
        or returns this string representation if the method itself is invoked.
        
        @return: String representation of this object.
        """ 
        return_string = ""
        return_string += "\tname = %s\n" % self.name
        return_string += "\tinternal_attribute = %s\n" % self.internal_attribute
        return_string += "\t<referenced_domain_entity>"
        return_string += self.referenced_domain_entity.__repr__()
        return_string += "\t</referenced_domain_entity>\n"
        for handler in self.handlers:
            return_string += "<handler>"
            return_string += handler.__repr__()
            return_string += "<\\handler>\n"   
        return return_string
    
class ReferencedDomainEntity:
    """
    Stores information about an entity relationship.
    """
    
    name = None
    """ Name of the referenced domain entity. """
    
    multiplicity = None
    """ Multiplicity of the relationship (one-to-one, one-to-many, many-to-many). """
    
    def get_name(self):
        """
        Retrieves the name of this referenced domain entity.
        
        @return: String with the name of this referenced domain entity.
        """
        return self.name
    
    def get_reference_multiplicity(self):
        """
        Retrieves the multiplicity of the relation established with this referenced domain entity.
        
        @return: String defining the type of relationship (one-to-one, one-to-many, many-to-many).
        """
        return self.multiplicity
    
    def __repr__(self):
        """
        Prints out a string representation of this object when it is used as a parameter for the print() function,
        or returns this string representation if the method itself is invoked.
        
        @return: String representation of this object.
        """ 
        return_string = ""
        return_string += "\t\tname = %s\n" % self.name
        return_string += "\t\tmultiplicity = %s\n" % self.multiplicity
        return return_string
    
class Handler:
    """
    Represents an handler function, which can be added to either a DomainEntity or a DomainEntityAttribute.
    """
    
    name = None
    """ Name of the handler function. """
    
    def __repr__(self):
        """
        Prints out a string representation of this object when it is used as a parameter for the print() function,
        or returns this string representation if the method itself is invoked.
        
        @return: String representation of this object.
        """ 
        return_string = ""
        return_string += "\tname = %s\n" % self.name
        return return_string