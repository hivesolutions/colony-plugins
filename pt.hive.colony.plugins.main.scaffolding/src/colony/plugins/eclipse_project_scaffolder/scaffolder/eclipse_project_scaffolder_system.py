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

__author__ = "Tiago Silva <tsilva@hive.pt>"
""" The author(s) of the module """

__version__ = "1.0.0"
""" The version of the module """

__revision__ = "$LastChangedRevision: 72 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2008-10-21 23:29:54 +0100 (Ter, 21 Out 2008) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

DESTINATION_PATH_VALUE = "destination_path"
""" The destination path value """

TEMPLATE_PATH_VALUE = "template_path"
""" The template path value """

SCAFFOLDER_TYPE = "eclipse_project"
""" The scaffolder type """

TEMPLATES_PATH = "eclipse_project_scaffolder/scaffolder/resources/templates/"
""" The templates path """

TEMPLATES_SETTINGS_PATH = TEMPLATES_PATH + "settings/"
""" The templates settings path """

TEMPLATES = (
    {
        TEMPLATE_PATH_VALUE : TEMPLATES_SETTINGS_PATH + "org.eclipse.core.resources.prefs.tpl",
        DESTINATION_PATH_VALUE : ".settings/org.eclipse.core.resources.prefs"
    },
    {
        TEMPLATE_PATH_VALUE : TEMPLATES_PATH + "project.tpl",
        DESTINATION_PATH_VALUE : ".project"
    },
    {
        TEMPLATE_PATH_VALUE : TEMPLATES_PATH + "pydevproject.tpl",
        DESTINATION_PATH_VALUE : ".pydevproject"
    }
)
""" The templates """

class EclipseProjectScaffolder:
    """
    The eclipse project scaffolder.
    """

    eclipse_project_scaffolder_plugin = None
    """ The eclipse project scaffolder plugin """

    def __init__(self, eclipse_project_scaffolder_plugin):
        """
        Constructor of the class.

        @type eclipse_project_scaffolder_plugin: EclipseProjectScaffolderPlugin
        @param eclipse_project_scaffolder_plugin: The eclipse project scaffolder plugin.
        """

        self.eclipse_project_scaffolder_plugin = eclipse_project_scaffolder_plugin

    def get_scaffolder_type(self):
        return SCAFFOLDER_TYPE

    def get_templates(self, scaffold_attributes_map):
        return TEMPLATES

    def process_scaffold_attributes(self, scaffold_attributes_map):
        pass

    def process_template(self, template_path, template, scaffold_attributes_map):
        return template

    def generate_scaffold(self, scaffold_path, scaffold_attributes_map):
        pass
