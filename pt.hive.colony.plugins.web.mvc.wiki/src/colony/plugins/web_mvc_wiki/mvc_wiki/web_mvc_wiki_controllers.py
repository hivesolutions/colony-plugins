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

__author__ = "João Magalhães <joamag@hive.pt> & Luís Martinho <lmartinho@hive.pt>"
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

import colony.libs.map_util
import colony.libs.importer_util

WEB_MVC_UTILS_VALUE = "web_mvc_utils"
""" The web mvc utils value """

WEB_MVC_WIKI_RESOURCES_PATH = "web_mvc_wiki/mvc_wiki/resources"
""" The web mvc wiki resources path """

DEFAULT_ENCODING = "utf-8"
""" The default encoding value """

DEFAULT_SUMMARY = "automated wiki commit"
""" The default summary value """

TARGET_FILE_ENCODING = "Cp1252"
""" The target file encoding """

TEMPLATES_PATH = WEB_MVC_WIKI_RESOURCES_PATH + "/templates"
""" The templates path """

WIKI_EXTENSION = ".wiki"
""" The wiki extension """

# imports the web mvc utils
web_mvc_utils = colony.libs.importer_util.__importer__(WEB_MVC_UTILS_VALUE)

class WebMvcWikiPageController:
    """
    The web mvc wiki page controller.
    """

    web_mvc_wiki_plugin = None
    """ The web mvc wiki plugin """

    web_mvc_wiki = None
    """ The web mvc wiki """

    def __init__(self, web_mvc_wiki_plugin, web_mvc_wiki):
        """
        Constructor of the class.

        @type web_mvc_wiki_plugin: WebMvcWikiPlugin
        @param web_mvc_wiki_plugin: The web vmc wiki plugin.
        @type web_mvc_wiki: WebMvcWiki
        @param web_mvc_wiki: The web mvc wiki.
        """

        self.web_mvc_wiki_plugin = web_mvc_wiki_plugin
        self.web_mvc_wiki = web_mvc_wiki

    def start(self):
        """
        Method called upon structure initialization
        """

        # retrieves the plugin manager
        plugin_manager = self.web_mvc_wiki_plugin.manager

        # retrieves the web mvc manager plugin path
        web_mvc_manager_plugin_path = plugin_manager.get_plugin_path_by_id(self.web_mvc_wiki_plugin.id)

        # creates the templates path
        templates_path = web_mvc_manager_plugin_path + "/" + TEMPLATES_PATH

        # sets the templates path
        self.set_templates_path(templates_path)

    def handle_new(self, rest_request, parameters):
        """
        Handles the given page rest request.

        @type rest_request: RestRequest
        @param rest_request: The page rest request to be handled.
        @rtype: bool
        @return: The result of the handling.
        """

        # retrieves the plugin manager
        plugin_manager = self.web_mvc_wiki_plugin.manager

        # retrieves the revision control manager plugin
        revision_control_manager_plugin = self.web_mvc_wiki_plugin.revision_control_manager_plugin

        # processes the form data
        form_data_map = self.process_form_data(rest_request, DEFAULT_ENCODING)

        # retrieves the instance for the rest request
        instance = self.web_mvc_wiki._get_instance(rest_request)

        # retrieves the instance name
        instance_name = instance["name"]

        # retrieves the instance repository type
        instance_repository_type = instance["repository_type"]

        # retrieves the instance repository arguments
        instance_repository_arguments = instance["repository_arguments"]

        # retrieves the instance repository path
        instance_repository_path = instance["repository_path"]

        # retrieves the summary and the contents
        summary = form_data_map.get("wiki_page_new_summary", DEFAULT_SUMMARY)
        contents = form_data_map["wiki_page_new_contents"]

        # normalizes the contents
        normalized_contents = self._normalize_contents(contents)

        # sets the base file path as the instance repository path
        # resolved by the plugin manager
        base_file_path = plugin_manager.resolve_file_path(instance_repository_path)

        # retrieves the file name
        file_name = rest_request.path_list[-1]

        # creates the complete file path for the wiki file
        complete_file_path = base_file_path + "/" + file_name + WIKI_EXTENSION

        # writes the normalized contents to the wiki file (in the complete file path)
        self._write_file(complete_file_path, normalized_contents)

        # creates the revision control parameters
        revision_control_parameters = colony.libs.map_util.map_extend(instance_repository_arguments, {"repository_path" : base_file_path})

        # loads a new revision control manager for the specified adapter name
        revision_control_manager = revision_control_manager_plugin.load_revision_control_manager(instance_repository_type, revision_control_parameters)

        # uses the revision control manager to add the file
        revision_control_manager.add([complete_file_path], True)

        # uses the revision control manager to perform the commit
        revision_control_manager.commit([complete_file_path], summary)

        # retrieves the base path
        base_path = self.get_base_path(rest_request)

        # redirects the rest request
        self.redirect(rest_request, base_path + instance_name + "/" + file_name)

        return True

    def handle_edit(self, rest_request, parameters):
        """
        Handles the given page rest request.

        @type rest_request: RestRequest
        @param rest_request: The page rest request to be handled.
        @rtype: bool
        @return: The result of the handling.
        """

        # retrieves the plugin manager
        plugin_manager = self.web_mvc_wiki_plugin.manager

        # retrieves the revision control manager plugin
        revision_control_manager_plugin = self.web_mvc_wiki_plugin.revision_control_manager_plugin

        # processes the form data
        form_data_map = self.process_form_data(rest_request, DEFAULT_ENCODING)

        # retrieves the instance for the rest request
        instance = self.web_mvc_wiki._get_instance(rest_request)

        # retrieves the instance repository type
        instance_repository_type = instance["repository_type"]

        # retrieves the instance repository arguments
        instance_repository_arguments = instance["repository_arguments"]

        # retrieves the instance repository path
        instance_repository_path = instance["repository_path"]

        # retrieves the summary and the contents
        summary = form_data_map.get("wiki_page_edit_summary", DEFAULT_SUMMARY)
        contents = form_data_map["wiki_page_edit_contents"]

        # normalizes the contents
        normalized_contents = self._normalize_contents(contents)

        # sets the base file path as the instance repository path
        # resolved by the plugin manager
        base_file_path = plugin_manager.resolve_file_path(instance_repository_path)

        # retrieves the file name
        file_name = rest_request.path_list[-1]

        # creates the complete file path for the wiki file
        complete_file_path = base_file_path + "/" + file_name + WIKI_EXTENSION

        # writes the normalized contents to the wiki file (in the complete file path)
        self._write_file(complete_file_path, normalized_contents)

        # creates the revision control parameters
        revision_control_parameters = colony.libs.map_util.map_extend(instance_repository_arguments, {"repository_path" : base_file_path})

        # loads a new revision control manager for the specified adapter name
        revision_control_manager = revision_control_manager_plugin.load_revision_control_manager(instance_repository_type, revision_control_parameters)

        # uses the revision control manager to perform the commit
        commit_revision = revision_control_manager.commit([complete_file_path], summary)

        # sets the request contents
        self.set_contents(rest_request, "revision: " + str(commit_revision.get_number()))

        return True

    def _normalize_contents(self, contents):
        """
        Normalizes the given contents, using the string normalization plugin.
        The output should be a string without trailing spaces and
        without extra newlines.

        @type contents: String
        @param contents: The contents to be normalized.
        @rtype: String
        @return: The normalized contents.
        """

        # retrieves the string normalization plugin
        string_normalization_plugin = self.web_mvc_wiki_plugin.string_normalization_plugin

        # normalizes the contents by removing the trailing spaces and the extra newlines
        normalized_contents = string_normalization_plugin.remove_trailing_spaces(contents, True, True)
        normalized_contents = string_normalization_plugin.remove_trailing_newlines(normalized_contents, True)

        # returns the normalized contents
        return normalized_contents

    def _write_file(self, file_path, contents):
        """
        Writes the contents to the file in the given
        file path, using default text encoding.

        @type file_path: String
        @param file_path: The path to the file to write.
        @type contents: String
        @param contents: The contents to be written.
        """

        # opens the file for writing
        file = open(file_path, "w")

        try:
            # encodes the contents to the file encoding
            contents = contents.encode(TARGET_FILE_ENCODING)

            # writes the contents
            file.write(contents)
        finally:
            # closes the file
            file.close()
