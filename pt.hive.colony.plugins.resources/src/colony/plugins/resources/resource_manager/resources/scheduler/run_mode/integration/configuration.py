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
    "sleep_step" : 0.5,
    "tasks" : [
        {
            "type" : "plugin",
            "plugin_id" : "pt.hive.colony.plugins.build.automation",
            "plugin_version" : "1.0.0",
            "method" : "run_automation",
            "arguments" : [
                "pt.hive.colony.plugins.build.automation.items.colony_integration",
                "1.0.0",
                "install",
                1
            ],
            "recursion_list" : [
                0, 0, 5, 0, 0
            ]
        },
        {
            "type" : "plugin",
            "plugin_id" : "pt.hive.colony.plugins.build.automation",
            "plugin_version" : "1.0.0",
            "method" : "run_automation",
            "arguments" : [
                "pt.hive.omni.plugins.build.automation.items.omni_integration",
                "1.0.0",
                "install",
                1
            ],
            "recursion_list" : [
                0, 0, 10, 0, 0
            ]
        },
        {
            "type" : "plugin",
            "plugin_id" : "pt.hive.colony.plugins.build.automation",
            "plugin_version" : "1.0.0",
            "method" : "run_automation",
            "arguments" : [
                "pt.hive.products.plugins.build.automation.items.products_integration",
                "1.0.0",
                "install",
                1
            ],
            "recursion_list" : [
                0, 0, 15, 0, 0
            ]
        },
        {
            "type" : "plugin",
            "plugin_id" : "pt.hive.hive_development.plugins.media_dashboard.updater.revision_control",
            "plugin_version" : "1.0.0",
            "method" : "update_media_dashboard",
            "arguments" : [
                {
                    "base_url" : "http://localhost:8080/media_dashboard/",
                    "bargania_base_url" : "http://bargania.com/",
                }
            ],
            "recursion_list" : [
                0, 0, 1, 0, 0
            ]
        },
        {
            "type" : "plugin",
            "plugin_id" : "pt.hive.hive_development.plugins.media_dashboard.updater.revision_control",
            "plugin_version" : "1.0.0",
            "method" : "update_media_dashboard",
            "arguments" : [
                {
                    "adapter_name" : "svn",
                    "revision_control_parameters" : {},
                    "repository_path" : "http://svn.hive.pt/hive-main",
                    "base_url" : "http://localhost:8080/media_dashboard/"
                }
            ],
            "recursion_list" : [
                0, 0, 1, 0, 0
            ]
        }
    ]
}
