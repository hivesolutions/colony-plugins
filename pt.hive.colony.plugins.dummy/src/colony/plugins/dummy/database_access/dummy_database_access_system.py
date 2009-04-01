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

__revision__ = "$LastChangedRevision$"
""" The revision number of the module """

__date__ = "$LastChangedDate$"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import sqlalchemy
import sqlalchemy.ext.declarative

Base = sqlalchemy.ext.declarative.declarative_base()

class DummyDatabaseAccess:

    dummy_database_access_plugin = None

    def __init__(self, dummy_database_access_plugin):
        self.dummy_database_access_plugin = dummy_database_access_plugin

    def get_all_entity_names(self):
        return ["user"]

    def get_entity_by_entity_name(self, entity_name):
        if entity_name == "user":
            return User

class User(Base):

    __tablename__ = "users"

    user_id = sqlalchemy.Column("user_id", sqlalchemy.Integer, primary_key = True)
    username = sqlalchemy.Column("username", sqlalchemy.String)
    password = None
    password_md5 = None
    secret_question = None
    secret_answer = None
    tip = None

    def __init__(self, user_id = None, username = None, password = None, password_md5 = None, secret_question = None, secret_answer = None, tip = None):
        self.user_id = user_id
        self.username = username
        self.password = password
        self.password_md5 = password_md5
        self.secret_question = secret_question
        self.secret_answer = secret_answer
        self.tip = tip
