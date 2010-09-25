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

__author__ = "Jo�o Magalh�es <joamag@hive.pt> & Lu�s Martinho <lmartinho@hive.pt>"
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
                 "default_end_points" : [("ssl", "", 443, {})],
                 "default_handler" : "file",
                 "default_encoding" : None,
                 "default_content_type_charset" : "utf-8",
                 "preferred_error_handlers" : ["template", "default"],
                 "allowed_hosts" : {"127.0.0.1" : True,
                                    "localhost" : True},
                 "redirections" : {
                     "resolution_order" : ["/manager"],
                     "/manager" : {
                         "target" : "/colony_mod_python/rest/mvc/web_mvc_manager/",
                         "recursive_redirection" : True
                     }
                 },
                 "contexts" : {
                     "resolution_order" : ["/colony_web/plugins",
                                           "/colony_web",
                                           "/colony_mod_python",
                                           "/"],
                     "/colony_web" : {
                         "handler" : "file",
                         "allow_redirection" : False,
                         "request_properties" : {
                             "base_path" : "$resource{system.path.colony_web}/pt.hive.colony.web",
                             "default_page" : "index.html"
                         }
                     },
                     "/colony_web/plugins" : {
                         "handler" : "colony",
                         "allow_redirection" : False,
                         "request_properties" : {
                             "plugin_handler" : "pt.hive.colony.plugins.javascript.file_handler"
                         }
                     },
                     "/colony_mod_python" : {
                         "handler" : "colony",
                         "allow_redirection" : False,
                         "request_properties" : {}
                     },
                     "/" : {
                         "handler" : "file",
                         "allow_redirection" : False,
                         "request_properties" : {
                             "base_path" : "$resource{system.path.colony_web}/pt.hive.colony.web",
                             "default_page" : "redirect.html"
                         }
                     }
                 }
             }
