#!/usr/bin/python
# -*- coding: utf-8 -*-

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
import tempfile

import colony.libs.map_util
import colony.libs.importer_util

import web_mvc_wiki_exceptions

WEB_MVC_UTILS_VALUE = "web_mvc_utils"
""" The web mvc utils value """

WEB_MVC_WIKI_RESOURCES_PATH = "web_mvc_wiki/mvc_wiki/resources"
""" The web mvc wiki resources path """

DEFAULT_ENCODING = "utf-8"
""" The default encoding value """

SERIALIZER_VALUE = "serializer"
""" The default serializer value """

DEFAULT_SUMMARY = "automated wiki commit"
""" The default summary value """

TARGET_FILE_ENCODING = "utf-8"
""" The target file encoding """

WIKI_FILE_ENCODING = "utf-8"
""" The wiki file encoding """

WIKI_EXTENSION = ".wiki"
""" The wiki extension """

CACHE_DIRECTORY_IDENTIFIER = "web_mvc_wiki"
""" The cache directory identifier """

WIKI_EXTENSION = ".wiki"
""" The wiki extension """

DEFAULT_LOGO_PATH = "images/colony_logo.png"
""" The default logo path """

DEFAULT_ICON_PATH = "images/colony_icon_ico"
""" The default icon path """

# imports the web mvc utils
web_mvc_utils = colony.libs.importer_util.__importer__(WEB_MVC_UTILS_VALUE)

