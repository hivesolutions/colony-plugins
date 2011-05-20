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

__author__ = "João Magalhães <joamag@hive.pt> & Tiago Silva <tsilva@hive.pt>"
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

import types

import wx.lib.customtreectrl

import colony.libs.structures_util

BOLD_VALUE = "bold"
""" The bold value """

CAPABILITIES_VALUE = "capabilities"
""" The capabilities value """

CAPABILITIES_ALLOWED_VALUE = "capabilities_allowed"
""" The capabilities allowed value """

CHECKABLE_VALUE = "checkable"
""" The checkable value """

CHECKED_VALUE = "checked"
""" The checked value """

CHILD_NODES_VALUE = "child_nodes"
""" The child nodes value """

DEPENDENCIES_VALUE = "dependencies"
""" The dependencies value """

TEXT_VALUE = "text"
""" The text value """

LINK_VALUE = "link"
""" The link value """

LOADED_VALUE = "loaded"
""" The loaded value """

IMAGE_WIDTH = 16
""" The image width """

IMAGE_HEIGHT = 16
""" The image height """

FAKE_NODE_ID_FORMAT = "%s_fake"
""" The fake node id format """

NODE_ATTRIBUTE_FORMAT = "%s.%s"
""" The node attribute format """

PLUGIN_NAME_FORMAT = "%s v%s"
""" The plugin text format """

PLUGIN_DEPENDENCY_CLASS_NAME = "PluginDependency"
""" The plugin dependency class text """

ROOT_NODE_ID = "root"
""" The root node id """

IMAGE_SIZE = (
    IMAGE_WIDTH,
    IMAGE_HEIGHT
)
""" The image size """

class PluginManagerInterface:
    """
    The plugin manager interface class.
    """

    plugin_manager_interface_plugin = None
    """ The plugin manager interface plugin """

    def __init__(self, plugin_manager_interface_plugin):
        """
        Constructor of the class.

        @type plugin_manager_interface_plugin: PluginManagerInterfacePlugin
        @param plugin_manager_interface_plugin: The plugin manager interface plugin.
        """

        self.plugin_manager_interface_plugin = plugin_manager_interface_plugin

    def do_panel(self, parent_widget):
        # creates the plugin manager panel
        plugin_manager_panel = PluginManagerPanel(self, parent_widget)

        # returns the plugin manager panel
        return plugin_manager_panel

