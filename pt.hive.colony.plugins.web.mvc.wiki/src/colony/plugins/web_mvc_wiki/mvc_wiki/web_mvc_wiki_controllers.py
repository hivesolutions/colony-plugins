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

import os
import time

import colony.libs.map_util
import colony.libs.importer_util

import web_mvc_wiki_exceptions

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

CACHE_DIRECTORY_IDENTIFIER = "web_mvc_wiki"
""" The cache directory identifier """

WIKI_EXTENSION = ".wiki"
""" The wiki extension """

# imports the web mvc utils
web_mvc_utils = colony.libs.importer_util.__importer__(WEB_MVC_UTILS_VALUE)

class WebMvcWikiController:
    """
    The web mvc wiki controller.
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

    def handle_wiki(self, rest_request, parameters = {}):
        """
        Handles the given wiki rest request.

        @type rest_request: RestRequest
        @param rest_request: The wiki rest request to be handled.
        @rtype: bool
        @return: The result of the handling.
        """

        # retrieves the initial time
        initial_time = time.clock()

        # retrieves the plugin manager
        plugin_manager = self.web_mvc_wiki_plugin.manager

        # retrieves the format mime plugin
        format_mime_plugin = self.web_mvc_wiki_plugin.format_mime_plugin

        # retrieves the pattern names from the parameters
        pattern_names = parameters["pattern_names"]

        # retrieves the instance name pattern
        instance_name = pattern_names["instance_name"]

        # retrieves the page name pattern
        page_name = pattern_names["page_name"]

        # retrieves the instance for the rest request
        instance = self.web_mvc_wiki._get_instance(instance_name)

        # retrieves the instance repository path
        instance_repository_path = instance["repository_path"]

        # sets the base file path as the instance repository path
        # resolved by the plugin manager
        base_file_path = plugin_manager.resolve_file_path(instance_repository_path)

        # in case the base file path is invalid
        if base_file_path == None:
            # raises the invalid repository path exception
            raise web_mvc_wiki_exceptions.InvalidRepositoryPath("'%s' from '%s'" % (base_file_path, instance_repository_path))

        # creates the base target path as the cache directory path
        # using the given instance name
        base_target_path = self._get_cache_directory_path(instance_name)

        # in case the base target path does not exists
        if not os.path.exists(base_target_path):
            # creates the base target path
            os.makedirs(base_target_path)

        # retrieves the file path striping the file path
        file_path = page_name.rstrip("/")

        # retrieves the file path
        file_path = file_path and file_path or "index"

        # retrieves the encoder name
        encoder_name = rest_request.encoder_name and rest_request.encoder_name or "html"

        if not rest_request.encoder_name or rest_request.encoder_name in ("html", "ajx", "prt"):
            # creates the wiki file path
            wiki_file_path = base_file_path + "/" + file_path + WIKI_EXTENSION

            # in case the wiki file does not exist
            if not os.path.exists(wiki_file_path):
                # retrieves the template file
                template_file = self.retrieve_template_file("general_action.html.tpl")

                # sets the page to be included
                template_file.assign("page_include", "new_contents.html.tpl")

                # sets the page name in the template file
                template_file.assign("page_name", file_path)

                # sets the instance name in the template file
                template_file.assign("instance_name", instance_name)

                # applies the base path to the template file
                self.apply_base_path_template_file(rest_request, template_file)

                # processes the template file and sets the request contents
                self.process_set_contents(rest_request, template_file)

                # returns true (valid)
                return True

            # creates the structure that will hold the information
            # about the output of the wiki generation
            output_structure = {}

            # creates the configuration map for the html generation
            configuration_map = {"auto_numbered_sections" : True, "generate_footer" : False, "simple_parse" : True}

            # creates the engine properties map
            engine_properties = {"file_path" : wiki_file_path, "target_path" : base_target_path,
                                 "output_structure" : output_structure, "configuration_map" : configuration_map}

            # retrieves the language wiki plugin
            language_wiki_plugin = self.web_mvc_wiki_plugin.language_wiki_plugin

            # generates the html files using the wiki engine with the given engine properties
            language_wiki_plugin.generate("html", engine_properties)

        # retrieves the file extension
        file_extension = encoder_name in ("ajx", "prt") and "html" or encoder_name

        # creates the target file name from the file path and the file extension
        target_file_name = file_path + "." + file_extension

        # creates the target file path appending the base target path with
        # the target file name
        target_file_path = base_target_path + "/" + target_file_name

        # opens the target file
        target_file = open(target_file_path, "rb")

        # reads the target file contents
        target_file_contents = target_file.read()

        # closes the target file
        target_file.close()

        # in case the file is html one
        if file_extension == "html":
            # decodes the file contents using the file encoding
            target_file_contents = target_file_contents.decode(TARGET_FILE_ENCODING)

        if not rest_request.encoder_name or rest_request.encoder_name in ("html", "prt"):
            # in case there is no encoder name defined or the encoder name is html
            if not rest_request.encoder_name or rest_request.encoder_name == "html":
                # retrieves the general template file
                template_file_name = "general.html.tpl"
            # in case the encoder name is print
            elif rest_request.encoder_name == "prt":
                # retrieves the general print template file
                template_file_name = "general_print.html.tpl"

            # retrieves the template file
            template_file = self.retrieve_template_file(template_file_name)

            # opens the wiki file
            wiki_file = open(wiki_file_path, "rb")

            # reads the wiki file contents
            wiki_file_contents = wiki_file.read()

            # decodes the wiki file contents
            wiki_file_contents = wiki_file_contents.decode("Cp1252")

            # closes the wiki file
            wiki_file.close()

            # retrieves the final time
            final_time = time.clock()

            # calculates the generation (delta) time
            generation_time = final_time - initial_time

            # creates the generation time string
            generation_time_string = "%.2f" % generation_time

            # sets the page name in the template file
            template_file.assign("page_name", file_path)

            # sets the page source in the template file
            template_file.assign("page_source", wiki_file_contents)

            # sets the page page contents to be loaded in the template file
            template_file.assign("page_contents", target_file_contents)

            # sets the generation time in the template file
            template_file.assign("generation_time", generation_time_string)

            # sets the instance name in the template file
            template_file.assign("instance_name", instance_name)

            # assigns the session variables to the template file
            self.assign_session_template_file(rest_request, template_file)

            # applies the base path to the template file
            self.apply_base_path_template_file(rest_request, template_file)

            # processes the template file and sets the request contents
            self.process_set_contents(rest_request, template_file)
        else:
            # retrieves the mime type for the target file name
            mime_type = format_mime_plugin.get_mime_type_file_name(target_file_name)

            # sets the request contents
            self.set_contents(rest_request, target_file_contents, mime_type)

        # returns true
        return True

    def handle_resources(self, rest_request, parameters):
        """
        Handles the given resources rest request.

        @type rest_request: RestRequest
        @param rest_request: The resources rest request to be handled.
        @rtype: bool
        @return: The result of the handling.
        """

        # retrieves the format mime plugin
        format_mime_plugin = self.web_mvc_wiki_plugin.format_mime_plugin

        # retrieves the pattern names from the parameters
        pattern_names = parameters["pattern_names"]

        # retrieves the instance name pattern
        instance_name = pattern_names["instance_name"]

        # retrieves the resource type pattern
        resource_type = pattern_names["resource_type"]

        # retrieves the resource name pattern
        resource_name = pattern_names["resource_name"]

        # creates the base target path as the cache directory path
        base_target_path = self._get_cache_directory_path(instance_name)

        # retrieves the file base path by joining resource values
        file_path = "/".join([resource_type, resource_name])

        # creates the full file name
        full_file_name = file_path + "." + rest_request.encoder_name

        # creates the full path to the file to be read
        full_file_path = base_target_path + "/" + full_file_name

        # opens the resource file
        resource_file = open(full_file_path, "rb")

        try:
            # retrieves the resource file contents
            resource_file_contents = resource_file.read()
        finally:
            # closes the resource file
            resource_file.close()

        # retrieves the mime type for the target file name
        mime_type = format_mime_plugin.get_mime_type_file_name(full_file_name)

        # sets the request contents
        self.set_contents(rest_request, resource_file_contents, mime_type)

        # returns true
        return True

    def _get_cache_directory_path(self, instance_name):
        """
        Retrieves the reference path for the cache directory.

        @type instance_name: String
        @param instance_name: The name of the instance in use.
        @rtype: String
        @return: The reference path to the cache directory.
        """

        # retrieves the main cache manager plugin
        main_cache_manager_plugin = self.web_mvc_wiki_plugin.main_cache_manager_plugin

        # retrieves the base cache directory path
        base_cache_directory_path = main_cache_manager_plugin.get_cache_directory_path()

        # creates the cache directory path appending the unique identifier
        cache_diretory_path = base_cache_directory_path + "/" + CACHE_DIRECTORY_IDENTIFIER + "/" + instance_name

        # returns the cache directory path
        return cache_diretory_path

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

    def handle_new(self, rest_request, parameters = {}):
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

        # retrieves the pattern names from the parameters
        pattern_names = parameters["pattern_names"]

        # retrieves the instance name pattern
        instance_name = pattern_names["instance_name"]

        # retrieves the page name pattern
        page_name = pattern_names["page_name"]

        # retrieves the instance for the instance name
        instance = self.web_mvc_wiki._get_instance(instance_name)

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

        # creates the complete file path for the wiki file
        complete_file_path = base_file_path + "/" + page_name + WIKI_EXTENSION

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
        self.redirect(rest_request, base_path + instance_name + "/" + page_name)

        return True

    def handle_edit(self, rest_request, parameters = {}):
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

        # retrieves the pattern names from the parameters
        pattern_names = parameters["pattern_names"]

        # retrieves the instance name pattern
        instance_name = pattern_names["instance_name"]

        # retrieves the page name pattern
        page_name = pattern_names["page_name"]

        # retrieves the instance for the rest request
        instance = self.web_mvc_wiki._get_instance(instance_name)

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

        # creates the complete file path for the wiki file
        complete_file_path = base_file_path + "/" + page_name + WIKI_EXTENSION

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
