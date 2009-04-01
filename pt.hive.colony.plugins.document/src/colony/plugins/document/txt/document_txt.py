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

__revision__ = "$LastChangedRevision$"
""" The revision number of the module """

__date__ = "$LastChangedDate$"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

class DocumentTxt:
    """
    Encapsulates a text file and provides operations allowing the
    insertion and extraction of data from and to a document template
    object.
    """

    file = None
    """ Reference to the text file. """

    url = None
    """ Location of the document. """

    document_id = None
    """ Unique number that identifies this file in the document manager. """

    def __init__(self, document_manager_plugin, url, document_id):
        """
        Class constructor.

        @type document_manager_plugin: DocumentManagerPlugin
        @param document_manager_plugin: Reference to the document manager plugin.
        @type document_txt_plugin: DocumentPlugin
        @param document_txt_plugin: Reference to the plugin that owns this class.
        @type url: String
        @param url: Location of the document.
        @type document_id: Integer
        @param document_id: Unique identification number for this file.
        """
        self.document_manager_plugin = document_manager_plugin
        self.file = None
        self.url = url
        self.document_id = document_id

    def get_id(self):
        """
        Returns the unique number that identifies this file in the
        document manager.

        @rtype: Integer
        @return: Unique identification number for this file.
        """
        return self.document_id

    def open(self):
        """
        Opens the document.
        """
        self.file = open(self.url, "r+")

    def close(self):
        """
        Closes the document and notifies the document manager.
        """
        self.file.close()
        self.document_manager_plugin.close(self)

    def read(self):
        """
        Extracts data from the file into a document template (each line
        in the text file is considered as a different template item).

        @rtype: DocumentTemplate
        @return: Template with data extracted from the document.
        """
        template = self.document_manager_plugin.get_new_template()
        lines = self.file.readlines()
        for line in lines:
            if line[-1] == "\n":
                line = line[:-1]
            template.set_chunk(line)
        return template

    def write(self, template):
        """
        Inserts data from the template into the document (each data item
        will be inserted into a different line in the file).

        @type template: DocumentTemplate
        @param template: Template with the data one wants to insert
        into the document.
        """
        chunks = template.get_chunks()
        for chunk in chunks:
            chunk_value = chunk.get_value()
            self.file.write(chunk_value + "\n")
