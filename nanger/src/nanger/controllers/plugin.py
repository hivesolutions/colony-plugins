#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Colony Framework
# Copyright (c) 2008-2012 Hive Solutions Lda.
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

__revision__ = "$LastChangedRevision$"
""" The revision number of the module """

__date__ = "$LastChangedDate$"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008-2012 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import colony

import base

mvc_utils = colony.__import__("mvc_utils")

class PluginController(base.BaseController):

    def list(self, rest_request):
        # retrieves the reference to the plugin manager running
        # in the current context
        plugin_manager = self.plugin.manager

        # retrieves the json plugin for the encoding of the
        # response value (serialized value)
        json_plugin = self.plugin.json_plugin

        # retrieves the various fields that are going to be used to
        # perform the query over the plugins
        filter = self.get_field(rest_request, "filter_string", "")
        start_record = self.get_field(rest_request, "start_record", 0, int)
        number_records = self.get_field(rest_request, "number_records", 9, int)

        # uses the plugin manager to retrieve the list of all plugin instances
        # (this is a list of object and as such is not serializable)
        loaded_plugins = plugin_manager.get_all_plugins()

        # creates the list that will hold the various plugin description maps
        # to be generates for the filtered plugins
        plugins = []

        # converts the filter into a lower cased representation to be able to
        # perform a case insensitive comparison
        _filter = filter.lower()

        # iterates over all the loaded plugins to be able to filter the ones
        # that comply with the provided query
        for loaded_plugin in loaded_plugins:
            # converts the plugin identifier and name into lower cased
            # values for the comparison and then performs it in case
            # the comparison fails continues the loop immediately
            id = loaded_plugin.id.lower()
            name = loaded_plugin.name.lower()
            if not id.startswith(_filter) and not name.startswith(_filter): continue

            # creates the plugin map containing the identifier and the
            # name of the plugin and then adds it to the plugins list
            plugin = {
                "id" : loaded_plugin.id,
                "name" : loaded_plugin.name,
                "short_name" : loaded_plugin.short_name
            }
            plugins.append(plugin)

        # sorts the plugins list using the default alphabetic order and
        # then serializes the same plugin list using the defined plugin
        plugins.sort()
        plugins = plugins[start_record:start_record + number_records]
        self.serialize(rest_request, plugins, serializer = json_plugin)

    def show(self, rest_request, plugin_id = None):
        # retrieves the reference to the plugin manager running
        # in the current context
        plugin_manger = self.plugin.manager

        # retrieves the identifier of the plugin to be used for the
        # current request and tries to retrieve the associated plugin
        # from the plugin manager, in case it fails raises exception
        plugin = plugin_manger._get_plugin(plugin_id)
        if not plugin: raise RuntimeError("Plugin '%s' not found" % plugin_id)

        # generates and processes the template with the provided values
        # changing the current rest request accordingly, note that there's
        # a defined partial page and a base template value defined
        self._template(
            rest_request = rest_request,
            template = "plugin/show.html.tpl",
            title = plugin.name,
            area = "plugins",
            section = "plugins.html.tpl",
            sub_area = "info",
            plugin = plugin
        )

    def load(self, rest_request, plugin_id = None):
        # retrieves the reference to the plugin manager running
        # in the current context
        plugin_manger = self.plugin.manager

        # retrieves the identifier of the plugin to be used for the
        # current request and tries to retrieve the associated plugin
        # from the plugin manager, in case it fails raises exception
        plugin = plugin_manger._get_plugin(plugin_id)
        if not plugin: raise RuntimeError("Plugin '%s' not found" % plugin_id)

        # loads the just retrieved plugin using its main identifier as
        # the trigger element for the loading
        plugin_manger.load_plugin(plugin.id)

        # redirects the user agent to the show page for the plugin
        # instance (default behavior)
        self.redirect_base_path(rest_request, "plugins/%s" % plugin.short_name)

    def unload(self, rest_request, plugin_id = None):
        # retrieves the reference to the plugin manager running
        # in the current context
        plugin_manger = self.plugin.manager

        # retrieves the identifier of the plugin to be used for the
        # current request and tries to retrieve the associated plugin
        # from the plugin manager, in case it fails raises exception
        plugin = plugin_manger._get_plugin(plugin_id)
        if not plugin: raise RuntimeError("Plugin '%s' not found" % plugin_id)

        # unloads the just retrieved plugin using its main identifier as
        # the trigger element for the loading
        plugin_manger.unload_plugin(plugin.id)

        # redirects the user agent to the show page for the plugin
        # instance (default behavior)
        self.redirect_base_path(rest_request, "plugins/%s" % plugin.short_name)

    def reload(self, rest_request, plugin_id = None):
        # retrieves the reference to the plugin manager running
        # in the current context
        plugin_manger = self.plugin.manager

        # retrieves the identifier of the plugin to be used for the
        # current request and tries to retrieve the associated plugin
        # from the plugin manager, in case it fails raises exception
        plugin = plugin_manger._get_plugin(plugin_id)
        if not plugin: raise RuntimeError("Plugin '%s' not found" % plugin_id)

        # loads and then unloads (reloading process) the just retrieved
        # plugin using its main identifier as the trigger element for the loading
        plugin_manger.unload_plugin(plugin.id)
        plugin_manger.load_plugin(plugin.id)

        # redirects the user agent to the show page for the plugin
        # instance (default behavior)
        self.redirect_base_path(rest_request, "plugins/%s" % plugin.short_name)
