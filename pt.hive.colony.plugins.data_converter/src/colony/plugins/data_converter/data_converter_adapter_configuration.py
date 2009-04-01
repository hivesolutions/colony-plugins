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

__revision__ = "$LastChangedRevision: 1807 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2009-03-10 11:07:56 +0000 (Tue, 10 Mar 2009) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

class DataConverterAdapterConfiguration:
    """
    Stores the information defined by the input configuration file and provides an easy way to retrieve it.
    """

    domain_entity_name_domain_entity_map = {}
    """ Dictionary relating domain entity name with domain entity object instances """

    def __init__(self):
        """
        Constructor of the class.
        """

        self.domain_entity_name_domain_entity_map = {}

    def add_domain_entity(self, domain_entity):
        """
        Adds a domain entity to the adapter configuration.

        @type domain_entity: DomainEntity
        @param domain_entity: DomainEntity object to add to this configuration.
        """

        self.domain_entity_name_domain_entity_map[domain_entity.name] = domain_entity

    def get_domain_entity(self, domain_entity_name):
        """
        Returns the specified domain entity.

        @type domain_entity_name: String
        @param domain_entity_name: Name of the domain entity one wants to retrieve.
        @rtype: DomainEntity
        @return: The requested domain entity configuration.
        """

        return self.domain_entity_name_domain_entity_map[domain_entity_name]

class DomainEntity:
    """
    Stores information about a domain entity and how it should be treated.
    """

    name = None
    """ Name of the domain entity """

    internal_entity = None
    """ Name of the internal entity this domain entity will be copied into """

    primary_key_domain_attributes = []
    """ Domain attributes that make up this domain entity's primary key """

    foreign_keys = []
    """ This domain entity's foreign keys """

    domain_attribute_name_domain_attribute_map = {}
    """ Dictionary relating domain attribute names with DomainAttribute objects """

    instance_handlers = []
    """ List of handlers to process when an instance of this domain entity is processed """

    global_handlers = []
    """ List of handlers to process when an all instances of this domain entity are processed """

    def __init__(self):
        """
        Constructor of the class.
        """

        self.domain_attribute_name_domain_attribute_map = {}
        self.global_handlers = []
        self.instance_handlers = []
        self.primary_key_domain_attributes = []
        self.foreign_keys = []

    def add_domain_attribute(self, domain_attribute):
        """
        Adds a domain attribute to this domain entity.

        @type domain_attribute: DomainAttribute
        @param domain_attribute: DomainAttribute object to add to this domain entity.
        """

        self.domain_attribute_name_domain_attribute_map[domain_attribute.name] = domain_attribute

    def get_domain_attribute(self, domain_attribute_name):
        """
        Returns a domain attribute.

        @type domain_attribute_name: String
        @return: Domain attribute object belonging to this domain entity.
        """

        return self.domain_attribute_name_domain_attribute_map[domain_attribute_name]

    def get_domain_attributes(self):
        """
        Retrieves a list of this domain entity's attributes.

        @rtype: List
        @return: List of domain attributes.
        """

        return self.domain_attribute_name_domain_attribute_map.values()

    def get_plain_domain_attributes(self):
        """
        Retrieves a list with all the domain attributes belonging to this domain entity
        that are not part of any foreign key.

        @rtype: List
        @return: List of domain attributes.
        """

        domain_attributes = self.get_domain_attributes()

        # remove foreign key domain attributes
        for foreign_key in self.foreign_keys:
            for foreign_key_domain_attribute in foreign_key.domain_attributes:
                if foreign_key_domain_attribute in domain_attributes:
                    domain_attributes.remove(foreign_key_domain_attribute)

        return domain_attributes

class DomainAttribute:
    """
    Represents a domain entity attribute and how it should be treated.
    """

    name = None
    """ Name of the domain entity attribute """

    internal_entity = None
    """ Internal entity this DomainAttribute belongs to, in case it is not the same as the parent domain entity """

    internal_entity_id = None
    """ Internal entity instance this DomainAttribute belongs to, in case it is not the same as the parent domain entity """

    internal_attribute = None
    """ Name of the internal entity attribute to which this DomainAttribute's contents will be copied to """

    handlers = []
    """ List of handler functions """

    def __init__(self):
        self.handlers = []

class ForeignKey:
    """
    Represents a foreign key that can be added to a domain entity object.
    """

    foreign_domain_entity = None
    """ Domain entity this foreign key points to """

    domain_attributes = []
    """ List of domain attributes that make this foreign key """

    def __init__(self):
        self.domain_attributes = []

class Handler:
    """
    Represents an handler function, which can be added to either a DomainEntity or a DomainAttribute object.
    """

    name = None
    """ Name of the handler function """
