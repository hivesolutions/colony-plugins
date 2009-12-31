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

__revision__ = "$LastChangedRevision: 2341 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2009-04-01 17:42:37 +0100 (qua, 01 Abr 2009) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

configuration = {
                 "default_socket_provider" : "normal",
                 "default_port" : 8080,
                 "default_handler" : "file",
                 "default_encoding" : None,
                 "default_content_type_charset" : "utf-8",
                 "preferred_error_handlers" : ["template", "default"],
                 "contexts" : {
                     "resolution_order" : ["/colony_web/plugins", "/colony_web", "/colony_manager", "/colony_mod_python", "/template_error_handler", "/docs", "/eclipse", "/cgi-bin", "/fastcgi-bin", "/web_administration"],
                     "/colony_web" : {
                         "handler" : "file",
                         "request_properties" : {
                             "base_path" : "$resource{system.path.colony_web}/pt.hive.colony.web",
                             "default_page" : "index.html"
                         }
                     },
                     "/colony_web/plugins" : {
                         "handler" : "colony",
                         "request_properties" : {
                             "plugin_handler" : "pt.hive.colony.plugins.javascript.file_handler"
                         }
                     },
                     "/colony_manager" : {
                         "handler" : "colony",
                         "request_properties" : {}
                     },
                     "/colony_mod_python" : {
                         "handler" : "colony",
                         "request_properties" : {}
                     },
                     "/template_error_handler" : {
                         "handler" : "file",
                         "request_properties" : {
                             "base_path" : "$resource{system.path.colony}/pt.hive.colony.plugins.main.service.http/src/colony/plugins/main_service_http_template_error_handler/template_error_handler/resources"
                         }
                     },
                     "/docs" : {
                         "handler" : "file",
                         "request_properties" : {
                             "base_path" : "$resource{system.path.colony}/pt.hive.colony.documentation.technical/generated",
                             "default_page" : "documentation_index.xhtml"
                         }
                     },
                     "/eclipse" : {
                         "handler" : "file",
                         "request_properties" : {
                             "base_path" : "${WORKSPACE_HOME}/pt.hive.eclipse.plugins.site",
                             "default_page" : "site.xml"
                         }
                     },
                     "/cgi-bin" : {
                         "handler" : "cgi",
                         "request_properties" : {
                             "base_path" : "${HOME}",
                         }
                     },
                     "/fastcgi-bin" : {
                         "handler" : "fast_cgi",
                         "request_properties" : {
                             "handler_type" : "local",
                             "base_path" : "${HOME}",
                             "connection_type" : 1,
                             "connection_arguments" : ("localhost", 9010)
                         }
                     },
                     "/web_administration" : {
                         "handler" : "file",
                         "request_properties" : {
                             "base_path" : "$resource{system.path.colony}/pt.hive.colony.plugins.web.administration/src/colony/plugins/web_administration/administration/resources"
                         }
                     },
                 }
             }
