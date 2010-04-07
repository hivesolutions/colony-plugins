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

__revision__ = "$LastChangedRevision: 421 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2008-11-20 15:16:53 +0000 (Qui, 20 Nov 2008) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import urllib

DEFAULT_CONTENT_TYPE = "text/html;charset=utf-8"
""" The default content type """

DEFAULT_ENCODING = "utf-8"
""" The default encoding value """

BASE_PATH_VALUE = "base_path"
""" The base path value """

BACK_PATH_VALUE = "../"
""" The back path value """

def _start_controller(self):
    """
    Starts the controller structures.
    """

    # in case the controller has the start method
    if hasattr(self, "start"):
        # calls the start method
        # in the controller
        self.start()

def get_base_path(self, rest_request):
    """
    Retrieves the base path according to
    the current rest request path.

    @type rest_request: RestRequest
    @param rest_request: The rest request to be used to retrieve
    the base path.
    @rtype: String
    @return: The base path.
    """

    # retrieves the path list length
    path_list_length = len(rest_request.path_list)

    # creates the base path
    base_path = str()

    # iterates over all the path list length without
    # the delta value
    for _index in range(path_list_length - 2):
        # adds the back path to the base path
        base_path += BACK_PATH_VALUE

    # returns the base path
    return base_path

def set_contents(self, rest_request, contents = ""):
    # sets the content type for the rest request
    rest_request.set_content_type(DEFAULT_CONTENT_TYPE)

    # sets the result for the rest request
    rest_request.set_result_translated(contents)

    # flushes the rest request
    rest_request.flush()

def retrieve_template_file(self, file_name = None):
    # creates the template file path
    template_file_path = self.templates_path + "/" + file_name

    # parses the template file path
    template_file = self.template_engine_manager_plugin.parse_file_path_encoding(template_file_path, "Cp1252")

    # returns the template file
    return template_file

def apply_base_path_template_file(self, rest_request, template_file):
    """
    Applies the base path to the template file according to
    the current rest request path.

    @type rest_request: RestRequest
    @param rest_request: The rest request to be used to set the base path.
    @type template_file: TemplateFile
    @param template_file: The template to be "applied" with the base path.
    """

    # retrieves the base path
    base_path = self.get_base_path(rest_request);

    # assigns the area value
    template_file.assign(BASE_PATH_VALUE, base_path)

def get_session_attribute(self, rest_request, session_attribute_name):
    # tries to retrieve the rest request session
    rest_request_session = rest_request.get_session()

    # in case the rest request session
    # is invalid
    if not rest_request_session:
        # returns none (invalid)
        return None

    # retrieves the attribute from the session
    session_attribute = rest_request_session.get_attribute(session_attribute_name)

    # returns the session attribute
    return session_attribute

def set_session_attribute(self, rest_request, session_attribute_name, session_attribute_value):
    # tries to retrieve the rest request session
    rest_request_session = rest_request.get_session()

    # in case the rest request session
    # is invalid
    if not rest_request_session:
        # start a session if none is started
        rest_request.start_session()

        # retrieves the rest request session
        rest_request_session = rest_request.get_session()

    # sets the attribute in the session
    rest_request_session.set_attribute(session_attribute_name, session_attribute_value)

def get_attribute_decoded(self, rest_request, attribute_name, encoding = DEFAULT_ENCODING):
    # retrieves the attribute value from the attribute name
    attribute_value = rest_request.get_attribute(attribute_name)

    # in case the attribute value is valid
    if attribute_value:
        # unquotes the attribute value
        attribute_value_unquoted = urllib.unquote(attribute_value)

        # converts the spaces values
        attribute_value_spaced = attribute_value_unquoted.replace("+", " ")

        # decodes the attribute value
        attribute_value_decoded = attribute_value_spaced.decode(encoding)

        # the attribute value decoded
        return attribute_value_decoded
    else:
        # returns the empty value
        return ""

def get_templates_path(self):
    """
    Retrieves the templates path.

    @rtype: Sring
    @return: The templates path.
    """

    return self.templates_path

def set_templates_path(self, templates_path):
    """
    Sets the templates path.

    @type templates_path: String
    @param templates_path: The templates path.
    """

    self.templates_path = templates_path

def get_template_engine_manager_plugin(self):
    """
    Retrieves the template engine manager plugin.

    @rtype: Plugin
    @return: The template engine manager plugin.
    """

    return self.template_engine_manager_plugin

def set_template_engine_manager_plugin(self, template_engine_manager_plugin):
    """
    Sets the template engine manager plugin.

    @type template_engine_manager_plugin: String
    @param template_engine_manager_plugin: The templates path.
    """

    self.template_engine_manager_plugin = template_engine_manager_plugin
