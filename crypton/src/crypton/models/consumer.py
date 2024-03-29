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

from .crypton_root import CryptonRoot

CryptonRoot = CryptonRoot


class Consumer(CryptonRoot):
    """
    The consumer class, which represents a generic
    consumer client with an API key.
    """

    STATUS_ACTIVE = 1
    """ The consumer status active """

    STATUS_INACTIVE = 2
    """ The consumer status inactive """

    STATUS_ENUM = (STATUS_ACTIVE, STATUS_INACTIVE)
    """ The status enumeration """

    name = dict(type="text", mandatory=True, secure=True)
    """ The consumers's name """

    api_key = dict(type="text", mandatory=True, secure=True)
    """ The consumers's value """

    status = dict(type="integer", mandatory=True, secure=True)
    """ The consumers's status (1 - active, 2 - inactive) """

    def __init__(self):
        """
        Constructor of the class, should set the initial and
        default values for a typical consumer.
        """

        CryptonRoot.__init__(self)
        self.name = None
        self.api_key = None
        self.status = Consumer.STATUS_INACTIVE

    def set_validation(self):
        """
        Sets the validation structures for the
        current structure.
        """

        # adds the inherited validations
        CryptonRoot.set_validation(self)

        # adds the validation methods to the name attribute
        self.add_validation("name", "not_none", True)
        self.add_validation("name", "not_empty")

        # adds the validation methods to the API key attribute
        self.add_validation("api_key", "not_none", True)
        self.add_validation("api_key", "not_empty")

        # adds the validation methods to the status attribute
        self.add_validation("status", "not_none", True)
        self.add_validation("status", "in_enumeration", values=Consumer.STATUS_ENUM)

    def _generate_api_key(self):
        # retrieves the random plugin
        random_plugin = self.crypton_plugin.random_plugin

        # generates a random string value for
        # the API key
        api_key = random_plugin.generate_random_sha256_string()

        # returns the (generated) API key
        return api_key
