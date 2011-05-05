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

__revision__ = "$LastChangedRevision$"
""" The revision number of the module """

__date__ = "$LastChangedDate$"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import wx.lib.customtreectrl

import misc_gui.tree_visualizer.tree_visualizer_system

class PluginManagerPanel(misc_gui.tree_visualizer.tree_visualizer_system.TreeVisualizerPanel):
    """
    The plugin manager panel class.
    """

    plugin_nodes_map = {}
    """ The plugin nodes map """

    def __init__(self, parent, parent_plugin):
        """
        Constructor of the class.

        @type parent: Object
        @param parent: The parent component
        @type parent_plugin: Plugin
        @param parent_plugin: The parent plugin.
        """

        misc_gui.tree_visualizer.tree_visualizer_system.TreeVisualizerPanel.__init__(self, parent, parent_plugin)
        self.tree.Bind(wx.lib.customtreectrl.EVT_TREE_ITEM_HYPERLINK, self.on_hyperlink)
        self.tree.Bind(wx.lib.customtreectrl.EVT_TREE_ITEM_CHECKED, self.on_checked)

    def on_hyperlink(self, evt):
        (plugin_id, version) = self.tree.GetItemPyData(evt._item)
        self.select_plugin(plugin_id, version)

    def on_checked(self, evt):
        item = evt.GetItem()
        (plugin_id, _plugin_version) = self.tree.GetItemPyData(item)
        if item._checked:
            self.parent_plugin.manager.load_plugin(plugin_id)
        else:
            self.parent_plugin.manager.unload_plugin(plugin_id)
        self.check_plugin_nodes()

    def check_plugin_nodes(self):
        self.Freeze()
        for (plugin_id, plugin_version) in self.plugin_nodes_map:
            item = self.plugin_nodes_map[(plugin_id, plugin_version)]
            if self.parent_plugin.manager.plugin_instances_map[plugin_id].is_loaded():
                item._checked = True
            else:
                item._checked = False
        self.Thaw()

    def select_plugin(self, plugin_id, plugin_version):
        self.tree.ToggleItemSelection(self.plugin_nodes_map[(plugin_id, plugin_version)])
        self.tree.Expand(self.plugin_nodes_map[(plugin_id, plugin_version)])

    def add_capabilities(self, node, plugin):
        if len(plugin.capabilities) > 0:
            capabilities_node = self.add_item(node, "Capabilities", 0)
            for capability in plugin.capabilities:
                capability_node = self.add_item(capabilities_node, "capability = \"%s\"" % capability, 0)
                plugin_list = self.parent_plugin.manager._get_plugins_allow_capability(capability)
                for plugin in plugin_list:
                    item_node = self.add_item(capability_node, "capability consumer plugin id = \"%s\"" % plugin.id, 0)
                    self.tree.SetItemHyperText(item_node, True)
                    self.tree.SetItemPyData(item_node, (plugin.id, plugin.version))

    def add_capabilities_allowed(self, node, plugin):
        if len(plugin.capabilities_allowed) > 0:
            # ads the capabilities allowed node label
            capabilities_allowed_node = self.add_item(node, "Capabilities allowed", 0)

            # retrieves the capabilities allowed (names) from the plugin
            capabilities_allowed = plugin._get_capabilities_allowed_names()

            # iterates over all the allowed capabilities
            for capability_allowed in capabilities_allowed:
                capability_node = self.add_item(capabilities_allowed_node, "capability allowed = \"%s\"" % str(capability_allowed), 0)
                plugin_list = self.parent_plugin.manager._get_plugins_by_capability(capability_allowed)
                for plugin in plugin_list:
                    item_node = self.add_item(capability_node, "capability provider plugin id = \"%s\"" % plugin.id, 0)
                    self.tree.SetItemHyperText(item_node, True)
                    self.tree.SetItemPyData(item_node, (plugin.id, plugin.version))

    def add_dependencies(self, node, plugin):
        if len(plugin.dependencies) > 0:
            package_list = []
            plugin_list = []
            for dependency in plugin.dependencies:
                if dependency.__class__.__name__ == "PluginDependency":
                    plugin_list.append(dependency)
                elif dependency.__class__.__name__ == "PackageDependency":
                    package_list.append(dependency)
            dependencies_node = self.add_item(node, "Dependencies", 0)
            if len(package_list) > 0:
                package_dependencies_node = self.add_item(dependencies_node, "Package dependencies", 0)
                for package_dependency in package_list:
                    package_node = self.add_item(package_dependencies_node, package_dependency.package_name + " v" + package_dependency.package_version, 0)
                    self.add_item(package_node, "name = \"%s\"" % package_dependency.package_name, 0)
                    self.add_item(package_node, "import name = \"%s\"" % package_dependency.package_import_name, 0)
                    self.add_item(package_node, "version = \"%s\"" % package_dependency.package_version, 0)
                    self.add_item(package_node, "url = \"%s\"" % package_dependency.package_url, 0)
            if len(plugin_list) > 0:
                plugin_dependencies_node = self.add_item(dependencies_node, "Plugin dependencies", 0)
                for plugin_dependency in plugin_list:
                    item_node = self.add_item(plugin_dependencies_node, "plugin dependency id = \"%s\"" % plugin_dependency.plugin_id, 0)
                    self.tree.SetItemHyperText(item_node, True)
                    self.tree.SetItemPyData(item_node, (plugin_dependency.plugin_id, plugin_dependency.plugin_version))
            plugin_list = self.parent_plugin.manager._get_plugins_by_dependency(plugin.id)
            if len(plugin_list) > 0:
                dependent_plugins_node = self.add_item(dependencies_node, "Dependent plugins", 0)
                for dependent_plugin in plugin_list:
                    item_node = self.add_item(dependent_plugins_node, "dependent plugin id = \"%s\"" % dependent_plugin.id, 0)
                    self.tree.SetItemHyperText(item_node, True)
                    self.tree.SetItemPyData(item_node, (dependent_plugin.id, dependent_plugin.version))

    def add_events_handled(self, node, plugin):
        if len(plugin.events_handled) > 0:
            events_handled_node = self.add_item(node, "Events handled", 0)
            for event_handled in plugin.events_handled:
                event_handled_node = self.add_item(events_handled_node, "event handled = \"%s\"" % event_handled, 0)
                plugin_list = self.parent_plugin.manager._get_plugins_by_event_registrable(event_handled)
                for plugin in plugin_list:
                    item_node = self.add_item(event_handled_node, "event provider plugin id = \"%s\"" % plugin.id, 0)
                    self.tree.SetItemHyperText(item_node, True)
                    self.tree.SetItemPyData(item_node, (plugin.id, plugin.version))

    def add_events_registrable(self, node, plugin):
        if len(plugin.events_registrable) > 0:
            events_registrable_node = self.add_item(node, "Events registrable", 0)
            for event_registrable in plugin.events_registrable:
                event_registrable_node = self.add_item(events_registrable_node, "event registrable = \"%s\"" % event_registrable, 0)
                plugin_list = self.parent_plugin.manager._get_plugins_by_event_handled(event_registrable)
                for plugin in plugin_list:
                    item_node = self.add_item(event_registrable_node, "event consumer plugin id = \"%s\"" % plugin.id, 0)
                    self.tree.SetItemHyperText(item_node, True)
                    self.tree.SetItemPyData(item_node, (plugin.id, plugin.version))

    def add_plugin(self, node, plugin):
        plugin_node = self.add_item(node, plugin.name + " v" + plugin.version, 1)
        self.tree.SetItemPyData(plugin_node, (plugin.id, plugin.version))
        self.plugin_nodes_map[(plugin.id, plugin.version)] = plugin_node
        self.add_item(plugin_node, "id = \"%s\"" % plugin.id, 0)
        self.add_item(plugin_node, "name = \"%s\"" % plugin.name, 0)
        self.add_item(plugin_node, "short_name = \"%s\"" % plugin.short_name, 0)
        self.add_item(plugin_node, "description = \"%s\"" % plugin.description, 0)
        self.add_item(plugin_node, "version = \"%s\"" % plugin.version, 0)
        self.add_item(plugin_node, "author = \"%s\"" % plugin.author, 0)
        self.add_capabilities(plugin_node, plugin)
        self.add_capabilities_allowed(plugin_node, plugin)
        self.add_dependencies(plugin_node, plugin)
        self.add_events_handled(plugin_node, plugin)
        self.add_events_registrable(plugin_node, plugin)

    def refresh_tree(self):
        # constructs the plugin nodes map
        self.plugin_nodes_map = {}

        # retrieves the list of plugins
        plugin_list_original = self.parent_plugin.manager.get_all_plugins()

        # creates an empty list to support the duplicated plugin references
        plugin_list = []

        # extends the list with the old list contains
        plugin_list.extend(plugin_list_original)

        # sorts the plugins
        plugin_list.sort()

        # sets the root node
        self.set_root("Plugins")

        self.node_list = [
            self.tree.GetRootItem()
        ]

        for plugin in plugin_list:
            self.add_plugin(self.tree.GetRootItem(), plugin)
        self.check_plugin_nodes()
        self.tree.Expand(self.tree.GetRootItem())
