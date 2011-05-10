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

__revision__ = "$LastChangedRevision: 7650 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2010-03-24 12:16:51 +0000 (qua, 24 Mar 2010) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import colony.base.plugin_system

class DocumentPdfPlugin(colony.base.plugin_system.Plugin):
    """
    The main class for the Document Pdf plugin.
    """

    id = "pt.hive.colony.plugins.document.pdf"
    name = "Document Pdf Plugin"
    short_name = "Document Pdf"
    description = "The that control the pdf document generation and loading"
    version = "1.0.0"
    author = "Hive Solutions Lda. <development@hive.pt>"
    loading_type = colony.base.plugin_system.EAGER_LOADING_TYPE
    platforms = [
        colony.base.plugin_system.CPYTHON_ENVIRONMENT
    ]
    attributes = {
        "build_automation_file_path" : "$base{plugin_directory}/document_pdf/pdf/resources/baf.xml"
    }
    capabilities = [
        "document_pdf",
        "build_automation_item"
    ]
    main_modules = [
        "document_pdf.pdf.document_pdf_exceptions",
        "document_pdf.pdf.document_pdf_filters",
        "document_pdf.pdf.document_pdf_system"
    ]

    document_pdf = None
    """ The document pdf """

    def load_plugin(self):
        colony.base.plugin_system.Plugin.load_plugin(self)
        global document_pdf
        import document_pdf.pdf.document_pdf_system
        self.document_pdf = document_pdf.pdf.document_pdf_system.DocumentPdf(self)

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

    def create_document_controller(self, document_attributes):
        return self.document_pdf.create_document_controller(document_attributes)
