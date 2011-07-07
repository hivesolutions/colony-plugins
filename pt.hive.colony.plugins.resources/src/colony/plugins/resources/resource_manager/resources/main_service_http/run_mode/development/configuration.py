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
    "default_end_points" : [
        (
            "normal", "", 8080, {}
        )
    ],
    "default_handler" : "file",
    "default_encoding" : None,
    "default_content_type_charset" : "utf-8",
    "default_service_type" : "async",
    "default_client_connection_timeout" : 3,
    "default_connection_timeout" : 30,
    "default_request_timeout" : 3,
    "default_response_timeout" : 30,
    "default_number_threads" : 1,
    "default_scheduling_algorithm" : 2,
    "default_maximum_number_threads" : 30,
    "default_maximum_number_work_threads" : 150,
    "default_work_scheduling_algorithm" : 3,
    "preferred_error_handlers" : [
        "template",
        "default"
    ],
    "verify_request" : False,
    "log_file_path" : "%configuration:pt.hive.colony.plugins.main.service.http%/access.log",
    "connectors" : [
        {
            "default_end_points" : [
                (
                    "normal", "", 8181, {}
                )
            ],
            "default_handler" : "file"
        }
    ],
    "virtual_servers" : {
        "resolution_order" : [
            "127.0.0.1", "panzerini.com"
        ],
        "127.0.0.1" : {
            "redirections" : {
                "resolution_order" : [
                    "/"
                ],
                "/" : {
                    "target" : "/colony_dynamic/rest/mvc/hive_blog/",
                    "recursive_redirection" : True
                }
            }
        },
        "panzerini.com" : {
            "redirections" : {
                "resolution_order" : [
                    "/"
                ],
                "/" : {
                    "target" : "/colony_dynamic/rest/mvc/panzerini_web_mvc/",
                    "recursive_redirection" : True
                }
            }
        }
    },
    "redirections" : {
        "resolution_order" : [
            "/push_apple",
            "/push",
            "/wiki",
            "/manager",
            "/hive",
            "/blog",
            "/media_dashboard",
            "/task_registry",
            "/openid",
            "/take_the_bill",
            "/a_la_carte",
            "/pecway",
            "/bargania",
            "/panzerini",
            "/encryption",
            "/"
        ],
        "/push_apple" : {
            "target" : "/colony_dynamic/rest/mvc/web_mvc_communication_push_apple/",
            "recursive_redirection" : True
        },
        "/push" : {
            "target" : "/colony_dynamic/rest/mvc/web_mvc_communication_push/",
            "recursive_redirection" : True
        },
        "/wiki" : {
            "target" : "/colony_dynamic/rest/mvc/wiki/",
            "recursive_redirection" : True
        },
        "/manager" : {
            "target" : "/colony_dynamic/rest/mvc/web_mvc_manager/",
            "recursive_redirection" : True
        },
        "/hive" : {
            "target" : "/colony_dynamic/rest/mvc/hive_site/",
            "recursive_redirection" : True
        },
        "/blog" : {
            "target" : "/colony_dynamic/rest/mvc/hive_blog/",
            "recursive_redirection" : True
        },
        "/media_dashboard" : {
            "target" : "/colony_dynamic/rest/mvc/media_dashboard/",
            "recursive_redirection" : True
        },
        "/task_registry" : {
            "target" : "/colony_dynamic/rest/mvc/task_registry/",
            "recursive_redirection" : True
        },
        "/openid" : {
            "target" : "/colony_dynamic/rest/mvc/hive_openid/",
            "recursive_redirection" : True
        },
        "/take_the_bill" : {
            "target" : "/colony_dynamic/rest/mvc/take_the_bill/",
            "recursive_redirection" : True
        },
        "/a_la_carte" : {
            "target" : "/colony_dynamic/rest/mvc/a_la_carte/",
            "recursive_redirection" : True
        },
        "/pecway" : {
            "target" : "/colony_dynamic/rest/mvc/pecway/",
            "recursive_redirection" : True
        },
        "/bargania" : {
            "target" : "/colony_dynamic/rest/mvc/bargania_site/",
            "recursive_redirection" : True
        },
        "/panzerini" : {
            "target" : "/colony_dynamic/rest/mvc/panzerini_web_mvc/",
            "recursive_redirection" : True
        },
        "/encryption" : {
            "target" : "/colony_dynamic/rest/mvc/web_mvc_encryption/",
            "recursive_redirection" : True
        },
        "/" : {
            "target" : "/welcome_handler/",
            "recursive_redirection" : True
        }
    },
    "contexts" : {
        "resolution_order" : [
            "/colony_web/plugins",
            "/colony_web",
            "/colony_manager",
            "/colony_dynamic",
            "/welcome_handler",
            "/system_information_handler",
            "/system_information",
            "/template_error_handler",
            "/template_directory_list_handler",
            "/eclipse",
            "/repository/ubuntu",
            "/repository/debian",
            "/cgi-bin",
            "/fastcgi-bin",
            "/wsgi-bin/simple_business_logic",
            "/wsgi-bin/remote_sql_service_foxpro",
            "/wsgi-bin/remote_sql_service_sqlite",
            "/wsgi-bin",
            "/web_administration",
            "/websession_test",
            "/websession",
            "/colony/repository",
            "/socket_bridge",
            "/system_unix",
            "/system_windows",
            "/proxy"
        ],
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
        "/colony_dynamic" : {
            "handler" : "colony",
            "allow_redirection" : False,
            "request_properties" : {}
        },
        "/welcome_handler" : {
            "handler" : "file",
            "allow_redirection" : False,
            "request_properties" : {
                "base_path" : "$plugin{pt.hive.colony.plugins.main.service.http.welcome_handler}/main_service_http_welcome_handler/welcome_handler/resources",
                "default_page" : "http_service_welcome.html"
            }
        },
        "/system_information_handler" : {
            "handler" : "file",
            "allow_redirection" : False,
            "request_properties" : {
                "base_path" : "$plugin{pt.hive.colony.plugins.main.service.http.system_information_handler}/main_service_http_system_information_handler/system_information_handler/resources"
            }
        },
        "/system_information" : {
            "handler" : "system_information",
            "allow_redirection" : False
        },
        "/template_error_handler" : {
            "handler" : "file",
            "allow_redirection" : False,
            "request_properties" : {
                "base_path" : "$plugin{pt.hive.colony.plugins.main.service.http.template_error_handler}/main_service_http_template_error_handler/template_error_handler/resources"
            }
        },
        "/template_directory_list_handler" : {
            "handler" : "file",
            "allow_redirection" : False,
            "request_properties" : {
                "base_path" : "$plugin{pt.hive.colony.plugins.main.service.http.template_directory_list_handler}/main_service_http_template_directory_list_handler/template_directory_list_handler/resources"
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
                "base_path" : "${HOME}/cgi-bin",
            }
        },
        "/fastcgi-bin" : {
            "handler" : "fast_cgi",
            "allow_redirection" : False,
            "request_properties" : {
                "handler_type" : "local",
                "base_path" : "${HOME}/fcgi-bin",
                "connection_type" : 1,
                "connection_arguments" : (
                    "localhost",
                    9010
                )
            }
        },
        "/wsgi-bin/simple_business_logic" : {
            "handler" : "wsgi",
            "authentication_handler" : "main",
            "allow_redirection" : False,
            "request_properties" : {
                "base_path" : "$resource{system.path.toolbox}/pt.hive.toolbox.simple_business_logic/src/toolbox/simple_business_logic_service/service",
                "module_name" : "simple_business_logic_service",
                "application_name" : "application"
            },
            "authentication_properties" : {
                "authentication_handler" : "python",
                "authentication_realm" : "system",
                "arguments" : {
                    "file_path" : "%configuration:pt.hive.colony.plugins.main.authentication.python_handler%/authentication.py"
                }
            }
        },
        "/wsgi-bin/remote_sql_service_foxpro" : {
            "handler" : "wsgi",
            "authentication_handler" : "main",
            "allow_redirection" : False,
            "request_properties" : {
                "base_path" : "$resource{system.path.toolbox}/pt.hive.toolbox.remote_sql_service/src/toolbox/remote_sql_service_foxpro/foxpro",
                "module_name" : "remote_sql_service_foxpro",
                "application_name" : "application"
            },
            "authentication_properties" : {
                "authentication_handler" : "python",
                "authentication_realm" : "system",
                "arguments" : {
                    "file_path" : "%configuration:pt.hive.colony.plugins.main.authentication.python_handler%/authentication.py"
                }
            }
        },
        "/wsgi-bin/remote_sql_service_sqlite" : {
            "handler" : "wsgi",
            "authentication_handler" : "main",
            "allow_redirection" : False,
            "request_properties" : {
                "base_path" : "$resource{system.path.toolbox}/pt.hive.toolbox.remote_sql_service/src/toolbox/remote_sql_service_sqlite/sqlite",
                "module_name" : "remote_sql_service_sqlite",
                "application_name" : "application"
            },
            "authentication_properties" : {
                "authentication_handler" : "python",
                "authentication_realm" : "system",
                "arguments" : {
                    "file_path" : "%configuration:pt.hive.colony.plugins.main.authentication.python_handler%/authentication.py"
                }
            }
        },
        "/wsgi-bin" : {
            "handler" : "wsgi",
            "allow_redirection" : False,
            "request_properties" : {
                "base_path" : "${HOME}/wsgi-bin",
                "module_name" : "server",
                "application_name" : "application"
            }
        },
        "/web_administration" : {
            "handler" : "file",
            "allow_redirection" : False,
            "request_properties" : {
                "base_path" : "$plugin{pt.hive.colony.plugins.web.administration}/web_administration/administration/resources"
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
        "/system_unix" : {
            "handler" : "file",
            "authentication_handler" : "main",
            "allow_redirection" : False,
            "request_properties" : {
                "base_path" : "/"
            },
            "authentication_properties" : {
                "authentication_handler" : "python",
                "authentication_realm" : "system",
                "arguments" : {
                    "file_path" : "%configuration:pt.hive.colony.plugins.main.authentication.python_handler%/authentication.py"
                }
            }
        },
        "/system_windows" : {
            "handler" : "file",
            "authentication_handler" : "main",
            "allow_redirection" : False,
            "request_properties" : {
                "base_path" : "c:/"
            },
            "authentication_properties" : {
                "authentication_handler" : "python",
                "authentication_realm" : "system",
                "arguments" : {
                    "file_path" : "%configuration:pt.hive.colony.plugins.main.authentication.python_handler%/authentication.py"
                }
            }
        },
        "/proxy" : {
            "handler" : "proxy",
            "allow_redirection" : False,
            "request_properties" : {
                "proxy_type" : "reverse",
                "proxy_target" : "http://www.hive.pt"
            }
        }
    }
}
