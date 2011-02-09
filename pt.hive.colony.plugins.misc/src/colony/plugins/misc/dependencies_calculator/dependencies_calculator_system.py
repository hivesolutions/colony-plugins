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

class DependenciesCalculator:
    """
    The dependencies calculator class.
    """

    dependencies_calculator_plugin = None
    """ The dependencies calculator plugin """

    def __init__(self, dependencies_calculator_plugin):
        """
        Constructor of the class.

        @type dependencies_calculator_plugin: DependenciesCalculatorPlugin
        @param dependencies_calculator_plugin: The dependencies calculator plugin.
        """

        self.dependencies_calculator_plugin = dependencies_calculator_plugin

    def generate_graph(self, plugin_list):
        plugin_graph_generator = PluginGraphGenerator(plugin_list)
        plugin_graph_generator.generate_graph()
        graph = plugin_graph_generator.get_value()
        return graph

    def detect_circular_references(self, plugin_list):
        graph = self.generate_graph(plugin_list)

        if not graph:
            raise Exception("Not valid graph given")

        return graph.has_circular_connections()

class PluginGraphGenerator:

    plugin_list = []
    plugin_id_version_node_map = {}
    graph = None

    def __init__(self, plugin_list = []):
        self.plugin_list = plugin_list
        self.plugin_id_node_map = {}

    def generate_graph(self):
        self.graph = Graph()

        # iterates over all the plugins creating a graph node for each
        for plugin in self.plugin_list:
            graph_node = GraphNode(plugin)
            plugin_tuple = plugin.get_tuple()
            # appends the plugin graph node to the map with the tuple key (plugin id and version)
            self.plugin_id_version_node_map[plugin_tuple] = graph_node
            # appends the plugin graph node to the grap nodes list
            self.graph.nodes_list.append(graph_node)

        # iterates over all the plugins associating the plugin relations
        # with the related graph nodes
        for plugin in self.plugin_list:
            plugin_tuple = plugin.get_tuple()
            graph_node = self.plugin_id_version_node_map[plugin_tuple]
            plugin_dependencies = plugin.get_all_plugin_dependencies()

            # iterates over all the dependencies
            for plugin_dependency in plugin_dependencies:
                plugin_dependency_tuple = plugin_dependency.get_tuple()
                if plugin_dependency_tuple in self.plugin_id_version_node_map:
                    dependency_graph_node = self.plugin_id_version_node_map[plugin_dependency_tuple]
                    graph_node.connected_nodes_list.append(dependency_graph_node)
                else:
                    raise Exception("Plugin dependency not found for plugin '%s' v%s" % (plugin.short_name, plugin.version))

    def get_value(self):
        return self.graph

class Graph:
    """
    The graph class, representing the graph structure.
    """

    MARK_WHITE = 1
    MARK_BLACK = 2
    MARK_GRAY = 3

    nodes_list = []
    """ The nodes list """

    def __init__(self):
        self.nodes_list = []

    def has_circular_connections(self):
        for node in self.nodes_list:
            node.mark = Graph.MARK_WHITE

        for node in self.nodes_list:
            if node.mark == Graph.MARK_WHITE:
                if self.visit_node(node):
                    self.clean_nodes()
                    return True

        self.clean_nodes()
        return False

    def visit_node(self, node):
        node.mark = Graph.MARK_GRAY

        for connected_node in node.connected_nodes_list:
            if connected_node.mark == Graph.MARK_GRAY:
                return True
            elif connected_node.mark == Graph.MARK_WHITE:
                if self.visit_node(connected_node):
                    return True

        node.mark = Graph.MARK_BLACK
        return False

    def clean_nodes(self):
        # iterates over all the nodes in the nodes list
        for node in self.nodes_list:
            # deletes the node mark
            del node.mark

    # @todo: improve the print of this graph
    def print_graph(self):
        for node in self.nodes_list:
            print node.value.id

class GraphNode:
    """
    The graph node class, representing the a graph node.
    """

    value = None
    """ The value of the graph node """

    connected_nodes_list = []
    """ The list of connected nodes """

    def __init__(self, value = None):
        """
        Constructor of the class.

        @type value: Object
        @param value: The value of the graph node.
        """

        self.value = value
        self.connected_nodes_list = []