class MainController:
    """
    The web mvc wiki main controller.
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

        # sets the relative resources path
        self.set_relative_resources_path(WEB_MVC_WIKI_RESOURCES_PATH)

class PageController:
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

        # sets the relative resources path
        self.set_relative_resources_path(WEB_MVC_WIKI_RESOURCES_PATH)

    def handle_create(self, rest_request, parameters = {}):
        """
        Handles the given create page rest request.

        @type rest_request: RestRequest
        @param rest_request: The create page rest request to
        be handled.
        """

        # retrieves the form data by processing the form
        form_data_map = self.process_form_data(rest_request, DEFAULT_ENCODING)

        # retrieves the instance name pattern
        instance_name = self.get_pattern(parameters, "instance_name")

        # retrieves the page
        page = form_data_map.get("page", {})

        # updates the page (created it because none exists)
        self._update_page(rest_request, page, instance_name)

        # retrieves the page name
        page_name = page["name"]

        # redirects the rest request
        self.redirect_base_path(rest_request, instance_name + "/" + page_name)

    def handle_show(self, rest_request, parameters = {}):
        """
        Handles the given show rest request.

        @type rest_request: RestRequest
        @param rest_request: The show rest request to be handled.
        """

        # retrieves the initial time
        initial_time = time.clock()

        # retrieves the plugin manager
        plugin_manager = self.web_mvc_wiki_plugin.manager

        # retrieves the format mime plugin
        format_mime_plugin = self.web_mvc_wiki_plugin.format_mime_plugin

        # retrieves the various patterns
        instance_name = self.get_pattern(parameters, "instance_name")
        page_name = self.get_pattern(parameters, "page_name")

        # retrieves the instance for the rest request
        instance = self.web_mvc_wiki._get_instance(instance_name)

        # retrieves the instance attributes
        instance_wiki_name = instance.get("wiki_name", instance_name)
        instance_template = instance.get("template", "main")
        instance_main_page = instance.get("main_page", "index")
        instance_repository_path = instance["repository_path"]
        instance_logo_path = instance.get("logo_path", DEFAULT_LOGO_PATH)
        instance_icon_path = instance.get("icon_path", DEFAULT_ICON_PATH)
        instance_footer_enabled = instance.get("footer_enabled", True)
        instance_options_enabled = instance.get("options_enabled", True)
        instance_print_enabled = instance.get("print_enabled", True)
        instance_header_links = instance.get("header_links", [])
        instance_configuration_map = instance.get("configuration_map", {})
        instance_configuration_index = instance.get("configuration_index", [])

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

        # retrieves the file path striping the file path
        # then checks if it's not empty using the instance
        # main page in case it is
        file_path = page_name.rstrip("/")
        file_path = file_path or instance_main_page

        # retrieves the encoder name
        encoder_name = rest_request.encoder_name and rest_request.encoder_name or "html"

        # encoder name is not provided or the encoder name is html, ajax or print
        if not rest_request.encoder_name or rest_request.encoder_name in ("html", "ajx", "prt"):
            # creates the wiki file path
            wiki_file_path = os.path.join(base_file_path, file_path + WIKI_EXTENSION)

            try:
                # generates the wiki files using the wiki engine
                self._generate_wiki_html_files(base_target_path, wiki_file_path, instance_configuration_map)
            except web_mvc_wiki_exceptions.WikiFileNotFound:
                # retrieves the template file
                template_file = self.retrieve_template_file("general_action.html.tpl")

                # assigns the include to the template
                self.assign_include_template_file(template_file, "page_include", "new_contents.html.tpl")

                # sets the page name in the template file
                template_file.assign("page_name", file_path)

                # sets the various template file variables
                template_file.assign("wiki_name", instance_wiki_name)
                template_file.assign("template", instance_template)
                template_file.assign("main_page", instance_main_page)
                template_file.assign("instance_name", instance_name)
                template_file.assign("instance_configuration_index", instance_configuration_index)
                template_file.assign("logo_path", instance_logo_path)
                template_file.assign("icon_path", instance_icon_path)
                template_file.assign("footer_enabled", instance_footer_enabled)
                template_file.assign("options_enabled", instance_options_enabled)
                template_file.assign("print_enabled", instance_print_enabled)
                template_file.assign("header_links", instance_header_links)

                # applies the base path to the template file
                self.apply_base_path_template_file(rest_request, template_file)

                # processes the template file and sets the request contents
                self.process_set_contents(rest_request, template_file)

                # returns
                return

        # retrieves the file extension
        file_extension = encoder_name in ("ajx", "prt") and "html" or encoder_name

        # creates the target file name from the file path and the file extension
        target_file_name = file_path + "." + file_extension

        # creates the target file path joining the base target path with
        # the target file name
        target_file_path = os.path.join(base_target_path, target_file_name)

        # retrieves the target file contents
        target_file_contents = self._get_file_contents(target_file_path)

        # in case the file is html one
        if file_extension == "html":
            # decodes the file contents using the file encoding
            target_file_contents = target_file_contents.decode(TARGET_FILE_ENCODING)

        # in case and encoder name is provided but is not html or print
        if rest_request.encoder_name and not rest_request.encoder_name in ("html", "prt"):
            # retrieves the mime type for the target file name
            mime_type = format_mime_plugin.get_mime_type_file_name(target_file_name)

            # sets the request contents
            self.set_contents(rest_request, target_file_contents, mime_type)

            # returns
            return

        # in case there is no encoder name defined or the encoder name is html
        if not rest_request.encoder_name or rest_request.encoder_name == "html":
            # retrieves the general template file
            template_file_name = "general.html.tpl"
        # in case the encoder name is print
        elif rest_request.encoder_name == "prt":
            # retrieves the general print template file
            template_file_name = "general_print.html.tpl"

        # retrieves the wiki file contents decoded
        wiki_file_contents = self._get_file_contents_decoded(wiki_file_path, WIKI_FILE_ENCODING)

        # retrieves the final time and calculates the
        # generation (delta) time
        final_time = time.clock()
        generation_time = final_time - initial_time

        # creates the generation time string
        generation_time_string = "%.2f" % generation_time

        # retrieves the template file
        template_file = self.retrieve_template_file(template_file_name)

        # sets the various template file variables
        template_file.assign("page_name", file_path)
        template_file.assign("page_source", wiki_file_contents)
        template_file.assign("page_contents", target_file_contents)
        template_file.assign("wiki_name", instance_wiki_name)
        template_file.assign("template", instance_template)
        template_file.assign("main_page", instance_main_page)
        template_file.assign("generation_time", generation_time_string)
        template_file.assign("instance_name", instance_name)
        template_file.assign("instance_configuration_index", instance_configuration_index)
        template_file.assign("logo_path", instance_logo_path)
        template_file.assign("icon_path", instance_icon_path)
        template_file.assign("footer_enabled", instance_footer_enabled)
        template_file.assign("options_enabled", instance_options_enabled)
        template_file.assign("print_enabled", instance_print_enabled)
        template_file.assign("header_links", instance_header_links)

        # assigns the session variables to the template file
        self.assign_session_template_file(rest_request, template_file)

        # applies the base path to the template file
        self.apply_base_path_template_file(rest_request, template_file)

        # processes the template file and sets the request contents
        self.process_set_contents(rest_request, template_file)

    def handle_resources(self, rest_request, parameters):
        """
        Handles the given resources rest request.

        @type rest_request: RestRequest
        @param rest_request: The resources rest request to be handled.
        """

        # retrieves the format mime plugin
        format_mime_plugin = self.web_mvc_wiki_plugin.format_mime_plugin

        # retrieves the various patterns
        instance_name = self.get_pattern(parameters, "instance_name")
        resource_type = self.get_pattern(parameters, "resource_type")
        resource_name = self.get_pattern(parameters, "resource_name")

        # creates the base target path as the cache directory path
        base_target_path = self._get_cache_directory_path(instance_name)

        # retrieves the file base path by joining resource values
        file_path = "/".join([resource_type, resource_name])

        # creates the full file name
        full_file_name = file_path + "." + rest_request.encoder_name

        # creates the full path to the file to be read
        full_file_path = os.path.join(base_target_path, full_file_name)

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

    def handle_edit(self, rest_request, parameters):
        """
        Handles the given edit rest request.

        @type rest_request: RestRequest
        @param rest_request: The edit rest request to be handled.
        """

        # retrieves the plugin manager
        plugin_manager = self.web_mvc_wiki_plugin.manager

        # retrieves the various patterns
        instance_name = self.get_pattern(parameters, "instance_name")
        page_name = self.get_pattern(parameters, "page_name")

        # retrieves the instance for the rest request
        instance = self.web_mvc_wiki._get_instance(instance_name)

        # retrieves the instance attributes
        instance_wiki_name = instance.get("wiki_name", instance_name)
        instance_template = instance.get("template", "main")
        instance_main_page = instance.get("main_page", "index")
        instance_repository_path = instance["repository_path"]
        instance_logo_path = instance.get("logo_path", DEFAULT_LOGO_PATH)
        instance_configuration_index = instance.get("configuration_index", [])

        # sets the base file path as the instance repository path
        # resolved by the plugin manager
        base_file_path = plugin_manager.resolve_file_path(instance_repository_path)

        # in case the base file path is invalid
        if base_file_path == None:
            # raises the invalid repository path exception
            raise web_mvc_wiki_exceptions.InvalidRepositoryPath("'%s' from '%s'" % (base_file_path, instance_repository_path))

        # retrieves the file path striping the file path
        # then checks if it's not empty using the instance
        # main page in case it is
        file_path = page_name.rstrip("/")
        file_path = file_path or instance_main_page

        # creates the wiki file path
        wiki_file_path = os.path.join(base_file_path, file_path + WIKI_EXTENSION)

        # retrieves the wiki file contents decoded
        wiki_file_contents = self._get_file_contents_decoded(wiki_file_path, WIKI_FILE_ENCODING)

        # retrieves the template file
        template_file = self.retrieve_template_file("general_action.html.tpl")

        # assigns the include to the template
        self.assign_include_template_file(template_file, "page_include", "edit_contents.html.tpl")

        # sets the various template file variables
        template_file.assign("page_name", file_path)
        template_file.assign("page_source", wiki_file_contents)
        template_file.assign("wiki_name", instance_wiki_name)
        template_file.assign("template", instance_template)
        template_file.assign("main_page", instance_main_page)
        template_file.assign("instance_name", instance_name)
        template_file.assign("instance_configuration_index", instance_configuration_index)
        template_file.assign("logo_path", instance_logo_path)

        # assigns the session variables to the template file
        self.assign_session_template_file(rest_request, template_file)

        # applies the base path to the template file
        self.apply_base_path_template_file(rest_request, template_file)

        # processes the template file and sets the request contents
        self.process_set_contents(rest_request, template_file)

    @web_mvc_utils.serialize_exceptions("all")
    def handle_update(self, rest_request, parameters = {}):
        """
        Handles the given update page serialized rest request.

        @type rest_request: RestRequest
        @param rest_request: The update page serialized rest request
        to be handled.
        """

        # retrieves the form data by processing the form
        form_data_map = self.process_form_data(rest_request, DEFAULT_ENCODING)

        # retrieves the various patterns
        instance_name = self.get_pattern(parameters, "instance_name")
        page_name = self.get_pattern(parameters, "page_name")

        # retrieves the page
        page = form_data_map.get("page", {})

        # sets the page name in the page
        page["name"] = page_name

        # updates the page
        self._update_page(rest_request, page, instance_name)

        # redirects the rest request
        self.redirect_base_path(rest_request, instance_name + "/" + page_name)

    def handle_preview(self, rest_request, parameters = {}):
        """
        Handles the given preview rest request.

        @type rest_request: RestRequest
        @param rest_request: The show rest request to be handled.
        """

        # retrieves the initial time
        initial_time = time.clock()

        # retrieves the form data by processing the form
        form_data_map = self.process_form_data(rest_request, DEFAULT_ENCODING)

        # retrieves the various patterns
        instance_name = self.get_pattern(parameters, "instance_name")
        page_name = self.get_pattern(parameters, "page_name")

        # retrieves the instance for the rest request
        instance = self.web_mvc_wiki._get_instance(instance_name)

        # retrieves the page
        page = form_data_map.get("page", {})

        # sets the page name in the page
        page["name"] = page_name

        # retrieves the page contents
        page_contents = page["contents"]

        # normalizes the contents
        normalized_contents = self._normalize_contents(page_contents)

        # retrieves the instance attributes
        instance_wiki_name = instance.get("wiki_name", instance_name)
        instance_template = instance.get("template", "main")
        instance_main_page = instance.get("main_page", "index")
        instance_logo_path = instance.get("logo_path", DEFAULT_LOGO_PATH)
        instance_icon_path = instance.get("icon_path", DEFAULT_ICON_PATH)
        instance_footer_enabled = instance.get("footer_enabled", True)
        instance_options_enabled = instance.get("options_enabled", True)
        instance_print_enabled = instance.get("print_enabled", True)
        instance_header_links = instance.get("header_links", [])
        instance_configuration_map = instance.get("configuration_map", {})
        instance_configuration_index = instance.get("configuration_index", [])

        # creates a new temporary directory path and a temporary
        # file path in the directory for the wiki page creation
        temporary_directory_path = tempfile.mkdtemp()
        temporary_file_path = os.path.join(temporary_directory_path, page_name + WIKI_EXTENSION)

        # opens the temporary file path for writing
        temporary_file = open(temporary_file_path, "wb")

        try:
            # writes the normalizes contents (wiki contents)
            # into the temporary file
            temporary_file.write(normalized_contents)
        finally:
            # closes the temporary file
            temporary_file.close()

        # retrieves the file path striping the file path
        # then checks if it's not empty using the instance
        # main page in case it is
        file_path = page_name.rstrip("/")
        file_path = file_path or instance_main_page

        # generates the wiki files using the wiki engine
        self._generate_wiki_html_files(temporary_directory_path, temporary_file_path, instance_configuration_map)

        # creates the target file name from the file path and the file extension
        target_file_name = file_path + ".html"

        # creates the target file path joining the base target path with
        # the target file name
        target_file_path = os.path.join(temporary_file_path, target_file_name)

        # retrieves the target file contents
        target_file_contents = self._get_file_contents(target_file_path)

        # decodes the file contents using the file encoding
        target_file_contents = target_file_contents.decode(TARGET_FILE_ENCODING)

        # retrieves the final time and  calculates the
        # generation (delta) time
        final_time = time.clock()
        generation_time = final_time - initial_time

        # creates the generation time string
        generation_time_string = "%.2f" % generation_time

        # retrieves the template file
        template_file = self.retrieve_template_file("general_action.html.tpl")

        # assigns the include to the template
        self.assign_include_template_file(template_file, "page_include", "preview_contents.html.tpl")

        # sets the various template file variables
        template_file.assign("page_name", file_path)
        template_file.assign("page_source", page_contents)
        template_file.assign("page_contents", target_file_contents)
        template_file.assign("wiki_name", instance_wiki_name)
        template_file.assign("template", instance_template)
        template_file.assign("main_page", instance_main_page)
        template_file.assign("generation_time", generation_time_string)
        template_file.assign("instance_name", instance_name)
        template_file.assign("instance_configuration_index", instance_configuration_index)
        template_file.assign("logo_path", instance_logo_path)
        template_file.assign("icon_path", instance_icon_path)
        template_file.assign("footer_enabled", instance_footer_enabled)
        template_file.assign("options_enabled", instance_options_enabled)
        template_file.assign("print_enabled", instance_print_enabled)
        template_file.assign("header_links", instance_header_links)

        # assigns the session variables to the template file
        self.assign_session_template_file(rest_request, template_file)

        # applies the base path to the template file
        self.apply_base_path_template_file(rest_request, template_file)

        # processes the template file and sets the request contents
        self.process_set_contents(rest_request, template_file)

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

    def _generate_wiki_html_files(self, base_target_path, wiki_file_path, configuration_map):
        """
        Generates the html files using the wiki engine.
        The generation of the html files is achieved using
        the wiki engine library.

        @type base_target_path: String.
        @param base_target_path: The base target path.
        @type wiki_file_path: String.
        @param wiki_file_path: The wiki file path.
        @type configuration_map: String.
        @param configuration_map: The configuration map to be used.
        """

        # prints a debug message
        self.web_mvc_wiki_plugin.debug("Generating wiki file: %s" % wiki_file_path)

        # in case the base target path does not exists
        if not os.path.exists(base_target_path):
            # creates the base target path
            os.makedirs(base_target_path)

        # in case the wiki file does not exist
        if not os.path.exists(wiki_file_path):
            # raise the file not found exception
            raise web_mvc_wiki_exceptions.WikiFileNotFound(wiki_file_path)

        # creates the structure that will hold the information
        # about the output of the wiki generation
        output_structure = {}

        # creates the engine properties map
        engine_properties = {
            "file_path" : wiki_file_path,
            "target_path" : base_target_path,
            "output_structure" : output_structure,
            "configuration_map" : configuration_map
        }

        # retrieves the language wiki plugin
        language_wiki_plugin = self.web_mvc_wiki_plugin.language_wiki_plugin

        # generates the html files using the wiki engine with the given engine properties
        language_wiki_plugin.generate("html", engine_properties)

    def _update_page(self, rest_request, page, instance_name):
        """
        Updates the page in the underlying repository structure.
        The updating of the page may involve the remote
        communication with the repository server.
        In case no page exists in the underlying repository a
        new page is created and persisted.

        @type rest_request: RestRequest
        @param rest_request: The current rest request in use
        for the handling.
        @type page: Dictionary
        @param page: The map containing the the page information
        (including name, summary and contents).
        @type instance_name: String
        @param instance_name: The name of the instance to be used
        in the updating of the page.
        @rtype: int
        @return: The revision number for the updated page.
        """

        # retrieves the plugin manager
        plugin_manager = self.web_mvc_wiki_plugin.manager

        # retrieves the revision control manager plugin
        revision_control_manager_plugin = self.web_mvc_wiki_plugin.revision_control_manager_plugin

        # retrieves the instance for the rest request
        instance = self.web_mvc_wiki._get_instance(instance_name)

        # retrieves the instance attributes
        instance_repository_path = instance["repository_path"]
        instance_repository_type = instance.get("repository_type",  None)
        instance_repository_arguments = instance.get("repository_arguments", None)

        # retrieves the page attributes
        page_name = page["name"]
        page_contents = page["contents"]
        page_summary = page.get("summary", DEFAULT_SUMMARY)

        # normalizes the contents
        normalized_contents = self._normalize_contents(page_contents)

        # sets the base file path as the instance repository path
        # resolved by the plugin manager
        base_file_path = plugin_manager.resolve_file_path(instance_repository_path)

        # creates the complete file path for the wiki file
        # joining the base file path and the wiki page name, then
        # checks if the file already exists (or not)
        complete_file_path = os.path.join(base_file_path, page_name + WIKI_EXTENSION)
        exists_file = os.path.exists(complete_file_path)

        # writes the normalized contents to the wiki file (in the complete file path)
        self._write_file(complete_file_path, normalized_contents)

        # in case no repository type is defined
        # for the instance (no repository)
        if not instance_repository_type:
            # returns immediately
            return None

        # defines the default repository arguments
        default_repository_arguments = {
            "repository_path" : base_file_path
        }

        # creates the revision control parameters and uses them to
        # loads a new revision control manager with the specified
        # adapter name (selects the adapter type)
        revision_control_parameters = colony.libs.map_util.map_extend(instance_repository_arguments, default_repository_arguments)
        revision_control_manager = revision_control_manager_plugin.load_revision_control_manager(instance_repository_type, revision_control_parameters)

        # in case the file is new uses the revision control manager
        # to add the file to the revision controller, then commits
        # the file to the revision control and retrieves the commit revision
        not exists_file and revision_control_manager.add([complete_file_path], True)
        commit_revision = revision_control_manager.commit([complete_file_path], page_summary)

        # returns the update revision
        return commit_revision

    def _get_file_contents(self, file_path):
        """
        Retrieves the contents of specified file.

        @type file_path: String
        @param file_path: The path to the file.
        """

        # opens the target file
        file = open(file_path, "rb")

        try:
            # reads the file contents
            file_contents = file.read()

            # returns the file contents
            return file_contents
        finally:
            # closes the target file
            file.close()

    def _get_file_contents_decoded(self, file_path, file_encoding):
        """
        Retrieves the contents of specified file in unicode.

        @type file_path: String
        @param file_path: The path to the file.
        @type file_encoding: String
        @param file_encoding: The encoding of the file.
        """

        # retrieves the file contents
        file_contents = self._get_file_contents(file_path)

        # decodes the file contents using the file encoding
        file_contents = file_contents.decode(file_encoding)

        # returns the file contents decoded
        return file_contents

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
