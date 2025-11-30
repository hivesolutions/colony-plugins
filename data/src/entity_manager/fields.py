#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Colony Framework
# Copyright (c) 2008-2024 Hive Solutions Lda.
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

__copyright__ = "Copyright (c) 2008-2024 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "Apache License, Version 2.0"
""" The license for the module """


class Field(object):
    """
    Descriptor-based field definition for entity attributes.

    This provides a more modern alternative to dict-based field definitions,
    with better IDE support, validation, and cleaner syntax.

    Usage:
        class Person(EntityClass):
            name = Field("text", nullable=False)
            age = Field("integer", indexed=True)
    """

    def __init__(
        self,
        field_type,
        nullable=True,
        indexed=False,
        unique=False,
        default=None,
        validator=None,
        **kwargs
    ):
        """
        Constructor for the Field descriptor.

        :type field_type: String
        :param field_type: The type of the field (text, integer, float, etc.)
        :type nullable: bool
        :param nullable: Whether the field can be null.
        :type indexed: bool
        :param indexed: Whether to create an index on this field.
        :type unique: bool
        :param unique: Whether values must be unique.
        :type default: object
        :param default: Default value for the field.
        :type validator: callable
        :param validator: Function to validate field values.
        """
        self.field_type = field_type
        self.nullable = nullable
        self.indexed = indexed
        self.unique = unique
        self.default = default
        self.validator = validator
        self.extra = kwargs
        self.name = None  # Set by __set_name__

    def __set_name__(self, owner, name):
        """
        Called when the descriptor is assigned to a class attribute.
        This is a Python 3.6+ feature.
        """
        self.name = name

    def __get__(self, instance, owner):
        """
        Descriptor getter - returns the field value from instance.__dict__.
        If called on the class (instance is None), returns the descriptor itself.
        """
        if instance is None:
            return self
        return instance.__dict__.get(self.name)

    def __set__(self, instance, value):
        """
        Descriptor setter - validates and stores the value in instance.__dict__.
        """
        # Validate nullable constraint
        if value is None and not self.nullable:
            raise ValueError("Field '%s' cannot be None" % self.name)

        # Run custom validator if provided
        if self.validator and value is not None:
            if not self.validator(value):
                raise ValueError(
                    "Validation failed for field '%s' with value: %s"
                    % (self.name, value)
                )

        # Store the value
        instance.__dict__[self.name] = value

    def to_dict(self):
        """
        Converts the field descriptor to the legacy dict format
        for backward compatibility with existing code.

        :rtype: dict
        :return: Dictionary representation of the field.
        """
        result = {"type": self.field_type}

        if not self.nullable:
            result["mandatory"] = True
        if self.indexed:
            result["indexed"] = True
        if self.unique:
            result["unique"] = True
        if self.default is not None:
            result["default"] = self.default

        # Include any extra kwargs
        result.update(self.extra)

        return result


class IdField(Field):
    """
    Specialized field for primary key identifiers.

    Usage:
        class Person(EntityClass):
            object_id = IdField(generated=True)
    """

    def __init__(self, generated=False, generator_type=None, **kwargs):
        """
        Constructor for ID field.

        :type generated: bool
        :param generated: Whether the ID is auto-generated.
        :type generator_type: String
        :param generator_type: Type of generator (e.g., "table").
        """
        kwargs["id"] = True
        if generated:
            kwargs["generated"] = generated
        if generator_type:
            kwargs["generator_type"] = generator_type

        super(IdField, self).__init__("integer", nullable=False, **kwargs)


class TextField(Field):
    """
    Text field - maps to VARCHAR or TEXT columns.

    Usage:
        class Person(EntityClass):
            name = TextField(max_length=255)
            description = TextField()  # Unlimited length
    """

    def __init__(self, max_length=None, **kwargs):
        if max_length:
            kwargs["max_length"] = max_length
        super(TextField, self).__init__("text", **kwargs)


class IntegerField(Field):
    """
    Integer field - maps to INTEGER columns.

    Usage:
        class Person(EntityClass):
            age = IntegerField(min_value=0, max_value=150)
    """

    def __init__(self, min_value=None, max_value=None, **kwargs):
        self.min_value = min_value
        self.max_value = max_value

        # Add validation
        def validate_range(value):
            if min_value is not None and value < min_value:
                return False
            if max_value is not None and value > max_value:
                return False
            return True

        if min_value is not None or max_value is not None:
            existing_validator = kwargs.get("validator")
            if existing_validator:
                kwargs["validator"] = lambda v: existing_validator(
                    v
                ) and validate_range(v)
            else:
                kwargs["validator"] = validate_range

        super(IntegerField, self).__init__("integer", **kwargs)


