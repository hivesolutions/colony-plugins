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
    "default_end_points" : [("normal", "", 80, {}), ("ssl", "", 443, {})],
    "default_handler" : "file",
    "default_encoding" : None,
    "default_content_type_charset" : "utf-8",
    "default_client_connection_timeout" : 3,
    "default_connection_timeout" : 30,
    "default_request_timeout" : 30,
    "default_response_timeout" : 30,
    "default_number_threads" : 30,
    "default_scheduling_algorithm" : 2,
    "default_maximum_number_threads" : 60,
    "default_maximum_number_work_threads" : 15,
    "default_work_scheduling_algorithm" : 3,
    "preferred_error_handlers" : ["template", "default"],
    "log_file_path" : "%configuration:pt.hive.colony.plugins.main.service.http%/access.log",
    "allowed_hosts" : {
        "127.0.0.1" : True,
        "localhost" : True,
        "hive.pt" : True,
        "www.hive.pt" : True,
        "blog.hive.pt" : True,
        "openid.hive.pt" : True,
        "takethebill.com" : True,
        "www.takethebill.com" : True,
        "svn.hive.pt" : True,
        "trac.hive.pt" : True,
        "bargania.com" : True
    },
    "virtual_servers" : {
        "resolution_order" : ["blog.hive.pt", "openid.hive.pt", "takethebill.com", "svn.hive.pt", "trac.hive.pt", "bargania.com"],
        "blog.hive.pt" : {
            "redirections" : {
                "resolution_order" : ["/"],
                "/" : {
                    "target" : "/colony_mod_python/rest/mvc/hive_blog/",
                    "recursive_redirection" : True
                }
            }
        },
        "openid.hive.pt" : {
            "redirections" : {
                "resolution_order" : ["/"],
                "/" : {
                    "target" : "/colony_mod_python/rest/mvc/hive_openid/",
                    "recursive_redirection" : True
                }
            }
        },
        "takethebill.com" : {
            "redirections" : {
                "resolution_order" : ["/"],
                "/" : {
                    "target" : "/colony_mod_python/rest/mvc/take_the_bill/",
                    "recursive_redirection" : True
                }
            }
        },
        "svn.hive.pt" : {
            "redirections" : {
                "resolution_order" : ["/"],
                "/" : {
                    "target" : "/proxy_svn/",
                    "recursive_redirection" : True
                }
            }
        },
        "trac.hive.pt" : {
            "redirections" : {
                "resolution_order" : ["/"],
                "/" : {
                    "target" : "/proxy_trac/",
                    "recursive_redirection" : True
                }
            }
        },
        "bargania.com" : {
            "redirections" : {
                "resolution_order" : ["/"],
                "/" : {
                    "target" : "/colony_mod_python/rest/mvc/bargania_site/",
                    "recursive_redirection" : True
                }
            }
        }
    },
    "redirections" : {
        "resolution_order" : ["/manager",
                              "/blog",
                              "/openid",
                              "/take_the_bill",
                              "/"],
        "/manager" : {
            "target" : "/colony_mod_python/rest/mvc/web_mvc_manager/",
            "recursive_redirection" : True
        },
        "/blog" : {
            "target" : "/colony_mod_python/rest/mvc/hive_blog/",
            "recursive_redirection" : True
        },
        "/openid" : {
            "target" : "/colony_mod_python/rest/mvc/hive_openid/",
            "recursive_redirection" : True
        },
        "/take_the_bill" : {
            "target" : "/colony_mod_python/rest/mvc/take_the_bill/",
            "recursive_redirection" : True
        },
        "/" : {
            "target" : "/colony_mod_python/rest/mvc/hive_site/",
            "recursive_redirection" : True
        }
    },
    "contexts" : {
        "resolution_order" : ["/colony_web/plugins",
                              "/colony_web",
                              "/colony_manager",
                              "/colony_mod_python",
                              "/template_error_handler",
                              "/eclipse",
                              "/cgi-bin",
                              "/fastcgi-bin",
                              "/web_administration",
                              "/websession_test",
                              "/websession",
                              "/proxy_svn",
                              "/proxy_trac"],
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
        "/eclipse" : {
            "handler" : "file",
            "allow_redirection" : False,
            "request_properties" : {
                "base_path" : "$resource{system.path.base}/pt.hive.eclipse.plugins.site",
                "default_page" : "site.xml"
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
        "/proxy_svn" : {
            "handler" : "proxy",
            "allow_redirection" : False,
            "request_properties" : {
                "proxy_type" : "reverse",
                "proxy_target" : "http://svn.hive.pt:8080"
            }
        },
        "/proxy_trac" : {
            "handler" : "proxy",
            "allow_redirection" : False,
            "request_properties" : {
                "proxy_type" : "reverse",
                "proxy_target" : "http://trac.hive.pt:8080"
            }
        }
    }
}
