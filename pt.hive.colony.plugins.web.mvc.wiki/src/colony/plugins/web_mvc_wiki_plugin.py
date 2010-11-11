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

__revision__ = "$LastChangedRevision: 684 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2008-12-08 15:16:55 +0000 (Seg, 08 Dez 2008) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import colony.base.plugin_system

class WebMvcWikiPlugin(colony.base.plugin_system.Plugin):
    """
    The main class for the Web Mvc Wiki plugin.
    """

    id = "pt.hive.colony.plugins.web.mvc.wiki"
    name = "Web Mvc Wiki Plugin"
    short_name = "Web Mvc Wiki"
    description = "The plugin that offers a web wiki service"
    version = "1.0.0"
    author = "Hive Solutions Lda. <development@hive.pt>"
    loading_type = colony.base.plugin_system.EAGER_LOADING_TYPE
    platforms = [colony.base.plugin_system.CPYTHON_ENVIRONMENT]
    attributes = {"build_automation_file_path" : "$base{plugin_directory}/web_mvc_wiki/mvc_wiki/resources/baf.xml"}
    capabilities = ["web.mvc_service", "build_automation_item"]
    capabilities_allowed = []
    dependencies = [colony.base.plugin_system.PluginDependency(
                    "pt.hive.colony.plugins.web.mvc.utils", "1.0.0"),
                    colony.base.plugin_system.PluginDependency(
                    "pt.hive.colony.plugins.language.wiki", "1.0.0"),
                     colony.base.plugin_system.PluginDependency(
                    "pt.hive.colony.plugins.main.cache.manager", "1.0.0"),
                    colony.base.plugin_system.PluginDependency(
                    "pt.hive.colony.plugins.revision_control.manager", "1.0.0"),
                    colony.base.plugin_system.PluginDependency(
                    "pt.hive.colony.plugins.misc.string_normalization", "1.0.0")]
    events_handled = []
    events_registrable = []
    main_modules = ["web_mvc_wiki.mvc_wiki.web_mvc_wiki_system"]

    web_mvc_wiki = None

    web_mvc_utils_plugin = None
    language_wiki_plugin = None
    main_cache_manager_plugin = None
    revision_control_manager_plugin = None
    string_normalization_plugin = None

    def load_plugin(self):
        colony.base.plugin_system.Plugin.load_plugin(self)
        global web_mvc_wiki
        import web_mvc_wiki.mvc_wiki.web_mvc_wiki_system
        self.web_mvc_wiki = web_mvc_wiki.mvc_wiki.web_mvc_wiki_system.WebMvcWiki(self)

    def end_load_plugin(self):
        colony.base.plugin_system.Plugin.end_load_plugin(self)
        self.web_mvc_wiki.load_components()

    def unload_plugin(self):
        colony.base.plugin_system.Plugin.unload_plugin(self)

    def end_unload_plugin(self):
        colony.base.plugin_system.Plugin.end_unload_plugin(self)

    def load_allowed(self, plugin, capability):
        colony.base.plugin_system.Plugin.load_allowed(self, plugin, capability)

    def unload_allowed(self, plugin, capability):
        colony.base.plugin_system.Plugin.unload_allowed(self, plugin, capability)

    @colony.base.decorators.inject_dependencies("pt.hive.colony.plugins.web.mvc.wiki", "1.0.0")
    def dependency_injected(self, plugin):
        colony.base.plugin_system.Plugin.dependency_injected(self, plugin)

    @colony.base.decorators.set_configuration_property("pt.hive.colony.plugins.web.mvc.wiki", "1.0.0")
    def set_configuration_property(self, property_name, property):
        colony.base.plugin_system.Plugin.set_configuration_property(self, property_name, property)

    @colony.base.decorators.unset_configuration_property("pt.hive.colony.plugins.web.mvc.wiki", "1.0.0")
    def unset_configuration_property(self, property_name):
        colony.base.plugin_system.Plugin.unset_configuration_property(self, property_name)

    def get_patterns(self):
        """
        Retrieves the tuple of regular expressions to be used as patterns,
        to the web mvc service. The tuple should relate the route with the handler
        method/function.

        @rtype: Tuple
        @return: The tuple of regular expressions to be used as patterns,
        to the web mvc service.
        """

        return self.web_mvc_wiki.get_patterns()

    def get_communication_patterns(self):
        """
        Retrieves the tuple of regular expressions to be used as communication patterns,
        to the web mvc service. The tuple should relate the route with a tuple
        containing the data handler, the connection changed handler and the name
        of the connection.

        @rtype: Tuple
        @return: The tuple of regular expressions to be used as communication patterns,
        to the web mvc service.
        """

        return self.web_mvc_wiki.get_communication_patterns()

    def get_resource_patterns(self):
        """
        Retrieves the tuple of regular expressions to be used as resource patterns,
        to the web mvc service. The tuple should relate the route with the base
        file system path to be used.

        @rtype: Tuple
        @return: The tuple of regular expressions to be used as resource patterns,
        to the web mvc service.
        """

        return self.web_mvc_wiki.get_resource_patterns()

    def get_web_mvc_utils_plugin(self):
        return self.web_mvc_utils_plugin

    @colony.base.decorators.plugin_inject("pt.hive.colony.plugins.web.mvc.utils")
    def set_web_mvc_utils_plugin(self, web_mvc_utils_plugin):
        self.web_mvc_utils_plugin = web_mvc_utils_plugin

    def get_language_wiki_plugin(self):
        return self.language_wiki_plugin

    @colony.base.decorators.plugin_inject("pt.hive.colony.plugins.language.wiki")
    def set_language_wiki_plugin(self, language_wiki_plugin):
        self.language_wiki_plugin = language_wiki_plugin

    def get_main_cache_manager_plugin(self):
        return self.main_cache_manager_plugin

    @colony.base.decorators.plugin_inject("pt.hive.colony.plugins.main.cache.manager")
    def set_main_cache_manager_plugin(self, main_cache_manager_plugin):
        self.main_cache_manager_plugin = main_cache_manager_plugin

    def get_revision_control_manager_plugin(self):
        return self.revision_control_manager_plugin

    @colony.base.decorators.plugin_inject("pt.hive.colony.plugins.revision_control.manager")
    def set_revision_control_manager_plugin(self, revision_control_manager_plugin):
        self.revision_control_manager_plugin = revision_control_manager_plugin

    def get_string_normalization_plugin(self):
        return self.string_normalization_plugin

    @colony.base.decorators.plugin_inject("pt.hive.colony.plugins.misc.string_normalization")
    def set_string_normalization_plugin(self, string_normalization_plugin):
        self.string_normalization_plugin = string_normalization_plugin

    @colony.base.decorators.set_configuration_property_method("configuration")
    def configuration_set_configuration_property(self, property_name, property):
        self.web_mvc_wiki.set_configuration_property(property)

    @colony.base.decorators.unset_configuration_property_method("configuration")
    def configuration_unset_configuration_property(self, property_name):
        self.web_mvc_wiki.unset_configuration_property()
