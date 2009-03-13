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

import string
import datetime
import os
import stat

class Diamante2003InputAdapterConfiguration:
    """
    Provides a the necessary configuration parameters and functions to convert
    data from the Diamante 2003 version to the intermediate internal structure
    """

    parent_plugin = None
    """ Reference to the plugin that owns this code """

    #@todo: move this to xml file
    work_unit_tables_map = {"customer" : ["empresas", "lojas", "funciona", "vendedor", "password", "zonas", "bancos", "estilo", "pureza", "qualidad", "tipopeca", "coleccao", "tiposerv", "talhe", "tipoprod", "tipopaga", "forneced", "produtos", "imagens", "profissa", "clientes"]}

    """ Dictionary relating work unit name with a list of the database table names that need to be processed for the work unit to be complete """

    def __init__(self, parent_plugin):
        self.parent_plugin = parent_plugin

    def get_work_units(self):
        """
        Gets a list of the work units provided by this configuration plugin
        
        @return: List of strings with the names of the available work units
        """

        return self.work_unit_tables_map.keys()

    def get_tables(self, work_unit_name):
        """
        Gets a list with the names of the tables a certain work unit is meant to process
        
        @param work_unit_name: Name of the work unit one wants to get the respective list of tables from
        @return: List of strings with the tables that belong to the provided work unit
        """

        return self.work_unit_tables_map[work_unit_name] 

    def get_configuration_file_paths(self):
        """
        Returns the path to the configuration file provided by this plugin
        
        @return: String with the full path to the input configuration file
        """

        file_paths = []
        path = os.path.dirname(__file__) + "/xml/"
        dirs = os.listdir(path)
        for fname in dirs:
            full_path = path + fname
            mode = os.stat(full_path)[stat.ST_MODE]
            if not stat.S_ISDIR(mode):
                file_paths.append(full_path)
        return file_paths

    def has_handler(self, handler_name):
        """
        Indicates this configuration plugin has a certain handler function
        
        @param handler_name: Name of the handler function
        @return: Boolean indicating if the requested handler function exists
        """

        if self.get_handler(handler_name) == None:
            return False
        return True

    def get_handler(self, handler_name):
        """
        Returns the requested handler function
        
        @param handler_name: Name of the handler function
        @return: Reference to the requested handler function in case it exists
        """

        return getattr(self, handler_name)

    def column_handler_timestamp_to_datetime(self, arguments):
        """
        Converts a timestamp to a datetime object
        
        @param arguments: List of arguments (1st argument: value to process)
        @return: Returns the processed value
        """

        value = arguments[0]
        
        if value:
            value = datetime.datetime.fromtimestamp(int(value))
        return value

    def column_handler_string_to_lowercase(self, arguments):
        """
        Converts a string to lowercase
        
        @param arguments: List of arguments (1st argument: value to process)
        @return: Returns the processed value
        """

        value = arguments[0]
        
        if value:
            value = string.lower(value)
        return value
    
    def column_handler_diamante_encryption_to_plaintext(self, arguments):
        """
        Decrypts a Diamante 2003 encoded string
        
        @param arguments: List of arguments (1st argument: value to process)
        @return: Returns the processed value
        """

        value = arguments[0]

        if value:
            newstr = ""
            for char in value:
                ascii_value = ord(char)
                decoded_ascii_value = 255 - ascii_value
                decoded_char = chr(decoded_ascii_value)
                newstr += decoded_char
            value = newstr
        return value

    def column_handler_diamante_gender_id_to_hive_gender_id(self, arguments):
        """
        Converts a Diamante 2003 gender enumeration to a Hive gender enumeration
        
        @param arguments: List of arguments (1st argument: value to process)
        @return: Returns the processed value
        """

        value = arguments[0]

        DIAMANTE_GENDER_MALE = "1"
        DIAMANTE_GENDER_FEMALE = "2"
        DIAMANTE_COMPANY = "3"
        HIVE_GENDER_MALE = "0"
        HIVE_GENDER_FEMALE = "1"
        HIVE_COMPANY = "2"

        if value == DIAMANTE_GENDER_MALE:
            return HIVE_GENDER_MALE
        elif value == DIAMANTE_GENDER_FEMALE:
            return HIVE_GENDER_FEMALE
        else:
            return HIVE_COMPANY

    def column_handler_diamante_anulado_to_hive_status(self, arguments):
        """
        Converts a Diamante 2003 status enumeration to a Hive status enumeration
        
        @param arguments: List of arguments (1st argument: value to process)
        @return: Returns the processed value
        """

        value = arguments[0]

        DIAMANTE_ACTIVE1 = ""
        DIAMANTE_ACTIVE2 = "0"
        DIAMANTE_INACTIVE = "1"
        HIVE_ACTIVE = "0"
        HIVE_INACTIVE = "1"
        
        if value == DIAMANTE_ACTIVE1:
            return HIVE_ACTIVE
        elif value == DIAMANTE_ACTIVE2:
            return HIVE_ACTIVE
        elif value == DIAMANTE_INACTIVE:
            return HIVE_INACTIVE

    def column_handler_diamante_paises_to_hive_country(self, arguments):
        """
        Converts a Diamante 2003 country enumeration to a Hive country enumeration
        
        @param arguments: List of arguments (1st argument: value to process)
        @return: Returns the processed value
        """

        value = arguments[0]

        DIAMANTE_PORTUGAL = "01"
        DIAMANTE_ESPANHA = "02"
        DIAMANTE_GRECIA = "03"
        DIAMANTE_HOLANDA = "04"
        DIAMANTE_BELGICA = "05"
        DIAMANTE_FRANCA = "06"
        DIAMANTE_ITALIA = "07"
        DIAMANTE_ALEMANHA = "08"
        DIAMANTE_FINLANDIA = "09"
        DIAMANTE_AUSTRIA = "10"
        
        HIVE_PORTUGAL = "Portugal"
        HIVE_ESPANHA = "Espanha"
        HIVE_GRECIA = "Grecia"
        HIVE_HOLANDA = "Holanda"
        HIVE_BELGICA = "Belgica"
        HIVE_FRANCA = "Franca"
        HIVE_ITALIA = "Italia"
        HIVE_ALEMANHA = "Alemanha"
        HIVE_FINLANDIA = "Finlandia"
        HIVE_AUSTRIA = "Austria"
        HIVE_OTHER = "Other"
        
        if value == DIAMANTE_PORTUGAL:
            return HIVE_PORTUGAL
        elif value == DIAMANTE_ESPANHA:
            return HIVE_ESPANHA
        elif value == DIAMANTE_GRECIA:
            return HIVE_GRECIA
        elif value == DIAMANTE_HOLANDA:
            return HIVE_HOLANDA
        elif value == DIAMANTE_BELGICA:
            return HIVE_BELGICA
        elif value == DIAMANTE_FRANCA:
            return HIVE_FRANCA
        elif value == DIAMANTE_ITALIA:
            return HIVE_ITALIA
        elif value == DIAMANTE_ALEMANHA:
            return HIVE_ALEMANHA
        elif value == DIAMANTE_FINLANDIA:
            return HIVE_FINLANDIA
        elif value == DIAMANTE_AUSTRIA:
            return HIVE_AUSTRIA
        else:
            return HIVE_OTHER
        
    def row_handler_feitio_to_design_cost(self, arguments):
        """
        Converts a Diamante 2003 feitio value to a Hive design cost, based on the calculation method
        
        @param arguments: List of arguments (1st argument: value to process)
        @return: Returns the processed value
        """

        #get dictionary with all the values of the table line
        table_line_dic = arguments[0].row
        
        #if tipolgpl is not null
        if table_line_dic.has_key("tiplgp"):
            
            #get design cost calculation method
            tiplgp = table_line_dic["tiplgp"]
            
            #get unit weight
            pesounit = table_line_dic["pesounit"]
            
            #get design cost (not processed)
            feitio = table_line_dic["feitio"]
        
            # if the design cost is calculated based on product weight
            if tiplgp == "1":
                feitio = pesounit * feitio
                table_line_dic["feitio"] = feitio

    def row_handler_margin_calculation_type(self, arguments):
        """
        Asks the user to identify the margin calculation method
        
        @param arguments: List of arguments (1st argument: value to process)
        @return: Returns the processed value
        """
        
        MARGIN_CALCULATION_TYPE_PERCENTAGE = 0
        MARGIN_CALCULATION_TYPE_VALUE = 1        
        
        #if margin calculation method not already defined
        if hasattr(arguments[0], "margin_calculation_type") == False:
            
            # @todo: SCERIO: utilizar isto
            # margin_calculation_type = raw_input("Enter margin calculation type (0 - Percentage    1 - Value): ")
            margin_calculation_type = MARGIN_CALCULATION_TYPE_PERCENTAGE
            
            #set margin calculation type to user definition
            setattr(arguments[0], "margin_calculation_type", margin_calculation_type)

    def row_handler_margin_calculation(self, arguments):
        """
        Updates calculation method based on user decision
        
        @param arguments: List of arguments (1st argument: value to process)
        @return: Returns the processed value
        """
        
        MARGIN_CALCULATION_TYPE_PERCENTAGE = 0
        MARGIN_CALCULATION_TYPE_VALUE = 1   
        
        #get internal structure
        internal_structure = arguments[0].internal_structure
        
        margin_calculation_type = arguments[0].margin_calculation_type
        
        # @todo: SCERIO: corrigir isto, colocando num handler após linha
        #creates, if not existent, the entity that represents merchandise/organization relation
        entity = internal_structure.add_entity("merchandise_contactable_organizational_hierarchy_tree_node")
        entity_id = entity._id
        
        internal_structure.add_field("merchandise_contactable_organizational_hierarchy_tree_node", entity_id, "margin")
        internal_structure.add_field("merchandise_contactable_organizational_hierarchy_tree_node", entity_id, "margin_type")
            
        if margin_calculation_type == MARGIN_CALCULATION_TYPE_VALUE:
            internal_structure.set_field_value("merchandise_contactable_organizational_hierarchy_tree_node", entity_id, "margin", "69")
            internal_structure.set_field_value("merchandise_contactable_organizational_hierarchy_tree_node", entity_id, "margin_type", "96")
        elif margin_calculation_type == MARGIN_CALCULATION_TYPE_PERCENTAGE:
            internal_structure.set_field_value("merchandise_contactable_organizational_hierarchy_tree_node", entity_id, "margin", "00")
            internal_structure.set_field_value("merchandise_contactable_organizational_hierarchy_tree_node", entity_id, "margin_type", "77")
        
