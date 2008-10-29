#!/usr/bin/python
# -*- coding: Cp1252 -*-

# Hive Colony
# Copyright (C) 2008 Hive Solutions Lda.
#
# This file is part of Hive Colony.
#
# Hive Colony is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Hive Colony is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Hive Colony. If not, see <http://www.gnu.org/licenses/>.

__author__ = "Tiago Silva <tsilva@hive.pt>"
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

import unittest
import os

class DocumentTest:

    document_manager_plugin = None

    def __init__(self, document_manager_plugin):
        self.document_manager_plugin = document_manager_plugin

    def get_plugin_test_case_bundle(self):
        return [DocumentManagerPluginTestCase]

class DocumentTestCase(unittest.TestCase):

    def setUp(self):
        self.plugin.logger.info("Setting up Document Manager Test Case...")

    def test_odt_to_txt(self):
        """
        Tests data extraction and retrieval to and from odt and txt files.
        """
        supported_formats = self.plugin.get_supported_formats()
        # if the txt and odt plugins are loaded
        if "txt" in supported_formats and "odt" in supported_formats:
            # open the odt test template
            temp_document_path = os.path.join(os.path.dirname(__file__), "odt/resources/test_template.odt")
            temp_document_path = os.path.abspath(temp_document_path)
            document = self.plugin.open(temp_document_path, "odt")
            # test the file was opened
            self.assertNotEqual(document, None)
            # test the id is valid
            document_id = document.get_id()
            self.assertTrue(document_id > 0)
            # test the manager is holding the correct amount of open files
            open_documents = self.plugin.get_open_documents()
            self.assertEqual(len(open_documents), 1)
            # extract data from the document and check that 5 chunks were extracted
            template = document.read()
            chunks = template.get_chunks()
            self.assertEqual(len(chunks), 5)
            # change the template and write it into the document
            template.set_chunk("Aibo Solutions", chunk_id = "company_name")
            template.set_chunk("Jeremias", chunk_id = "name")
            template.set_chunk("Rua das cenas", chunk_id = "address")
            template.set_chunk("66666666", chunk_id = "phone")
            template.set_chunk("99999999", chunk_id = "fax")
            document.write(template)
            document.close()
            
            # open the document again and check that the previously written data is there
            document = self.plugin.open(temp_document_path, "odt")
            self.assertNotEqual(document, None)
            document_id = document.get_id()
            self.assertTrue(document_id > 0)
            open_documents = self.plugin.get_open_documents()
            self.assertEqual(len(open_documents), 1)
            template = document.read()
            chunks = template.get_chunks()
            self.assertEqual(len(chunks), 5)
            self.assertEqual(template.get_chunk("company_name").get_value(), "Aibo Solutions")
            self.assertEqual(template.get_chunk("name").get_value(), "Jeremias")
            self.assertEqual(template.get_chunk("address").get_value(), "Rua das cenas")
            self.assertEqual(template.get_chunk("phone").get_value(), "66666666")
            self.assertEqual(template.get_chunk("fax").get_value(), "99999999")
            document.close()
            
            # clears the test txt file
            temp_document_path = os.path.join(os.path.dirname(__file__), "txt/resources/test_template.txt")
            temp_document_path = os.path.abspath(temp_document_path)
            file = open(temp_document_path, "w")
            file.close()
            
            # opens the test txt file, and write's the template extracted from the odt into it
            document = self.plugin.open(temp_document_path, "txt")
            self.assertNotEqual(document, None)
            document_id = document.get_id()
            self.assertTrue(document_id > 0)
            open_documents = self.plugin.get_open_documents()
            self.assertEqual(len(open_documents), 1)
            document.write(template)
            document.close()
            
            # opens the txt file again and checks that the data previously written is there
            document = self.plugin.open(temp_document_path, "txt")
            self.assertNotEqual(document, None)
            document_id = document.get_id()
            self.assertTrue(document_id > 0)
            open_documents = self.plugin.get_open_documents()
            self.assertEqual(len(open_documents), 1)
            template = document.read()
            chunks = template.get_chunks()
            for chunk in chunks:
                value = chunk.get_value()
                self.assertTrue(value in ["Aibo Solutions", "Jeremias", "Rua das cenas", "66666666", "99999999"])
            self.assertEqual(len(chunks), 5)
            document.close()

class DocumentManagerPluginTestCase:

    @staticmethod
    def get_related_class():
        return pt.hive.colony.plugins.DocumentManagerPlugin

    @staticmethod
    def get_test_case():
        return DocumentTestCase

    @staticmethod
    def get_pre_conditions():
        return None

    @staticmethod
    def get_description():
        return "Document Manager Plugin test case"
