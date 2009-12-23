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

__revision__ = "$LastChangedRevision: 421 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2008-11-20 15:16:53 +0000 (Qui, 20 Nov 2008) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

DEFAULT_NUMBER_RECORDS = 30
""" The default number records """

class WebDatabaseAdministration:
    """
    The web database administration class.
    """

    web_database_administration_plugin = None
    """ The web database administration plugin """

    entity_manager = None
    """ The entity manager reference """

    def __init__(self, web_database_administration_plugin):
        """
        Constructor of the class.

        @type web_database_administration_plugin: WebDatabaseAdministrationPlugin
        @param web_database_administration_plugin: The web database administration plugin.
        """

        self.web_database_administration_plugin = web_database_administration_plugin

    def get_routes(self):
        pass

    def handle_rest_request(self, rest_request):
        # retrieves the entity manager
        entity_manager = self._get_entity_manager()

        # retrieves the request
        request = rest_request.request

        # retrieves the rest path list
        rest_path_list = rest_request.rest_path_list

        # retrieves the rest path list length
        rest_path_list_length = len(rest_request.rest_path_list)

        # retrieves the entity name
        entity_name = rest_request.rest_path_list[0]

        # creates the filter fields list
        filter_fields_list = []

        # in case the rest path list length is two
        if rest_path_list_length == 2:
            # retrieves the entity id
            entity_id = rest_path_list[1]

            # creates the filter field
            filter_field = {"field_name" : "object_id", "field_value" : entity_id}

            # adds the filter field to the filter fields list
            filter_fields_list.append(filter_field)

        # treats the entity name
        entity_name_treated = entity_name.capitalize()[:-1]

        # retrieves the entity class
        entity_class = entity_manager.get_entity_class(entity_name_treated)

        for attribute_name in request.attributes_map:
            # retrieves the attribute value from the attributes map
            attribute_value = request.attributes_map[attribute_name]

            # creates the filter field
            filter_field = {"field_name" : attribute_name, "field_value" : attribute_value}

            # adds the filter field to the filter fields list
            filter_fields_list.append(filter_field)

        if filter_fields_list:
            # creates the filter map
            filter = {"filter_type" : "equals", "filter_fields" : filter_fields_list}
        else:
            # sets the filter as none
            filter = None

        # creates the options map
        options_map = {}

        # in case the filter is defined
        if filter:
            # sets the filters in the options map
            options_map["filters"] = [filter]

        # sets the number of records in the options map
        options_map["number_records"] = DEFAULT_NUMBER_RECORDS

        # retrieves the entity objects for the given filter
        entity_objects = entity_manager._find_all_options(entity_class, options_map)

        # retrieves the rest encoder plugins
        rest_encoder_plugins = rest_request.rest_encoder_plugins

        # in case the encoder name is defined
        if rest_request.encoder_name:
            # iterates over all the rest encoder plugins
            for rest_encoder_plugin in rest_encoder_plugins:
                if rest_encoder_plugin.get_encoder_name() == rest_request.encoder_name:
                    # retrieves the content type from the rest encoder plugin
                    content_type = rest_encoder_plugin.get_content_type()

                    # calls the the encoder plugin to encode the result
                    result_encoded = rest_encoder_plugin.encode_value(entity_objects)
        else:
            # sets the default content type
            content_type = "text/plain"

            # retrieves the result encoded with the default encoder
            result_encoded = str(entity_objects)

        # sets the content type for the rest request
        rest_request.content_type = content_type

        # sets the content type for the rest request
        rest_request.result_translated = result_encoded

        # flushes the rest request
        rest_request.flush()

        return True

    def _get_entity_manager(self):
        """
        Retrieves the entity manager, loading it if necessary.

        @rtype: EntityManager
        @return: The entity manager.
        """

        # in case the entity manager is not defined
        if not self.entity_manager:
            # retrieves the resource manager plugin
            resource_manager_plugin = self.web_database_administration_plugin.resource_manager_plugin

            # retrieves the business entity manager plugin
            business_entity_manager_plugin = self.web_database_administration_plugin.business_entity_manager_plugin

            # retrieves the user home path resource
            user_home_path_resource = resource_manager_plugin.get_resource("system.path.user_home")

            # retrieves the user home path value
            user_home_path = user_home_path_resource.data

            # retrieves the database file name resource
            database_file_name_resource = resource_manager_plugin.get_resource("system.database.file_name")

            # retrieves the database file name
            database_file_name = database_file_name_resource.data

            # creates a new entity manager with the sqlite engine
            self.entity_manager = business_entity_manager_plugin.load_entity_manager("sqlite")

            # sets the connection parameters for the entity manager
            self.entity_manager.set_connection_parameters({"file_path" : user_home_path + "/" + database_file_name, "autocommit" : False})

            # loads the entity manager
            self.entity_manager.load_entity_manager()

        # returns the entity manager
        return self.entity_manager
