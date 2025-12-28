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
__copyright__ = "Copyright (c) 2008-2024 Hive Solutions Lda."
__license__ = "Apache License, Version 2.0"

import base64


class MockPlugin(object):
    def __init__(self):
        self.mvc_utils_plugin = None
        self.ssl_plugin = None
        self.manager = None


class MockConfigurationProperty(object):
    def __init__(self, data):
        self._data = data

    def get_data(self):
        return self._data


class MockController(object):
    def __init__(self, name):
        self.name = name


class MockSSLStructure(object):
    def encrypt_base_64(self, key_path, data):
        if isinstance(data, bytes):
            return base64.b64encode(b"encrypted:" + data).decode("utf-8")
        return base64.b64encode(b"encrypted:" + data.encode("utf-8")).decode("utf-8")

    def decrypt_base_64(self, key_path, data):
        decoded = base64.b64decode(data)
        if decoded.startswith(b"encrypted:"):
            return decoded[10:]
        return decoded

    def sign_base_64(self, key_path, algorithm, data):
        if isinstance(data, bytes):
            return base64.b64encode(b"sig:" + algorithm.encode() + b":" + data).decode(
                "utf-8"
            )
        return base64.b64encode(
            b"sig:" + algorithm.encode() + b":" + data.encode("utf-8")
        ).decode("utf-8")

    def verify_base_64(self, key_path, signature, data):
        try:
            decoded = base64.b64decode(signature)
            return decoded.startswith(b"sig:")
        except Exception:
            return False

    def generate_keys(self, private_path, public_path, number_bits=1024):
        pass
