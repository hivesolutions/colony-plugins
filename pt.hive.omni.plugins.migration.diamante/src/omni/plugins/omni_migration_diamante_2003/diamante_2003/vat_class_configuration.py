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

class VatClassConfiguration:
    """
    Provides the migration configuration necessary to migrate
    omni VatClass entities from diamante.
    """

    omni_migration_diamante_2003_plugin = None
    """ The omni migration diamante 2003 plugin """

    def __init__(self, omni_migration_diamante_2003_plugin):
        self.omni_migration_diamante_2003_plugin = omni_migration_diamante_2003_plugin

    def load_data_converter_configuration(self):
        """
        Loads the data converter configuration.
        """

        # defines how to extract vat class entities from iva entities
        iva_input_entities = {NAME_VALUE : "iva",
                              OUTPUT_ENTITIES_VALUE : [{OUTPUT_ATTRIBUTES_VALUE : [{NAME_VALUE : "start_date",
                                                                                    ATTRIBUTE_NAME_VALUE : "DATA1"},
                                                                                   {NAME_VALUE : "end_date",
                                                                                    ATTRIBUTE_NAME_VALUE : "DATA2"},
                                                                                   {NAME_VALUE : "vat_rate",
                                                                                    ATTRIBUTE_NAME_VALUE : "VALOR2",
                                                                                    HANDLERS_VALUE : [{FUNCTION_VALUE : self.attribute_handler_convert_percentage}]}]}]}

        # defines how to extract vat class entities
        self.attribute_mapping_output_entities = [{NAME_VALUE : "VatClass",
                                                   INPUT_ENTITIES_VALUE : [iva_input_entities]}]

    def attribute_handler_convert_percentage(self, data_converter, input_intermediate_structure, input_entity, output_intermediate_structure, output_entity, output_attribute_value, arguments):
        # converts a diamante percentage to an omni percentage
        output_attribute_value = float(output_attribute_value) / 100

        return output_attribute_value
