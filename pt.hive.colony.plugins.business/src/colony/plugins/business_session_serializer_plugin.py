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

__author__ = "João Magalhães <joamag@hive.pt>"
""" The author(s) of the module """

__version__ = "1.0.0"
""" The version of the module """

__revision__ = "$LastChangedRevision: 684 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2008-12-08 15:16:55 +0000 (seg, 08 Dez 2008) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import colony.base.plugin_system
import colony.base.decorators

class BusinessSessionSerializerPlugin(colony.base.plugin_system.Plugin):
    """
    The main class for the Business Session Serializer plugin.
    """

    id = "pt.hive.colony.plugins.business.session_serializer"
    name = "Business Session Serializer Plugin"
    short_name = "Business Session Serializer"
    description = "Business Session Serializer Plugin"
    version = "1.0.0"
    author = "Hive Solutions Lda. <development@hive.pt>"
    loading_type = colony.base.plugin_system.EAGER_LOADING_TYPE
    platforms = [
        colony.base.plugin_system.CPYTHON_ENVIRONMENT
    ]
    attributes = {
        "build_automation_file_path" : "$base{plugin_directory}/business/session_serializer/resources/baf.xml"
    }
    capabilities = [
        "business_session_serializer",
        "rpc_service",
        "build_automation_item"
    ]
    main_modules = [
        "business.session_serializer.business_session_serializer_exceptions",
        "business.session_serializer.business_session_serializer_system"
    ]

    business_session_serializer = None
    """ The business session serializer """

    @colony.base.decorators.load_plugin()
    def load_plugin(self):
        colony.base.plugin_system.Plugin.load_plugin(self)
        import business.session_serializer.business_session_serializer_system
        self.business_session_serializer = business.session_serializer.business_session_serializer_system.BusinessSessionSerializer(self)

    def end_load_plugin(self):
        colony.base.plugin_system.Plugin.end_load_plugin(self)

    def unload_plugin(self):
        colony.base.plugin_system.Plugin.unload_plugin(self)

    def end_unload_plugin(self):
        colony.base.plugin_system.Plugin.end_unload_plugin(self)

    def load_allowed(self, plugin, capability):
        colony.base.plugin_system.Plugin.load_allowed(self, plugin, capability)

    def unload_allowed(self, plugin, capability):
        colony.base.plugin_system.Plugin.unload_allowed(self, plugin, capability)

    def dependency_injected(self, plugin):
        colony.base.plugin_system.Plugin.dependency_injected(self, plugin)

    @colony.base.decorators.plugin_call(True)
    def add_session_proxy(self, session_proxy, replace_proxy):
        self.business_session_serializer.add_session_proxy(session_proxy, replace_proxy)

    @colony.base.decorators.plugin_call(True)
    def remove_session_proxy(self, session_proxy):
        self.business_session_serializer.remove_session_proxy(session_proxy)

    @colony.base.decorators.plugin_call(True)
    def get_service_id(self):
        return self.business_session_serializer.get_service_id()

    @colony.base.decorators.plugin_call(True)
    def get_service_alias(self):
        return self.business_session_serializer.get_service_alias()

    @colony.base.decorators.plugin_call(True)
    def get_available_rpc_methods(self):
        return self.business_session_serializer.get_available_rpc_methods()

    @colony.base.decorators.plugin_call(True)
    def get_rpc_methods_alias(self):
        return self.business_session_serializer.get_rpc_methods_alias()

    @colony.base.decorators.plugin_meta_information("rpc_method", {"alias" : []})
    def create_persistent_session(self, session_information):
        return self.business_session_serializer.create_persistent_session(session_information)

    @colony.base.decorators.plugin_meta_information("rpc_method", {"alias" : []})
    def get_session_methods(self, session_information):
        return self.business_session_serializer.get_session_methods(session_information)

    @colony.base.decorators.plugin_meta_information("rpc_method", {"alias" : []})
    def update_session_information(self, session_information):
        return self.business_session_serializer.update_session_information(session_information)

    @colony.base.decorators.plugin_meta_information("rpc_method", {"alias" : []})
    def flush_session_information(self, session_information):
        return self.business_session_serializer.flush_session_information(session_information)

    @colony.base.decorators.plugin_meta_information("rpc_method", {"alias" : []})
    def call_session_method(self, session_information, session_entity, session_method, session_method_arguments, session_method_arguments_map):
        return self.business_session_serializer.call_session_method(session_information, session_entity, session_method, session_method_arguments, session_method_arguments_map)
