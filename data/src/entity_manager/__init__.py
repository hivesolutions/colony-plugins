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
from . import benchmark
from . import decorators
from . import exceptions
from . import migration
from . import structures
from . import system
from . import test

from .analysis import EntityManagerAnalyzer
from .benchmark import run_benchmarks, print_report
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
from .migration import (
    has_table,
    index_query,
    insert_ignore_query,
    get_hierarchy_classes,
    get_root_class,
    get_column_definitions,
    get_source_table_for_column,
    backup_database,
    validate_hierarchy,
    validate_data,
    generate_cti_to_concrete_queries,
    generate_concrete_to_cti_queries,
    migrate,
)
from .structures import Connection, EntityClass, rset, load_serializers
from .system import DataEntityManager
from .test import EntityManagerTest, EntityManagerBaseTestCase
