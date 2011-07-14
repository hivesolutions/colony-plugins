#!/usr/bin/python
# -*- coding: utf-8 -*-

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

__author__ = "João Magalhães <joamag@hive.pt> & Luís Martinho <lmartinho@hive.pt>"
""" The author(s) of the module """

__version__ = "1.0.0"
""" The version of the module """

__revision__ = "$LastChangedRevision: 72 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2008-10-21 23:29:54 +0100 (Tue, 21 Oct 2008) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

class SearchInterpreter:
    """
    The search interpreter class.
    """

    search_interpreter_plugin = None
    """ The search interpreter plugin """

    def __init__(self, search_interpreter_plugin):
        """
        Constructor of the class.

        @type search_interpreter_plugin: SearchInterpreterPlugin
        @param search_interpreter_plugin: The search interpreter plugin.
        """

        self.search_interpreter_plugin = search_interpreter_plugin

    def process_tokens_list(self, tokens_list, properties):
        search_interpreter_adapter_plugins = self.search_interpreter_plugin.search_interpreter_adapter_plugins

        adapter_type_list = []

        for search_interpreter_adapter_plugin in search_interpreter_adapter_plugins:
            search_interpreter_adapter_plugin.process_tokens_list(tokens_list, properties)

            search_interpreter_adapter_plugin_type = search_interpreter_adapter_plugin.get_type()

            adapter_type_list.append(search_interpreter_adapter_plugin_type)

        return adapter_type_list
