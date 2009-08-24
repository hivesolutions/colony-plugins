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

DIAMANTE_INVOICE_DOCUMENT_TYPE = "FAC"
""" The invoice document type in diamante """

DIAMANTE_RETURN_TO_VENDOR_SLIP_DOCUMENT_TYPE = "DEV"
""" The return to vendor document type in diamante """

DIAMANTE_CONSIGNMENT_SLIP_DOCUMENT_TYPE = "G/C"
""" The consignment slip document type in diamante """

OMNI_DOCUMENT_COMPLETED_STATUS = 2
""" The completed document status indicator in omni """

class ReturnToVendorSlipConfiguration:
    """
    Provides the migration configuration necessary to migrate
    omni ReturnToVendorSlip entities from diamante.
    """

    omni_migration_diamante_2003_plugin = None
    """ The omni migration diamante 2003 plugin """

    def __init__(self, omni_migration_diamante_2003_plugin):
        self.omni_migration_diamante_2003_plugin = omni_migration_diamante_2003_plugin

    def load_data_converter_configuration(self):
        """
        Loads the data converter configuration.
        """

        # defines how to extract return to vendor slip entities from devolver entities
        devolver_input_entities = {NAME_VALUE : "devolver",
                                   OUTPUT_ENTITIES_VALUE : [{VALIDATORS_VALUE : [{FUNCTION_VALUE : self.entity_validator_is_consignment_or_supplier_return,
                                                                                  INPUT_DEPENDENCIES_VALUE : {"devolver" : ["DOCUMENTO"],
                                                                                                              "extrdocc" : ["DOCUMENTO", "DOCVINDODE", "TIPODOC"]}}],
                                                             OUTPUT_ATTRIBUTES_VALUE : [{NAME_VALUE : "identifier",
                                                                                         ATTRIBUTE_NAME_VALUE : "DOCUMENTO"},
                                                                                        {NAME_VALUE : "document_status",
                                                                                         DEFAULT_VALUE_VALUE : OMNI_DOCUMENT_COMPLETED_STATUS}]}]}

        # defines how to extract return to vendor slip entities
        self.attribute_mapping_output_entities = [{NAME_VALUE : "ReturnToVendorSlip",
                                                   INPUT_ENTITIES_VALUE : [devolver_input_entities]}]

    def entity_validator_is_consignment_or_supplier_return(self, data_converter, input_intermediate_structure, input_entity, arguments):
        # indicates if the entity is a consignement or supplier return

        supplier_return = self.entity_validator_is_supplier_return(data_converter, input_intermediate_structure, input_entity, arguments)
        consignment_return = self.entity_validator_is_consignment_return(data_converter, input_intermediate_structure, input_entity, arguments)

        return supplier_return or consignment_return

    def entity_validator_is_supplier_return(self, data_converter, input_intermediate_structure, input_entity, arguments):
        # indicates if the entity represents a supplier return

        documento = input_entity.get_attribute("DOCUMENTO")

        extrdocc_entity_index = (ENTITY_NAME_VALUE, EQUALS_VALUE, "extrdocc",
                                 AND_VALUE, "DOCUMENTO", EQUALS_VALUE, documento,
                                 AND_VALUE, "DOCVINDODE", EQUALS_VALUE, DIAMANTE_INVOICE_DOCUMENT_TYPE,
                                 AND_VALUE, "TIPODOC", EQUALS_VALUE, DIAMANTE_RETURN_TO_VENDOR_SLIP_DOCUMENT_TYPE)

        entities = input_intermediate_structure.get_entities_by_index(extrdocc_entity_index)

        return len(entities) == 1

    def entity_validator_is_consignment_return(self, data_converter, input_intermediate_structure, input_entity, arguments):
        # indicates if the entity represents a consignment return

        documento = input_entity.get_attribute("DOCUMENTO")

        extrdocc_entity_index = (ENTITY_NAME_VALUE, EQUALS_VALUE, "extrdocc",
                                 AND_VALUE, "DOCUMENTO", EQUALS_VALUE, documento,
                                 AND_VALUE, "DOCVINDODE", EQUALS_VALUE, DIAMANTE_CONSIGNMENT_SLIP_DOCUMENT_TYPE,
                                 AND_VALUE, "TIPODOC", EQUALS_VALUE, DIAMANTE_RETURN_TO_VENDOR_SLIP_DOCUMENT_TYPE)

        entities = input_intermediate_structure.get_entities_by_index(extrdocc_entity_index)

        return len(entities) == 1
