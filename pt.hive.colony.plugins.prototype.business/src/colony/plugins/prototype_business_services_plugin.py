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

import colony.plugins.plugin_system
import colony.plugins.decorators

class PrototypeBusinessServicesPlugin(colony.plugins.plugin_system.Plugin):
    """
    The main class for the Prototype Business Services plugin
    """

    id = "pt.hive.colony.plugins.prototype.business.services"
    name = "Prototype Business Services Plugin"
    short_name = "Prototype Business Services"
    description = "Prototype Business Services Plugin"
    version = "1.0.0"
    author = "Hive Solutions Lda. <development@hive.pt>"
    loading_type = colony.plugins.plugin_system.EAGER_LOADING_TYPE
    platforms = [colony.plugins.plugin_system.CPYTHON_ENVIRONMENT]
    capabilities = ["rpc_service"]
    capabilities_allowed = []
    dependencies = [colony.plugins.plugin_system.PluginDependency(
                    "pt.hive.colony.plugins.misc.resource_manager", "1.0.0")]
    events_handled = []
    events_registrable = []

    prototype_business_services = None

    resource_manager_plugin = None

    @colony.plugins.decorators.load_plugin("pt.hive.colony.plugins.prototype.business.services", "1.0.0")
    def load_plugin(self):
        colony.plugins.plugin_system.Plugin.load_plugin(self)
        global prototype_business_services
        import prototype_business_services.services.prototype_business_services_system
        self.prototype_business_services = prototype_business_services.services.prototype_business_services_system.PrototypeBusinessServices(self)

    def end_load_plugin(self):
        colony.plugins.plugin_system.Plugin.end_load_plugin(self)
        self.prototype_business_services.create_database()

    def unload_plugin(self):
        colony.plugins.plugin_system.Plugin.unload_plugin(self)

    def end_unload_plugin(self):
        colony.plugins.plugin_system.Plugin.end_unload_plugin(self)    

    def load_allowed(self, plugin, capability):
        colony.plugins.plugin_system.Plugin.load_allowed(self, plugin, capability)

    def unload_allowed(self, plugin, capability):
        colony.plugins.plugin_system.Plugin.unload_allowed(self, plugin, capability)

    @colony.plugins.decorators.inject_dependencies("pt.hive.colony.plugins.prototype.business.services", "1.0.0")
    def dependency_injected(self, plugin):
        colony.plugins.plugin_system.Plugin.dependency_injected(self, plugin)

    @colony.plugins.decorators.plugin_call(True)
    def get_service_id(self):
        return self.prototype_business_services.get_service_id()

    @colony.plugins.decorators.plugin_call(True)
    def get_service_alias(self):
        return self.prototype_business_services.get_service_alias()

    @colony.plugins.decorators.plugin_call(True)
    def get_available_rpc_methods(self):
        return self.prototype_business_services.get_available_rpc_methods()

    @colony.plugins.decorators.plugin_call(True)
    def get_rpc_methods_alias(self):
        return self.prototype_business_services.get_rpc_methods_alias()

    @colony.plugins.decorators.plugin_meta_information("rpc_method", {"alias" : []})
    def create_user(self, username, password, picture_base64):
        return self.prototype_business_services.create_user(username, password, picture_base64)

    @colony.plugins.decorators.plugin_meta_information("rpc_method", {"alias" : []})
    def edit_user(self, username, field_names, field_values):
        return self.prototype_business_services.edit_user(username, field_names, field_values)

    @colony.plugins.decorators.plugin_meta_information("rpc_method", {"alias" : []})
    def remove_user(self, username):
        return self.prototype_business_services.remove_user(username)

    @colony.plugins.decorators.plugin_meta_information("rpc_method", {"alias" : []})
    def get_user(self, username):
        return self.prototype_business_services.get_user(username)

    @colony.plugins.decorators.plugin_meta_information("rpc_method", {"alias" : []})
    def get_all_users(self):
        return self.prototype_business_services.get_all_users()

    @colony.plugins.decorators.plugin_meta_information("rpc_method", {"alias" : []})
    def create_customer(self, name, age, address, gender, picture_base64):
        return self.prototype_business_services.create_customer(name, age, address, gender, picture_base64)

    @colony.plugins.decorators.plugin_meta_information("rpc_method", {"alias" : []})
    def edit_customer(self, name, field_names, field_values):
        return self.prototype_business_services.edit_customer(name, field_names, field_values)

    @colony.plugins.decorators.plugin_meta_information("rpc_method", {"alias" : []})
    def remove_customer(self, name):
        return self.prototype_business_services.remove_customer(name)

    @colony.plugins.decorators.plugin_meta_information("rpc_method", {"alias" : []})
    def get_customer(self, name):
        return self.prototype_business_services.get_customer(name)

    @colony.plugins.decorators.plugin_meta_information("rpc_method", {"alias" : []})
    def get_all_customers(self):
        return self.prototype_business_services.get_all_customers()

    @colony.plugins.decorators.plugin_meta_information("rpc_method", {"alias" : []})
    def create_supplier(self, name, address, picture_base64):
        return self.prototype_business_services.create_supplier(name, address, picture_base64)

    @colony.plugins.decorators.plugin_meta_information("rpc_method", {"alias" : []})
    def edit_supplier(self, name, field_names, field_values):
        return self.prototype_business_services.edit_supplier(name, field_names, field_values)

    @colony.plugins.decorators.plugin_meta_information("rpc_method", {"alias" : []})
    def remove_supplier(self, name):
        return self.prototype_business_services.remove_supplier(name)

    @colony.plugins.decorators.plugin_meta_information("rpc_method", {"alias" : []})
    def get_supplier(self, name):
        return self.prototype_business_services.get_supplier(name)

    @colony.plugins.decorators.plugin_meta_information("rpc_method", {"alias" : []})
    def get_all_suppliers(self):
        return self.prototype_business_services.get_all_suppliers()

    @colony.plugins.decorators.plugin_meta_information("rpc_method", {"alias" : []})
    def create_product(self, id, heading1, heading2, description, weight, height, quantity, picture_base64):
        return self.prototype_business_services.create_product(id, heading1, heading2, description, weight, height, quantity, picture_base64)

    @colony.plugins.decorators.plugin_meta_information("rpc_method", {"alias" : []})
    def edit_product(self, id, field_names, field_values):
        return self.prototype_business_services.edit_product(id, field_names, field_values)

    @colony.plugins.decorators.plugin_meta_information("rpc_method", {"alias" : []})
    def remove_product(self, id):
        return self.prototype_business_services.remove_product(id)

    @colony.plugins.decorators.plugin_meta_information("rpc_method", {"alias" : []})
    def get_product(self, id):
        return self.prototype_business_services.get_product(id)

    @colony.plugins.decorators.plugin_meta_information("rpc_method", {"alias" : []})
    def get_all_products(self):
        return self.prototype_business_services.get_all_products()

    @colony.plugins.decorators.plugin_meta_information("rpc_method", {"alias" : []})
    def create_sale(self, id, payment_type, description, customer_name, product_tuples):
        return self.prototype_business_services.create_sale(id, payment_type, description, customer_name, product_tuples)

    @colony.plugins.decorators.plugin_meta_information("rpc_method", {"alias" : []})
    def get_sale(self, id):
        return self.prototype_business_services.get_sale(id)

    @colony.plugins.decorators.plugin_meta_information("rpc_method", {"alias" : []})
    def get_all_sales(self):
        return self.prototype_business_services.get_all_sales()

    @colony.plugins.decorators.plugin_meta_information("rpc_method", {"alias" : []})
    def create_purchase(self, id, description, supplier_name, product_tuples):
        return self.prototype_business_services.create_purchase(id, description, supplier_name, product_tuples)

    @colony.plugins.decorators.plugin_meta_information("rpc_method", {"alias" : []})
    def get_purchase(self, id):
        return self.prototype_business_services.get_purchase(id)

    @colony.plugins.decorators.plugin_meta_information("rpc_method", {"alias" : []})
    def get_all_purchases(self):
        return self.prototype_business_services.get_all_purchases()

    def get_resource_manager_plugin(self):
        return self.resource_manager_plugin

    @colony.plugins.decorators.plugin_inject("pt.hive.colony.plugins.misc.resource_manager")
    def set_resource_manager_plugin(self, resource_manager_plugin):
        self.resource_manager_plugin = resource_manager_plugin
