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

__author__ = "João Magalhães <joamag@hive.pt>"
""" The author(s) of the module """

__version__ = "1.0.0"
""" The version of the module """

__revision__ = "$LastChangedRevision: 72 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2008-10-21 23:29:54 +0100 (Ter, 21 Out 2008) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

class VisitorNode(object):
    """
    The visitor node.
    """

    def __init__(self):
        pass

    def accept(self, visitor):
        """
        Accepts the visitor running the iteration logic.

        @type visitor: Visitor
        @param visitor: The visitor object.
        """

        visitor.visit(self)

    def accept_post_order(self, visitor):
        """
        Accepts the visitor running the iteration logic, in post order.

        @type visitor: Visitor
        @param visitor: The visitor object.
        """

        visitor.visit(self)

class Query(VisitorNode):
    """
    The query class.
    """

    def __init__(self):
        """
        Constructor of the class.
        """

        VisitorNode.__init__(self)

class SelectQuery(Query):
    """
    The select query.
    """

    select_fields = []
    """ The select fields to be used """

    select_entities = []
    """ The select entities to be used """

    select_filters = []
    """ The select fielters to be used """

    def __init__(self):
        """
        Constructor of the class.
        """

        Query.__init__(self)

        self.select_fields = []
        self.select_entities = []
        self.select_filters = []

    def add_select_field(self, select_field):
        self.select_fields.append(select_field)

    def add_select_entity(self, select_entity):
        self.select_entities.append(select_entity)

    def add_select_filters(self, select_filter):
        self.select_filters.append(select_filter)

    def accept(self, visitor):
        """
        Accepts the visitor running the iteration logic.

        @type visitor: Visitor
        @param visitor: The visitor object.
        """

        visitor.visit(self)

        if visitor.visit_childs:
            for select_field in self.select_fields:
                select_field.accept(visitor)

            for select_entity in self.select_entities:
                select_entity.accept(visitor)

            for select_filter in self.select_filters:
                select_filter.accept(visitor)

    def accept_post_order(self, visitor):
        """
        Accepts the visitor running the iteration logic, in post order.

        @type visitor: Visitor
        @param visitor: The visitor object.
        """

        if visitor.visit_childs:
            for select_field in self.select_fields:
                select_field.accept_post_order(visitor)

            for select_entity in self.select_entities:
                select_entity.accept_post_order(visitor)

            for select_filter in self.select_filters:
                select_filter.accept_post_order(visitor)

        visitor.visit(self)

class Field(VisitorNode):
    """
    The field class.
    """

    def __init__(self):
        VisitorNode.__init__(self)

class SimpleField(Field):
    """
    The simple field class.
    """

    field_name = "none"
    """ The field name """

    def __init__(self):
        Field.__init__(self)

class Entity(VisitorNode):
    """
    The entity class.
    """

    def __init__(self):
        """
        Constructor of the class.
        """

        VisitorNode.__init__(self)

class SimpleEntity(Entity):
    """
    The simple entity class.
    """

    entity_name = "none"
    """ The entity name """

    def __init__(self):
        """
        Constructor of the class.
        """

        Entity.__init__(self)

class Filter(VisitorNode):
    """
    The filter class.
    """

    def __init__(self):
        """
        Constructor of the class.
        """

        VisitorNode.__init__(self)

class BinaryTermFilter(Filter):
    """
    The binary term filter class.
    """

    first_operand = None
    second_operand = None

    def __init__(self):
        """
        Constructor of the class.
        """

        Filter.__init__(self)

    def accept(self, visitor):
        """
        Accepts the visitor running the iteration logic.

        @type visitor: Visitor
        @param visitor: The visitor object.
        """

        visitor.visit(self)
        visitor.visit(self.first_operand)
        visitor.visit(self.second_operand)

    def accept_post_order(self, visitor):
        """
        Accepts the visitor running the iteration logic, in post order.

        @type visitor: Visitor
        @param visitor: The visitor object.
        """

        visitor.visit(self.first_operand)
        visitor.visit(self.second_operand)

        visitor.visit(self)

class BooleanTermFilter(BinaryTermFilter):
    """
    The boolean term filter class.
    """

    def __init__(self):
        """
        Constructor of the class.
        """

        BinaryTermFilter.__init__(self)

class EqualTermFilter(BooleanTermFilter):
    """
    The equal term filter class.
    """

    def __init__(self):
        """
        Constructor of the class.
        """

        BooleanTermFilter.__init__(self)

class GreaterTermFilter(BooleanTermFilter):
    """
    The greater term filter class.
    """

    def __init__(self):
        """
        Constructor of the class.
        """

        BooleanTermFilter.__init__(self)

class UnaryTermFilter(Filter):
    """
    The unary term filter class.
    """

    operand = None

    def __init__(self):
        """
        Constructor of the class.
        """

        Filter.__init__(self)

class NotTermFilter(UnaryTermFilter):
    """
    The not term filter class.
    """

    def __init__(self):
        """
        Constructor of the class.
        """

        UnaryTermFilter.__init__(self)

class FieldReference(VisitorNode):
    """
    The field reference class.
    """

    def __init__(self):
        """
        Constructor of the class.
        """

        VisitorNode.__init__(self)

class SimpleFieldReference(FieldReference):
    """
    The simple field reference class.
    """

    field_name = "none"

    def __init__(self):
        """
        Constructor of the class.
        """

        FieldReference.__init__(self)

class Value(VisitorNode):

    value = None
    """ The value """

    def __init__(self):
        """
        Constructor of the class.
        """

        VisitorNode.__init__(self)
