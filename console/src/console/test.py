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

from . import system

class ConsoleTestCase(colony.ColonyTestCase):
    """
    The console test case class.
    """

    last_output = None
    """ The last output value """

    def setUp(self):
        self.console = system.Console(ConsoleTestCase.plugin)

    def test_invalid_command(self):
        """
        Tests and invalid command of the console.
        """

        # process the invalid command line
        return_value = self.console.process_command_line("invalid_command", self.output_method)

        # asserts the echo value
        self.assertEqual(self.last_output, system.INVALID_COMMAND_MESSAGE)

        # assets the return value
        self.assertEqual(return_value, False)

    def output_method(self, text, new_line = True):
        self.last_output = text
