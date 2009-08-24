#!/usr/bin/python
# -*- coding: Cp1252 -*-

# Hive Omni ERP
# Copyright (C) 2008 Hive Solutions Lda.
#
# This file is part of Hive Omni ERP.
#
# Hive Omni ERP is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Hive Omni ERP is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Hive Omni ERP. If not, see <http://www.gnu.org/licenses/>.

__author__ = "Tiago Silva <tsilva@hive.pt>"
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

import os
import base64
import tempfile

ATTRIBUTES_VALUE = "attributes"

DIRECTORY_PATHS_VALUE = "directory_paths"

ENTITY_NAME_PATH_REGEX_MAP_VALUE = "entity_name_path_regex_map"

FILE_WRITE_BINARY_MODE = "wb"
""" The file write binary mode in python """

IMAGE_WIDTH = 130
""" The image's width """

IMAGE_HEIGHT = 115
""" The imagem's height """

JPEG_MIME_TYPE = "image/jpeg"
""" The mime type for a jpeg file """

DEMO_DATA_DIRECTORY_NAME = "demo_data"
""" Name of the directory where the demo data is located """

COMPANY_IMAGE_FILE_REGEX = ".*company(/|\\\\)([a-zA-Z]|[0-9])+([a-zA-Z]|[0-9]|_)*\.(jpg|JPG|jpeg|JPEG)"
""" Regular expression used to match company image files """

CUSTOMERS_IMAGE_FILE_REGEX = ".*customers(/|\\\\)([a-zA-Z]|[0-9])+([a-zA-Z]|[0-9]|_)*\.(jpg|JPG|jpeg|JPEG)"
""" Regular expression used to match armazens image files """

MERCHANDISE_IMAGE_FILE_REGEX = ".*merchandise(/|\\\\)([a-zA-Z]|[0-9])+([a-zA-Z]|[0-9]|_)*\.(jpg|JPG|jpeg|JPEG)"
""" Regular expression used to match merchandise image files """

IO_ADAPTER_FILESYSTEM_PLUGIN_ID = "pt.hive.colony.plugins.data_converter.io_adapter.filesystem"
""" Unique identifier for the filesystem io adapter plugin """

class MediaConfiguration:
    """
    Provides the migration configuration necessary to migrate
    omni Media entities from diamante.
    """

    omni_migration_demo_data_plugin = None
    """ The omni migration demo data plugin """

    def __init__(self, omni_migration_demo_data_plugin):
        self.omni_migration_demo_data_plugin = omni_migration_demo_data_plugin

    def load_data_converter_configuration(self):
        """
        Loads the data converter configuration.
        """

        # retrieves the demo data path
        resource_manager_plugin = self.omni_migration_demo_data_plugin.resource_manager_plugin
        user_home_path_resource = resource_manager_plugin.get_resource("system.path.user_home")
        user_home_path = user_home_path_resource.data
        demo_data_path = os.path.join(user_home_path, DEMO_DATA_DIRECTORY_NAME)

        # defines how the input adapter should read data from the input source
        self.input_io_adapters_options = [{IO_ADAPTER_PLUGIN_ID_VALUE : IO_ADAPTER_FILESYSTEM_PLUGIN_ID,
                                           DIRECTORY_PATHS_VALUE : [demo_data_path],
                                           ENTITY_NAME_PATH_REGEX_MAP_VALUE : {"DD_Media_Company" : COMPANY_IMAGE_FILE_REGEX,
                                                                               "DD_Media_Customer" : CUSTOMERS_IMAGE_FILE_REGEX,
                                                                               "DD_Media_Merchandise" : MERCHANDISE_IMAGE_FILE_REGEX}}]

        # defines how to extract media entities from dd media company entities
        dd_media_company_input_entities = {NAME_VALUE : "DD_Media_Company",
                                           OUTPUT_ENTITIES_VALUE : [{OUTPUT_ATTRIBUTES_VALUE : [{NAME_VALUE : "base_64_data",
                                                                                                 ATTRIBUTE_NAME_VALUE : "data",
                                                                                                 HANDLERS_VALUE : [{FUNCTION_VALUE : self.attribute_handler_resize_image},
                                                                                                                   {FUNCTION_VALUE : self.attribute_handler_encode_image_base_64}]},
                                                                                                {NAME_VALUE : "label",
                                                                                                 ATTRIBUTE_NAME_VALUE : "name"},
                                                                                                {NAME_VALUE : "mime_type",
                                                                                                 DEFAULT_VALUE_VALUE : JPEG_MIME_TYPE}]}]}

        # defines how to extract media entities from dd media customer entities
        dd_media_customer_input_entities = {NAME_VALUE : "DD_Media_Customer",
                                            OUTPUT_ENTITIES_VALUE : [{OUTPUT_ATTRIBUTES_VALUE : [{NAME_VALUE : "base_64_data",
                                                                                                  ATTRIBUTE_NAME_VALUE : "data",
                                                                                                  HANDLERS_VALUE : [{FUNCTION_VALUE : self.attribute_handler_resize_image},
                                                                                                                    {FUNCTION_VALUE : self.attribute_handler_encode_image_base_64}]},
                                                                                                 {NAME_VALUE : "label",
                                                                                                  ATTRIBUTE_NAME_VALUE : "name"},
                                                                                                 {NAME_VALUE : "mime_type",
                                                                                                  DEFAULT_VALUE_VALUE : JPEG_MIME_TYPE}]}]}
        # defines how to extract media entities from dd media merchandise entities
        dd_media_merchandise_input_entities = {NAME_VALUE : "DD_Media_Merchandise",
                                               OUTPUT_ENTITIES_VALUE : [{OUTPUT_ATTRIBUTES_VALUE : [{NAME_VALUE : "base_64_data",
                                                                                                     ATTRIBUTE_NAME_VALUE : "data",
                                                                                                     HANDLERS_VALUE : [{FUNCTION_VALUE : self.attribute_handler_resize_image},
                                                                                                                       {FUNCTION_VALUE : self.attribute_handler_encode_image_base_64}]},
                                                                                                   {NAME_VALUE : "label",
                                                                                                    ATTRIBUTE_NAME_VALUE : "name"},
                                                                                                   {NAME_VALUE : "mime_type",
                                                                                                    DEFAULT_VALUE_VALUE : JPEG_MIME_TYPE}]}]}

        # defines how to extract media entities
        self.attribute_mapping_output_entities = [{NAME_VALUE : "Media",
                                                   INPUT_ENTITIES_VALUE : [dd_media_company_input_entities,
                                                                           dd_media_customer_input_entities,
                                                                           dd_media_merchandise_input_entities]}]

    def attribute_handler_resize_image(self, data_converter, input_intermediate_structure, input_entity, output_intermediate_structure, output_entity, output_attribute_value, arguments):
        # dumps the file data in a temporary file
        file, file_path = tempfile.mkstemp()
        file = open(file_path, FILE_WRITE_BINARY_MODE)
        file.write(output_attribute_value)
        file.close()

        # resizes the image
        output_attribute_value = self.omni_migration_demo_data_plugin.image_treatment_plugin.resize_image_aspect_background(file_path, IMAGE_WIDTH, IMAGE_HEIGHT).getvalue()

        return output_attribute_value

    def attribute_handler_encode_image_base_64(self, data_converter, input_intermediate_structure, input_entity, output_intermediate_structure, output_entity, output_attribute_value, arguments):
        # converts the image data to base 64
        output_attribute_value = base64.encodestring(output_attribute_value)

        return output_attribute_value
