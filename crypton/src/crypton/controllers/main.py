#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Colony Framework
# Copyright (c) 2008-2023 Hive Solutions Lda.
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

__copyright__ = "Copyright (c) 2008-2023 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "Apache License, Version 2.0"
""" The license for the module """

import colony

from .base import BaseController

DEFAULT_ALGORITHM_NAME = "sha1"
""" The default algorithm name """

models = colony.__import__("models")


class MainController(BaseController):
    def encrypt(self, request):
        signature_controller = self.system.signature_controller
        api_key = request.form("api_key", None)
        key_name = request.form("key_name", required=True)
        message = request.form("message", required=True)
        message_e = signature_controller.encrypt(request, api_key, key_name, message)
        self.set_contents(request, message_e, "text/plain")

    def decrypt(self, request):
        signature_controller = self.system.signature_controller
        api_key = request.form("api_key", None)
        key_name = request.form("key_name", required=True)
        message_e = request.form("message_e", required=True)
        message = signature_controller.decrypt(request, api_key, key_name, message_e)
        self.set_contents(request, message, "text/plain")

    def sign(self, request):
        signature_controller = self.system.signature_controller
        api_key = request.form("api_key", None)
        key_name = request.form("key_name", required=True)
        message = request.form("message", required=True)
        algorithm_name = request.form("algorithm_name", DEFAULT_ALGORITHM_NAME)
        signature = signature_controller.sign(
            request, api_key, key_name, message, algorithm_name
        )
        self.set_contents(request, signature, "text/plain")

    def verify(self, request):
        signature_controller = self.system.signature_controller
        api_key = request.form("api_key", None)
        key_name = request.form("key_name", required=True)
        signature = request.form("signature", required=True)
        message = request.form("message", required=True)
        result = signature_controller.verify(
            request, api_key, key_name, signature, message
        )
        self.set_contents(request, result, "text/plain")
