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
                 "verify_request" : False,
                 "connectors" : [
                     {"default_port" : 8181,
                      "default_handler" : "file"}
                 ],
                 "virtual_servers" : {
                     "resolution_order" : ["127.0.0.1"],
                     "127.0.0.1" : {
                         "redirections" : {
                             "resolution_order" : ["/"],
                             "/" : {
                                 "target" : "/colony_mod_python/rest/mvc/hive_blog/",
                                 "recursive_redirection" : True
                             }
                         }
                     }
                 },
                 "redirections" : {
                     "resolution_order" : ["/push",
                                           "/wiki",
                                           "/manager",
                                           "/blog",
                                           "/colony_site",
                                           "/take_the_bill",
                                           "/a_la_carte",
                                           "/"],
                     "/push" : {
                         "target" : "/colony_mod_python/rest/mvc/web_mvc_communication_push/",
                         "recursive_redirection" : True
                     },
                     "/wiki" : {
                         "target" : "/colony_mod_python/rest/mvc/wiki/",
                         "recursive_redirection" : True
                     },
                     "/manager" : {
                         "target" : "/colony_mod_python/rest/mvc/web_mvc_manager/",
                         "recursive_redirection" : True
                     },
                     "/blog" : {
                         "target" : "/colony_mod_python/rest/mvc/hive_blog/",
                         "recursive_redirection" : True
                     },
                     "/colony_site" : {
                         "target" : "/colony_mod_python/rest/mvc/colony_site/",
                         "recursive_redirection" : True
                     },
                     "/take_the_bill" : {
                         "target" : "/colony_mod_python/rest/mvc/take_the_bill/",
                         "recursive_redirection" : True
                     },
                     "/a_la_carte" : {
                         "target" : "/colony_mod_python/rest/mvc/a_la_carte/",
                         "recursive_redirection" : True
                     },
                     "/" : {
                         "target" : "/colony_mod_python/rest/mvc/hive/",
                         "recursive_redirection" : True
                     }
                 },
                 "contexts" : {
                     "resolution_order" : ["/colony_web/plugins",
                                           "/colony_web",
                                           "/colony_manager",
                                           "/colony_mod_python",
                                           "/template_error_handler",
                                           "/template_directory_list_handler",
                                           "/eclipse",
                                           "/repository/ubuntu",
                                           "/repository/debian",
                                           "/cgi-bin",
                                           "/fastcgi-bin",
                                           "/web_administration",
                                           "/websession_test",
                                           "/websession",
                                           "/colony/repository",
                                           "/socket_bridge",
                                           "/system"],
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
                     "/colony_manager" : {
                         "handler" : "colony",
                         "allow_redirection" : False,
                         "request_properties" : {}
                     },
                     "/colony_mod_python" : {
                         "handler" : "colony",
                         "allow_redirection" : False,
                         "request_properties" : {}
                     },
                     "/template_error_handler" : {
                         "handler" : "file",
                         "allow_redirection" : False,
                         "request_properties" : {
                             "base_path" : "$resource{system.path.colony}/pt.hive.colony.plugins.main.service.http/src/colony/plugins/main_service_http_template_error_handler/template_error_handler/resources"
                         }
                     },
                     "/template_directory_list_handler" : {
                         "handler" : "file",
                         "allow_redirection" : False,
                         "request_properties" : {
                             "base_path" : "$resource{system.path.colony}/pt.hive.colony.plugins.main.service.http/src/colony/plugins/main_service_http_file_handler/file_handler/resources"
                         }
                     },
                     "/eclipse" : {
                         "handler" : "file",
                         "allow_redirection" : False,
                         "request_properties" : {
                             "base_path" : "$resource{system.path.base}/pt.hive.eclipse.plugins.site",
                             "default_page" : "site.xml"
                         }
                     },
                     "/repository/ubuntu" : {
                         "handler" : "file",
                         "allow_redirection" : False,
                         "request_properties" : {
                             "base_path" : "$resource{colony.manager_path}/tmp/target/repository",
                         }
                     },
                     "/repository/debian" : {
                         "handler" : "file",
                         "allow_redirection" : False,
                         "request_properties" : {
                             "base_path" : "$resource{colony.manager_path}/tmp/target/repository",
                         }
                     },
                     "/cgi-bin" : {
                         "handler" : "cgi",
                         "allow_redirection" : False,
                         "request_properties" : {
                             "base_path" : "${HOME}",
                         }
                     },
                     "/fastcgi-bin" : {
                         "handler" : "fast_cgi",
                         "allow_redirection" : False,
                         "request_properties" : {
                             "handler_type" : "local",
                             "base_path" : "${HOME}",
                             "connection_type" : 1,
                             "connection_arguments" : ("localhost", 9010)
                         }
                     },
                     "/web_administration" : {
                         "handler" : "file",
                         "allow_redirection" : False,
                         "request_properties" : {
                             "base_path" : "$resource{system.path.colony}/pt.hive.colony.plugins.web.administration/src/colony/plugins/web_administration/administration/resources"
                         }
                     },
                     "/websession_test" : {
                         "handler" : "file",
                         "allow_redirection" : False,
                         "request_properties" : {
                             "base_path" : "c:/test",
                             "default_page" : "index.html"
                         }
                     },
                     "/websession" : {
                         "handler" : "websocket",
                         "allow_redirection" : False,
                         "request_properties" : {
                             "protocol" : "default"
                         }
                     },
                     "/colony/repository" : {
                         "handler" : "file",
                         "allow_redirection" : False,
                         "request_properties" : {
                             "base_path" : "$resource{system.path.colony}/pt.hive.colony.plugin_repository"
                         }
                     },
                     "/socket_bridge" : {
                         "handler" : "file",
                         "allow_redirection" : False,
                         "request_properties" : {
                             "base_path" : "$resource{system.path.colony}/hive_colony_socket_bridge"
                         }
                     },
                     "/system" : {
                         "handler" : "file",
                         "allow_redirection" : False,
                         "request_properties" : {
                             "base_path" : "C:/"
                         }
                     }
                 }
             }