class FloatField(Field):
    """
    Float/decimal field - maps to DOUBLE PRECISION columns.

    Usage:
        class Person(EntityClass):
            weight = FloatField()
            height = FloatField(min_value=0.0)
    """

    def __init__(self, min_value=None, max_value=None, **kwargs):
        super(FloatField, self).__init__("float", **kwargs)


class DateField(Field):
    """
    Date field - maps to date storage (Unix timestamp in Colony).

    Usage:
        class Person(EntityClass):
            birth_date = DateField()
    """

    def __init__(self, **kwargs):
        super(DateField, self).__init__("date", **kwargs)


class MetadataField(Field):
    """
    Metadata field - stores JSON-serializable data structures.

    Usage:
        class Person(EntityClass):
            metadata = MetadataField()
    """

    def __init__(self, **kwargs):
        super(MetadataField, self).__init__("metadata", **kwargs)


class EmbeddedField(object):
    """
    Embedded component field - flattens a component class's fields
    into the parent table with an optional prefix.

    Usage:
        class Address(Component):
            street = TextField()
            city = TextField()

        class Person(EntityClass):
            home_address = EmbeddedField(Address, prefix="home_")
            work_address = EmbeddedField(Address, prefix="work_")

    This creates columns: home_street, home_city, work_street, work_city
    """

    def __init__(self, component_class, prefix=""):
        """
        Constructor for embedded field.

        :type component_class: Class
        :param component_class: The component class to embed.
        :type prefix: String
        :param prefix: Prefix to add to all embedded column names.
        """
        self.component_class = component_class
        self.prefix = prefix
        self.name = None

    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, instance, owner):
        if instance is None:
            return self

        # Lazily create component instance from flattened attributes
        if self.name not in instance.__dict__:
            component = self.component_class()
            for field_name in self._get_component_fields():
                column_name = self.prefix + field_name
                if hasattr(instance, column_name):
                    setattr(component, field_name, getattr(instance, column_name))
            instance.__dict__[self.name] = component

        return instance.__dict__[self.name]

    def __set__(self, instance, value):
        # When setting the component, flatten it to individual attributes
        if value is None:
            instance.__dict__[self.name] = None
            return

        for field_name in self._get_component_fields():
            column_name = self.prefix + field_name
            field_value = getattr(value, field_name, None)
            setattr(instance, column_name, field_value)

        instance.__dict__[self.name] = value

    def _get_component_fields(self):
        """Returns list of field names in the component class."""
        fields = []
        for attr_name in dir(self.component_class):
            attr = getattr(self.component_class, attr_name)
            if isinstance(attr, Field):
                fields.append(attr_name)
        return fields

    def get_columns(self):
        """
        Returns a dictionary mapping column names to field definitions.
        Used during schema generation.

        :rtype: dict
        :return: Map of column_name -> field_dict
        """
        columns = {}
        for attr_name in dir(self.component_class):
            attr = getattr(self.component_class, attr_name)
            if isinstance(attr, Field):
                column_name = self.prefix + attr_name
                columns[column_name] = attr.to_dict()
        return columns


class RelationField(object):
    """
    Descriptor-based relation field definition.

    This provides a more modern alternative to static methods for relations,
    with better IDE support and validation.

    Usage:
        class Person(EntityClass):
            dogs = RelationField("to-many", "Dog", reverse="owner")
            parent = RelationField("to-one", "Person", reverse="children", is_mapper=True)
    """

    def __init__(
        self, relation_type, target, reverse=None, is_mapper=False, lazy=True, **kwargs
    ):
        """
        Constructor for relation field.

        :type relation_type: String
        :param relation_type: Type of relation ("to-one" or "to-many")
        :type target: String or Class
        :param target: Target entity class or class name
        :type reverse: String
        :param reverse: Name of the reverse relation
        :type is_mapper: bool
        :param is_mapper: Whether this side owns the foreign key
        :type lazy: bool
        :param lazy: Whether to use lazy loading
        """
        self.relation_type = relation_type
        self.target = target
        self.reverse = reverse
        self.is_mapper = is_mapper
        self.lazy = lazy
        self.extra = kwargs
        self.name = None

    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, instance, owner):
        if instance is None:
            return self
        # Delegate to entity's lazy loading mechanism
        return instance.__getattribute__(self.name)

    def __set__(self, instance, value):
        instance.__dict__[self.name] = value

    def to_dict(self):
        """
        Converts to legacy relation definition format.

        :rtype: dict
        :return: Relation definition dictionary
        """
        result = {"type": self.relation_type}

        # Handle target - can be string or class
        if isinstance(self.target, str):
            # Will be resolved later by entity manager
            result["target_name"] = self.target
        else:
            result["target"] = self.target

        if self.reverse:
            result["reverse"] = self.reverse
        if self.is_mapper:
            result["is_mapper"] = True
        if not self.lazy:
            result["fetch_type"] = "eager"

        result.update(self.extra)
        return result