class PluginManagerPanel(wx.Panel):
    """
    The plugin manager panel class.
    """

    plugin_manager_interface = None
    """ The plugin manager interface """

    tree_map = {}
    """ The data that is represented in the tree """

    node_map = {}
    """ The node information indexed by node id """

    node_item_map = {}
    """ The node items index by node id """

    dirty_node_map = {}
    """ The ids of the nodes that must be refreshed """

    def __init__(self, plugin_manager_interface, parent_widget):
        """
        Constructor of the class.

        @type plugin_manager_interface: PluginManagerInterface
        @param plugin_manager_interface: The plugin manager interface.
        @type parent_widget: Object
        @param parent_widget: The parent widget.
        """

        # calls the super
        wx.Panel.__init__(self, parent_widget, -1, style = wx.WANTS_CHARS)

        # stores the plugin manager interface
        self.plugin_manager_interface = plugin_manager_interface

        # initializes the structures
        self.tree_map = colony.libs.structures_util.OrderedMap()
        self.node_map = {}
        self.node_item_map = {}
        self.dirty_node_map = {}

        # creates the tree
        self.create_tree(parent_widget)

        # creates the tree map
        self.create_tree_map()

        # indexes the tree map
        self.index_tree_map()

        # creates the root node item
        self.create_root_node_item()

    def create_tree_map(self):
        # retrieves the plugin manager
        plugin_manager_interface = self.plugin_manager_interface
        plugin_manager_interface_plugin = plugin_manager_interface.plugin_manager_interface_plugin
        plugin_manager = plugin_manager_interface_plugin.manager

        # retrieves the plugins
        plugins = plugin_manager.get_all_plugins()

        # creates a list of the plugins to
        # avoid manipulating the original reference
        plugins = list(plugins)

        # sorts the plugins by their id
        plugins.sort(self.compare_plugins)

        # for each plugin
        for plugin in plugins:
            # creates the plugin map
            self.create_plugin_map(plugin)

    def create_plugin_map(self, plugin):
        # retrieves the plugin's attributes
        plugin_id = plugin.id
        plugin_version = plugin.version
        plugin_loaded = plugin.is_loaded()

        # defines the plugin attribute texts
        plugin_text = PLUGIN_NAME_FORMAT % (plugin_id, plugin_version)

        # creates the plugin child nodes map
        plugin_child_nodes_map = {}

        # adds the capabilities to the plugin map
        self.add_plugin_map_capabilities(plugin, plugin_child_nodes_map)

        # adds the capabilities allowed to the plugin map
        self.add_plugin_map_capabilities_allowed(plugin, plugin_child_nodes_map)

        # adds the pluing dependencies to the plugin map
        self.add_plugin_map_plugin_dependencies(plugin, plugin_child_nodes_map)

        # creates the plugin map
        plugin_map = {}

        # sets the plugin map's attributes
        plugin_map[TEXT_VALUE] = plugin_text
        plugin_map[CHECKABLE_VALUE] = True
        plugin_map[CHECKED_VALUE] =  plugin_loaded
        plugin_map[CHILD_NODES_VALUE] = plugin_child_nodes_map

        # sets the plugin map in the tree map
        self.tree_map[plugin_id] = plugin_map

    def add_plugin_map_capabilities(self, plugin, plugin_map):
        # retrieves the plugin capabilities
        plugin_capabilities = plugin.capabilities

        # in case the plugin has no capabilities
        if not plugin_capabilities:
            # returns since no capabilities were found
            return

        # initializes the capabilities map
        capabilities_map = {}

        # creates the maps for the plugin capabilities
        for plugin_capability in plugin_capabilities:
            # defines the plugin capability map
            plugin_capability_map = {}

            # sets the attributes in the plugin capability map
            plugin_capability_map[TEXT_VALUE] = plugin_capability

            # sets the plugin capability map in the capabilities map
            capabilities_map[plugin_capability] = plugin_capability_map

        # initializes the plugin capabilities map
        plugin_capabilities_map = {}

        # sets the attributes in the plugin capabilities map
        plugin_capabilities_map[TEXT_VALUE] = CAPABILITIES_VALUE
        plugin_capabilities_map[CHILD_NODES_VALUE] = capabilities_map

        # sets the plugin capabilities map in the plugin map
        plugin_map[CAPABILITIES_VALUE] = plugin_capabilities_map

    def add_plugin_map_capabilities_allowed(self, plugin, plugin_map):
        # retrieves the plugin capabilities allowed
        plugin_capabilities_allowed = plugin.capabilities_allowed

        # in case the plugin has no capabilities allowed
        if not plugin_capabilities_allowed:
            # returns since no capabilities were found
            return

        # initializes the capabilities allowed map
        capabilities_allowed_map = {}

        # creates the maps for the plugin capabilities allowed
        for plugin_capability_allowed in plugin_capabilities_allowed:
            # retrieves the plugin capability allowed type
            plugin_capability_allowed_type = type(plugin_capability_allowed)

            # retrieves the plugin capability allowed id
            plugin_capability_allowed_id = plugin_capability_allowed_type == types.TupleType and plugin_capability_allowed[0] or plugin_capability_allowed

            # defines the plugin capability allowed map
            plugin_capability_allowed_map = {}

            # sets the attributes in the plugin capability allowed map
            plugin_capability_allowed_map[TEXT_VALUE] = plugin_capability_allowed_id

            # sets the plugin capability allowed map in the capabilities allowed map
            capabilities_allowed_map[plugin_capability_allowed_id] = plugin_capability_allowed_map

        # creates the plugin capabilities allowed map
        plugin_capabilities_allowed_map = {}

        # sets the plugin capabilities allowed map attributes
        plugin_capabilities_allowed_map[TEXT_VALUE] = "capabilities allowed"
        plugin_capabilities_allowed_map[CHILD_NODES_VALUE] = capabilities_allowed_map

        # sets the plugin capabilities allowed map in the plugin map
        plugin_map[CAPABILITIES_ALLOWED_VALUE] = plugin_capabilities_allowed_map

    def add_plugin_map_plugin_dependencies(self, plugin, plugin_map):
        # retrieves the plugin dependencies
        plugin_dependencies = plugin.dependencies

        # filters out package dependencies
        plugin_dependencies = [plugin_dependency for plugin_dependency in plugin_dependencies if plugin_dependency.__class__.__name__ == PLUGIN_DEPENDENCY_CLASS_NAME]

        # in case the plugin has no dependencies
        if not plugin_dependencies:
            # returns since no dependencies were found
            return

        # initializes the dependencies map
        dependencies_map = {}

        # creates the maps for the plugin dependencies
        for plugin_dependency in plugin_dependencies:
            # retrieves the plugin dependency attributes
            plugin_dependency_id = plugin_dependency.plugin_id
            plugin_dependency_version = plugin_dependency.plugin_version

            # defines the plugin dependency text
            plugin_dependency_text = PLUGIN_NAME_FORMAT % (plugin_dependency_id, plugin_dependency_version)

            # creates the plugin dependency map
            plugin_dependency_map = {}

            # sets the attributes in the plugin dependency map
            plugin_dependency_map[TEXT_VALUE] = plugin_dependency_text
            plugin_dependency_map[LINK_VALUE] = plugin_dependency_id

            # sets the plugin dependency map in the dependencies map
            dependencies_map[plugin_dependency_id] = plugin_dependency_map

        # creates the plugin dependencies map
        plugin_dependencies_map = {}

        # sets the plugin dependencies map attributes
        plugin_dependencies_map[TEXT_VALUE] = "dependencies"
        plugin_dependencies_map[CHILD_NODES_VALUE] = dependencies_map

        # sets the plugin dependencies map in the plugin map
        plugin_map[DEPENDENCIES_VALUE] = plugin_dependencies_map

    def index_tree_map(self):
        # retrieves the tree map items
        tree_map_items = self.tree_map.items()

        # indexes the tree map items
        for node_id, node_map in tree_map_items:
            # retrieves the node attributes
            child_nodes_map = node_map.get(CHILD_NODES_VALUE, {})

            # indexes the node by its id
            self.node_map[node_id] = node_map

            # indexes the child nodes map
            child_nodes_map and self.index_node_map(node_id, child_nodes_map)

    def index_node_map(self, prefix, node_map):
        # retrieves the node map items
        node_map_items = node_map.items()

        # indexes the nodes by their id
        for node_id, sub_node_map in node_map_items:
            # removes the entry from the node map
            del node_map[node_id]

            # creates the prefixed version of the id
            node_id = NODE_ATTRIBUTE_FORMAT % (prefix, node_id)

            # sets the map in the node map with the full id
            node_map[node_id] = sub_node_map

            # retrieves the node attributes
            child_nodes_map = sub_node_map.get(CHILD_NODES_VALUE, {})

            # indexes the node by its id
            self.node_map[node_id] = sub_node_map

            # indexes the child nodes map
            child_nodes_map and self.index_node_map(node_id, child_nodes_map)

    def create_root_node_item(self):
        # creates the root node map
        root_node_map = {}

        # sets the attributes in the root node map
        root_node_map[TEXT_VALUE] = "Plugins"
        root_node_map[CHILD_NODES_VALUE] = self.tree_map

        # creates the root node item
        root_node_item = self.tree.AddRoot("Plugins")
        self.tree.SetItemImage(root_node_item, self.fldridx, wx.TreeItemIcon_Normal)
        self.tree.SetItemImage(root_node_item, self.fldropenidx, wx.TreeItemIcon_Expanded)
        self.tree.SetItemPyData(root_node_item, ROOT_NODE_ID)

        # sets the root item in the node item map
        self.node_map[ROOT_NODE_ID] = root_node_map
        self.node_item_map[ROOT_NODE_ID] = root_node_item

        # creates a fake node item to make the
        # node act as an expandable node
        fake_node_id = FAKE_NODE_ID_FORMAT % ROOT_NODE_ID
        self.create_node_item(root_node_item, fake_node_id, {})

        # loads the root node
        self.load_node_item(ROOT_NODE_ID, root_node_map, root_node_item)

        # expands the root node item
        self.tree.Expand(root_node_item)

    def load_node_item(self, node_id, node_map, node_item):
        # retrieves the child nodes map
        child_nodes_map = node_map.get(CHILD_NODES_VALUE, {})

        # retrieves the child node items
        child_nodes_items = child_nodes_map.items()

        # for each child node
        for child_node_id, child_node_map in child_nodes_items:
            # retrieves the child nodes map
            child_nodes_map = child_node_map.get(CHILD_NODES_VALUE, {})

            # creates the child node item
            child_node_item = self.create_node_item(node_item, child_node_id, child_node_map)

            # creates a fake node item to make the node act as an expandable node
            fake_node_id = FAKE_NODE_ID_FORMAT % child_node_id
            child_nodes_map and self.create_node_item(child_node_item, fake_node_id, {})

        # sets the node as loaded
        node_map[LOADED_VALUE] = True

        # retrieves the fake node item for this node
        fake_node_id = FAKE_NODE_ID_FORMAT % node_id
        fake_node_item = self.node_item_map[fake_node_id]

        # deletes the fake node item
        self.tree.Delete(fake_node_item)

    def create_node_item(self, parent_item, node_id, node_map):
        # retrieves the node attributes
        node_text = node_map.get(TEXT_VALUE, node_id)
        node_checkable = node_map.get(CHECKABLE_VALUE, False)

        # sets the parent item's images
        self.tree.SetItemImage(parent_item, self.fldridx, wx.TreeItemIcon_Normal)
        self.tree.SetItemImage(parent_item, self.fldropenidx, wx.TreeItemIcon_Expanded)
        self.tree.SetItemImage(parent_item, self.fldropenidx, wx.TreeItemIcon_Selected)

        # calculates the node item attributes
        node_item_type = node_checkable and 1 or 0

        # creates the node item
        node_item = self.tree.AppendItem(parent_item, node_text, ct_type = node_item_type)

        # sets the item's iamges
        self.tree.SetItemImage(node_item, self.fileidx, wx.TreeItemIcon_Normal)
        self.tree.SetItemImage(node_item, self.fileidx, wx.TreeItemIcon_Selected)

        # sets the item's data
        self.tree.SetItemPyData(node_item, node_id)

        # indexes the node item by its
        self.node_item_map[node_id] = node_item

        # refreshes the node item
        self.refresh_node_item(node_id, node_map, node_item)

        # returns the node item
        return node_item

    def refresh_node_items_checked(self):
        # retrieves the plugin manager
        plugin_manager_interface_plugin = self.plugin_manager_interface.plugin_manager_interface_plugin
        plugin_manager = plugin_manager_interface_plugin.manager

        # for each node in the tree map
        for node_id in self.tree_map:
            # retrieves the plugin instance
            plugin = plugin_manager.plugin_instances_map[node_id]

            # checks if the plugin is loaded
            loaded = plugin.is_loaded()

            # updates the node's checked attribute
            self.set_node_attribute(node_id, CHECKED_VALUE, loaded)

        # refreshes the node items
        self.refresh_node_items()

    def refresh_node_items(self):
        # for each node in the dirty nodes map
        for node_id in self.dirty_node_map:
            # retrieves the node map
            node_map = self.node_map[node_id]

            # retrieves the node item
            node_item = self.node_item_map[node_id]

            # refreshes the node item
            self.refresh_node_item(node_id, node_map, node_item)

        # resets the dirty nodes map
        self.dirty_node_map = {}

    def refresh_node_item(self, node_id, node_map, node_item):
        # retrieves the node attributes
        node_link = node_map.get(LINK_VALUE, None)
        node_bold = node_map.get(BOLD_VALUE, False)
        node_checked = node_map.get(CHECKED_VALUE, False)

        # calculates the node item attributes
        node_item_hypertext = node_link and True or False

        # sets the item attributes
        self.tree.SetItemHyperText(node_item, node_item_hypertext)
        self.tree.SetItemBold(node_item, node_bold)
        node_item._checked = node_checked

    def set_node_attribute(self, node_id, attribute_name, attribute_value):
        # retrieves the node map
        node_map = self.node_map[node_id]

        # sets the attribute in the node map
        node_map[attribute_name] = attribute_value

        # marks the node as dirty
        self.dirty_node_map[node_id] = True

    def create_tree(self, parent_widget):
        # creates the images
        images = wx.ImageList(IMAGE_WIDTH, IMAGE_HEIGHT)
        folder_bitmap = wx.ArtProvider_GetBitmap(wx.ART_FOLDER, wx.ART_OTHER, IMAGE_SIZE)
        file_open_bitmap = wx.ArtProvider_GetBitmap(wx.ART_FILE_OPEN, wx.ART_OTHER, IMAGE_SIZE)
        file_bitmap = wx.ArtProvider_GetBitmap(wx.ART_NORMAL_FILE, wx.ART_OTHER, IMAGE_SIZE)
        self.fldridx = images.Add(folder_bitmap)
        self.fldropenidx = images.Add(file_open_bitmap)
        self.fileidx = images.Add(file_bitmap)
        self.il = images

        # creates the grid sizer
        grid_sizer = wx.FlexGridSizer(0, 1, 0)
        grid_sizer.AddGrowableCol(0)
        grid_sizer.AddGrowableRow(1)

        # creates the tree
        self.tree = wx.lib.customtreectrl.CustomTreeCtrl(self, wx.ID_ANY, style = wx.BORDER_DEFAULT | wx.lib.customtreectrl.TR_HAS_BUTTONS | wx.lib.customtreectrl.TR_HAS_VARIABLE_ROW_HEIGHT)

        # creates the panel's components
        self.search_textfield = wx.SearchCtrl(self, wx.ID_ANY, style = wx.TE_PROCESS_ENTER)

        # configures the components
        self.tree.SetImageList(images)
        self.tree.EnableSelectionVista(True)
        self.search_textfield.ShowSearchButton(True)
        self.search_textfield.ShowCancelButton(True)

        # binds the component's events
        self.Bind(wx.EVT_SIZE, self.on_size)
        self.Bind(wx.EVT_TEXT, self.on_search, self.search_textfield)
        self.Bind(wx.lib.customtreectrl.EVT_TREE_ITEM_HYPERLINK, self.on_hyperlink)
        self.tree.Bind(wx.lib.customtreectrl.EVT_TREE_ITEM_CHECKED, self.on_checked)
        self.tree.Bind(wx.lib.customtreectrl.EVT_TREE_ITEM_EXPANDED, self.on_expanded)

        # sets the components in the layout
        grid_sizer.Add(self.search_textfield, 0, wx.GROW | wx.ALIGN_CENTER | wx.ALL, 5)
        grid_sizer.Add(self.tree, 0, wx.GROW | wx.ALIGN_CENTER | wx.ALL, 5)

        # sets the panel's sizer
        self.SetSizer(grid_sizer)

        # performs the layout
        self.Layout()

    def search(self, search_value):
        # initializes the first match node id
        first_match_node_id = None

        # searches for the specified value
        for node_id in self.tree_map:
            # checks if the node is a match
            match = search_value in node_id

            # stores the first match
            first_match_node_id = not first_match_node_id and match and node_id or first_match_node_id

            # sets the node as bold in case it is a match
            self.set_node_attribute(node_id, BOLD_VALUE, match)

        # refreshes the node items
        self.refresh_node_items()

        # selects the first match
        first_match_node_item = first_match_node_id and self.node_item_map[first_match_node_id]
        first_match_node_id and self.tree.SelectItem(first_match_node_item)

    def compare_plugins(self, first_plugin, second_plugin):
        # retrieves the plugin ids
        first_plugin_id = first_plugin.id
        second_plugin_id = second_plugin.id

        # compares the plugins
        plugin_comparison = cmp(first_plugin_id, second_plugin_id)

        # returns the plugin comparison
        return plugin_comparison

    def on_size(self, event):
        # performs the layout
        self.Layout()

    def on_expanded(self, event):
        # retrieves the item
        item = event.GetItem()

        # retrieves the expanded node id
        node_id = self.tree.GetItemPyData(item)

        # retrieves the node map
        node_map = self.node_map[node_id]

        # retrieves the loaded flag from the node map
        loaded = node_map.get(LOADED_VALUE, False)

        # returns in case the node is already loaded
        if loaded:
            return

        # retrieves the node item
        node_item = self.node_item_map[node_id]

        # loads the node item
        self.load_node_item(node_id, node_map, node_item)

    def toggle_plugin_state(self, node_id, load):
        # retrieves the plugin manager
        plugin_manager_interface_plugin = self.plugin_manager_interface.plugin_manager_interface_plugin
        plugin_manager = plugin_manager_interface_plugin.manager

        # loads or unloads the plugin depending on the state
        load and plugin_manager.load_plugin(node_id) or plugin_manager.unload_plugin(node_id)

        # refreshes the node items checked state
        self.refresh_node_items_checked()

    def on_checked(self, event):
        # retrieves the item
        item = event.GetItem()

        # retrieves the checked node id
        node_id = self.tree.GetItemPyData(item)

        # retrieves the item's checked attribute
        load = item._checked

        # toggles the plugin's state
        self.toggle_plugin_state(node_id, load)

    def on_hyperlink(self, event):
        # retrieves the item
        item = event.GetItem()

        # retrieves the checked node id
        node_id = self.tree.GetItemPyData(item)

        # retrieves the node map
        node_map = self.node_map[node_id]

        # retrieves the node link
        node_link = node_map[LINK_VALUE]

        # retrieves the node link item
        node_link_item = self.node_item_map[node_link]

        # selects the node link item
        self.tree.SelectItem(node_link_item)

    def on_search(self, event):
        # retrieves the search value
        search_value = event.GetString()

        # performs the search
        self.search(search_value)
