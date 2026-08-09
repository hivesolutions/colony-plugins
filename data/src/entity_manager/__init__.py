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

__copyright__ = "Copyright (c) 2008-2024 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "Apache License, Version 2.0"
""" The license for the module """

from . import analysis
from . import decorators
from . import exceptions
from . import structures
from . import system
from . import test
from . import mapping_strategies
from . import fields
from . import inheritance_strategies
from . import lazy_collections
from . import query_builder

from .analysis import EntityManagerAnalyzer
from .decorators import transaction, lock_table
from .exceptions import (
    EntityManagerException,
    RuntimeError,
    EntityManagerEngineNotFound,
    MissingRelationMethod,
    ValidationError,
    RelationValidationError,
    InvalidSerializerError,
)
from .structures import Connection, EntityClass, rset, load_serializers
from .system import DataEntityManager
from .test import EntityManagerTest, EntityManagerBaseTestCase
from .mapping_strategies import (
    MappingStrategy,
    DefaultMappingStrategy,
    ConventionOverConfigurationStrategy,
    AnnotationBasedStrategy,
)
from .fields import (
    Field,
    IdField,
    TextField,
    IntegerField,
    FloatField,
    DateField,
    MetadataField,
    EmbeddedField,
    RelationField,
)
from .inheritance_strategies import (
    InheritanceStrategy,
    JoinedTableStrategy,
    SingleTableStrategy,
    TablePerClassStrategy,
    get_inheritance_strategy,
)
from .lazy_collections import LazyCollection, BatchLoader, LazyProxy
from .query_builder import QueryBuilder, Q
