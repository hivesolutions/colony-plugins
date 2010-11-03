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

__revision__ = "$LastChangedRevision: 72 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2008-10-21 23:29:54 +0100 (Ter, 21 Out 2008) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import types

import xml.dom.minidom

TEXT_NODE_TYPES = (xml.dom.minidom.Node.TEXT_NODE, xml.dom.minidom.Node.CDATA_SECTION_NODE)
""" The text node types tuple """

class Parser:
    """
    The abstract parser class
    """

    def __init__(self):
        """
        Constructor of the class
        """

        pass

    def parse(self):
        """
        Parses the defined file
        """

        pass

    def get_value(self):
        """
        Retrieves the result of the parse

        @rtype: Object
        @return: The result of the parse
        """

        pass

class BuildAutomationFileParser(Parser):
    """
    The build automation file parser class.
    """

    file = None
    """ The file path """

    build_automation = None
    """ The build automation """

    def __init__(self, file = None):
        Parser.__init__(self)
        self.file = file

    def parse(self):
        self.load_build_automation_file(self.file)

    def get_value(self):
        return self.build_automation

    def get_build_automation(self):
        return self.build_automation

    def load_build_automation_file(self, file):
        print "vai fazer parse"
        # creates the xml doument DOM object
        xml_document = xml.dom.minidom.parse(file)
        print "acabou de fazer parse"
        child_nodes = xml_document.childNodes

        for child_node in child_nodes:
            if valid_node(child_node):
                self.build_automation = self.parse_build_automation(child_node)

    def parse_build_automation(self, build_automation):
        build_automation_structure = BuildAutomation()
        child_nodes = build_automation.childNodes

        for child_node in child_nodes:
            if valid_node(child_node):
                self.parse_build_automation_element(child_node, build_automation_structure)

        return build_automation_structure

    def parse_build_automation_element(self, build_automation_element, build_automation):
        node_name = build_automation_element.nodeName

        if node_name == "parent":
            build_automation.parent = self.parse_build_automation_parent(build_automation_element)
        elif node_name == "artifact":
            build_automation.artifact = self.parse_build_automation_artifact(build_automation_element)
        elif node_name == "modules":
            build_automation.modules = self.parse_build_automation_modules(build_automation_element)
        elif node_name == "build":
            build_automation.build = self.parse_build_automation_build(build_automation_element)
        elif node_name == "profiles":
            build_automation.profiles = self.parse_build_automation_profiles(build_automation_element)

    def parse_build_automation_parent(self, build_automation_parent):
        parent = Parent()
        child_nodes = build_automation_parent.childNodes

        for child_node in child_nodes:
            if valid_node(child_node):
                self.parse_build_automation_parent_element(child_node, parent)

        return parent

    def parse_build_automation_parent_element(self, build_automation_parent_element, parent):
        node_name = build_automation_parent_element.nodeName

        if node_name == "id":
            parent.id = self.parse_build_automation_parent_id(build_automation_parent_element)
        elif node_name == "version":
            parent.version = self.parse_build_automation_parent_version(build_automation_parent_element)

    def parse_build_automation_parent_id(self, parent_id):
        build_automation_parent_id = parent_id.firstChild.data.strip()
        return build_automation_parent_id

    def parse_build_automation_parent_version(self, parent_version):
        build_automation_parent_version = parent_version.firstChild.data.strip()
        return build_automation_parent_version

    def parse_build_automation_artifact(self, build_automation_artifact):
        artifact = Artifact()
        child_nodes = build_automation_artifact.childNodes

        for child_node in child_nodes:
            if valid_node(child_node):
                self.parse_build_automation_artifact_element(child_node, artifact)

        return artifact

    def parse_build_automation_artifact_element(self, build_automation_artifact_element, artifact):
        node_name = build_automation_artifact_element.nodeName

        if node_name == "id":
            artifact.id = self.parse_build_automation_artifact_id(build_automation_artifact_element)
        elif node_name == "version":
            artifact.version = self.parse_build_automation_artifact_version(build_automation_artifact_element)
        elif node_name == "type":
            artifact.type = self.parse_build_automation_artifact_type(build_automation_artifact_element)
        elif node_name == "name":
            artifact.name = self.parse_build_automation_artifact_name(build_automation_artifact_element)
        elif node_name == "description":
            artifact.description = self.parse_build_automation_artifact_description(build_automation_artifact_element)

    def parse_build_automation_artifact_id(self, artifact_id):
        build_automation_artifact_id = artifact_id.firstChild.data.strip()
        return build_automation_artifact_id

    def parse_build_automation_artifact_version(self, artifact_version):
        build_automation_artifact_version = artifact_version.firstChild.data.strip()
        return build_automation_artifact_version

    def parse_build_automation_artifact_type(self, artifact_type):
        build_automation_artifact_type = artifact_type.firstChild.data.strip()
        return build_automation_artifact_type

    def parse_build_automation_artifact_name(self, artifact_name):
        build_automation_artifact_name = artifact_name.firstChild.data.strip()
        return build_automation_artifact_name

    def parse_build_automation_artifact_description(self, artifact_description):
        build_automation_artifact_description = artifact_description.firstChild.data.strip()
        return build_automation_artifact_description

    def parse_build_automation_modules(self, build_automation_modules):
        build_automation_modules_list = []
        child_nodes = build_automation_modules.childNodes

        for child_node in child_nodes:
            if valid_node(child_node):
                build_automation_module = self.parse_build_automation_module(child_node)
                build_automation_modules_list.append(build_automation_module)

        return build_automation_modules_list

    def parse_build_automation_module(self, build_automation_module):
        module = Module()
        child_nodes = build_automation_module.childNodes

        for child_node in child_nodes:
            if valid_node(child_node):
                self.parse_build_automation_module_element(child_node, module)

        return module

    def parse_build_automation_module_element(self, build_automation_module_element, module):
        node_name = build_automation_module_element.nodeName

        if node_name == "id":
            module.id = self.parse_build_automation_module_id(build_automation_module_element)
        elif node_name == "version":
            module.version = self.parse_build_automation_module_version(build_automation_module_element)
        elif node_name == "stage":
            module.stage = self.parse_build_automation_module_stage(build_automation_module_element)

    def parse_build_automation_module_id(self, module_id):
        build_automation_module_id = module_id.firstChild.data.strip()
        return build_automation_module_id

    def parse_build_automation_module_version(self, module_version):
        build_automation_module_version = module_version.firstChild.data.strip()
        return build_automation_module_version

    def parse_build_automation_module_stage(self, module_stage):
        build_automation_module_stage = module_stage.firstChild.data.strip()
        return build_automation_module_stage

    def parse_build_automation_build(self, build_automation_build):
        build = Build()
        child_nodes = build_automation_build.childNodes

        for child_node in child_nodes:
            if valid_node(child_node):
                self.parse_build_automation_build_element(child_node, build)

        return build

    def parse_build_automation_build_element(self, build_automation_build_element, build):
        node_name = build_automation_build_element.nodeName

        if node_name == "default_stage":
            build.default_stage = self.parse_build_automation_build_default_stage(build_automation_build_element)
        elif node_name == "execution_directory":
            build.execution_directory = self.parse_build_automation_build_execution_directory(build_automation_build_element)
        elif node_name == "target_directory":
            build.target_directory = self.parse_build_automation_build_target_directory(build_automation_build_element)
        elif node_name == "classes_directory":
            build.classes_directory = self.parse_build_automation_build_classes_directory(build_automation_build_element)
        elif node_name == "plugins_directory":
            build.plugins_directory = self.parse_build_automation_build_plugins_directory(build_automation_build_element)
        elif node_name == "documentation_directory":
            build.documentation_directory = self.parse_build_automation_build_documentation_directory(build_automation_build_element)
        elif node_name == "repository_directory":
            build.repository_directory = self.parse_build_automation_build_repository_directory(build_automation_build_element)
        elif node_name == "resources_directory":
            build.resources_directory = self.parse_build_automation_build_resources_directory(build_automation_build_element)
        elif node_name == "log_directory":
            build.log_directory = self.parse_build_automation_build_log_directory(build_automation_build_element)
        elif node_name == "source_directory":
            build.source_directory = self.parse_build_automation_build_source_directory(build_automation_build_element)
        elif node_name == "final_name":
            build.final_name = self.parse_build_automation_build_final_name(build_automation_build_element)
        elif node_name == "clean_target_directory":
            build.clean_target_directory = self.parse_build_automation_build_clean_target_directory(build_automation_build_element)
        elif node_name == "dependencies":
            build.dependencies = self.parse_build_automation_build_dependencies(build_automation_build_element)
        elif node_name == "plugins":
            build.plugins = self.parse_build_automation_build_plugins(build_automation_build_element)

    def parse_build_automation_build_default_stage(self, build_default_stage):
        build_automation_build_default_stage = build_default_stage.firstChild.data.strip()
        return build_automation_build_default_stage

    def parse_build_automation_build_execution_directory(self, build_execution_directory):
        build_automation_build_execution_directory = build_execution_directory.firstChild.data.strip()
        return build_automation_build_execution_directory

    def parse_build_automation_build_target_directory(self, build_target_directory):
        build_automation_build_target_directory = build_target_directory.firstChild.data.strip()
        return build_automation_build_target_directory

    def parse_build_automation_build_classes_directory(self, build_classes_directory):
        build_automation_build_classes_directory = build_classes_directory.firstChild.data.strip()
        return build_automation_build_classes_directory

    def parse_build_automation_build_plugins_directory(self, build_plugins_directory):
        build_automation_build_plugins_directory = build_plugins_directory.firstChild.data.strip()
        return build_automation_build_plugins_directory

    def parse_build_automation_build_documentation_directory(self, build_documentation_directory):
        build_automation_build_documentation_directory = build_documentation_directory.firstChild.data.strip()
        return build_automation_build_documentation_directory

    def parse_build_automation_build_repository_directory(self, build_repository_directory):
        build_automation_build_repository_directory = build_repository_directory.firstChild.data.strip()
        return build_automation_build_repository_directory

    def parse_build_automation_build_resources_directory(self, build_resources_directory):
        build_automation_build_resources_directory = build_resources_directory.firstChild.data.strip()
        return build_automation_build_resources_directory

    def parse_build_automation_build_log_directory(self, build_log_directory):
        build_automation_build_log_directory = build_log_directory.firstChild.data.strip()
        return build_automation_build_log_directory

    def parse_build_automation_build_source_directory(self, build_source_directory):
        build_automation_build_source_directory = build_source_directory.firstChild.data.strip()
        return build_automation_build_source_directory

    def parse_build_automation_build_final_name(self, build_final_name):
        build_automation_build_final_name = build_final_name.firstChild.data.strip()
        return build_automation_build_final_name

    def parse_build_automation_build_clean_target_directory(self, build_final_name):
        build_automation_build_clean_target_directory = build_final_name.firstChild.data.strip()
        return build_automation_build_clean_target_directory

    def parse_build_automation_build_dependencies(self, build_dependencies):
        build_automation_build_dependencies_list = []
        child_nodes = build_dependencies.childNodes

        for child_node in child_nodes:
            if valid_node(child_node):
                build_automation_build_dependency = self.parse_build_automation_build_dependency(child_node)
                build_automation_build_dependencies_list.append(build_automation_build_dependency)

        return build_automation_build_dependencies_list

    def parse_build_automation_build_dependency(self, build_dependency):
        dependency = Dependency()
        child_nodes = build_dependency.childNodes

        for child_node in child_nodes:
            if valid_node(child_node):
                self.parse_build_automation_build_dependency_element(child_node, dependency)

        return dependency

    def parse_build_automation_build_dependency_element(self, build_automation_build_dependency_element, dependency):
        node_name = build_automation_build_dependency_element.nodeName

        if node_name == "id":
            dependency.id = self.parse_build_automation_build_dependency_id(build_automation_build_dependency_element)
        elif node_name == "version":
            dependency.version = self.parse_build_automation_build_dependency_version(build_automation_build_dependency_element)
        elif node_name == "scope":
            dependency.scope = self.parse_build_automation_build_dependency_scope(build_automation_build_dependency_element)

    def parse_build_automation_build_dependency_id(self, build_dependency_id):
        build_automation_build_dependency_id = build_dependency_id.firstChild.data.strip()
        return build_automation_build_dependency_id

    def parse_build_automation_build_dependency_version(self, build_dependency_version):
        build_automation_build_dependency_version = build_dependency_version.firstChild.data.strip()
        return build_automation_build_dependency_version

    def parse_build_automation_build_dependency_scope(self, build_dependency_scope):
        build_automation_build_dependency_scope = build_dependency_scope.firstChild.data.strip()
        return build_automation_build_dependency_scope

    def parse_build_automation_build_plugins(self, build_plugins):
        build_automation_build_plugins_list = []
        child_nodes = build_plugins.childNodes

        for child_node in child_nodes:
            if valid_node(child_node):
                build_automation_build_plugin = self.parse_build_automation_plugin(child_node)
                build_automation_build_plugins_list.append(build_automation_build_plugin)

        return build_automation_build_plugins_list

    def parse_build_automation_plugin(self, build_automation_plugin):
        plugin = Plugin()
        child_nodes = build_automation_plugin.childNodes

        for child_node in child_nodes:
            if valid_node(child_node):
                self.parse_build_automation_plugin_element(child_node, plugin)

        return plugin

    def parse_build_automation_plugin_element(self, build_automation_plugin_element, plugin):
        node_name = build_automation_plugin_element.nodeName

        if node_name == "id":
            plugin.id = self.parse_build_automation_plugin_id(build_automation_plugin_element)
        elif node_name == "version":
            plugin.version = self.parse_build_automation_plugin_version(build_automation_plugin_element)
        elif node_name == "stage":
            plugin.stage = self.parse_build_automation_plugin_stage(build_automation_plugin_element)
        elif node_name == "stage_dependency":
            plugin.stage_dependency = self.parse_build_automation_plugin_stage_dependency(build_automation_plugin_element)
        elif node_name == "configuration":
            plugin.configuration = self.parse_build_automation_plugin_configuration(build_automation_plugin_element)

    def parse_build_automation_plugin_id(self, plugin_id):
        build_automation_plugin_id = plugin_id.firstChild.data.strip()
        return build_automation_plugin_id

    def parse_build_automation_plugin_version(self, plugin_version):
        build_automation_plugin_version = plugin_version.firstChild.data.strip()
        return build_automation_plugin_version

    def parse_build_automation_plugin_stage(self, plugin_stage):
        build_automation_plugin_stage = plugin_stage.firstChild.data.strip()
        return build_automation_plugin_stage

    def parse_build_automation_plugin_stage_dependency(self, plugin_stage_dependency):
        build_automation_plugin_stage_dependency = plugin_stage_dependency.firstChild.data.strip()
        return build_automation_plugin_stage_dependency

    def parse_build_automation_plugin_configuration(self, plugin_configuration):
        configuration = Configuration()
        child_nodes = plugin_configuration.childNodes

        for child_node in child_nodes:
            if valid_node(child_node):
                self.parse_generic_element(child_node, configuration)

        return configuration

    def parse_build_automation_profiles(self, build_automation_profiles):
        build_automation_profiles_list = []
        child_nodes = build_automation_profiles.childNodes

        for child_node in child_nodes:
            if valid_node(child_node):
                build_automation_profile = self.parse_build_automation_profile(child_node)
                build_automation_profiles_list.append(build_automation_profile)

        return build_automation_profiles_list

    def parse_build_automation_profile(self, build_automation_profile):
        profile = Profile()
        child_nodes = build_automation_profile.childNodes

        for child_node in child_nodes:
            if valid_node(child_node):
                self.parse_build_automation_profile_element(child_node, profile)

        return profile

    def parse_build_automation_profile_element(self, build_automation_profile_element, profile):
        node_name = build_automation_profile_element.nodeName

        if node_name == "id":
            profile.id = self.parse_build_automation_profile_id(build_automation_profile_element)
        elif node_name == "activation":
            profile.activation = self.parse_build_automation_profile_activation(build_automation_profile_element)
        elif node_name == "build":
            profile.build = self.parse_build_automation_build(build_automation_profile_element)

    def parse_build_automation_profile_id(self, profile_id):
        build_automation_profile_id = profile_id.firstChild.data.strip()
        return build_automation_profile_id

    def parse_build_automation_profile_activation(self, profile_activation):
        activation = Activation()
        child_nodes = profile_activation.childNodes

        for child_node in child_nodes:
            if valid_node(child_node):
                self.parse_build_automation_profile_activation_element(child_node, activation)

        return activation

    def parse_build_automation_profile_activation_element(self, profile_activation_element, activation):
        node_name = profile_activation_element.nodeName

        if node_name == "property":
            activation.property = self.parse_build_automation_property(profile_activation_element)

    def parse_build_automation_property(self, build_automation_property):
        property = Property()
        child_nodes = build_automation_property.childNodes

        for child_node in child_nodes:
            if valid_node(child_node):
                self.parse_build_automation_property_element(child_node, property)

        return property

    def parse_build_automation_property_element(self, build_automation_property_element, property):
        node_name = build_automation_property_element.nodeName

        if node_name == "name":
            property.name = self.parse_build_automation_property_name(build_automation_property_element)
        elif node_name == "value":
            property.value = self.parse_build_automation_property_value(build_automation_property_element)

    def parse_build_automation_property_name(self, property_name):
        build_automation_property_name = property_name.firstChild.data.strip()
        return build_automation_property_name

    def parse_build_automation_property_value(self, property_value):
        build_automation_property_value = property_value.firstChild.data.strip()
        return build_automation_property_value

    def parse_generic_element(self, generic_element, generic_structure):
        node_name = generic_element.nodeName

        if len(generic_element.childNodes) == 1 and generic_element.firstChild.nodeType in TEXT_NODE_TYPES:
            data_value = generic_element.firstChild.data.strip()
            self._setattr(generic_structure, node_name, data_value)
        else:
            # creates a new generic structure
            new_generic_structure = GenericElement()
            new_generic_structure.element_name = node_name

            child_nodes = generic_element.childNodes

            for child_node in child_nodes:
                if valid_node(child_node):
                    self.parse_generic_element(child_node, new_generic_structure)

            self._setattr(generic_structure, node_name, new_generic_structure)

    def _setattr(self, structure, name, value):
        """
        Sets a value in a structure (object) with a given name.
        In case the value already exists a new list is created for
        the given name and the value is appended.

        @type structure: Object
        @param structure: The object to have the value set.
        @type name: String
        @param name: The name of the value (attribute) in the structure.
        @type value: Object
        @param value: The value (attribute) to be set in the structure.
        """

        # in case the name already exists in the structure
        # the duplicated value must be converted to a list
        if hasattr(structure, name):
            # retrieves the base value from the structure
            base_value = getattr(structure, name)

            # in case the base value is not a list yet
            if not type(base_value) == types.ListType:
                # sets the (new) list in the structure
                setattr(structure, name, [base_value])

            # retrieves the base value from the structure
            base_value = getattr(structure, name)

            # adds the value to the base value (list)
            base_value.append(value)
        else:
            # sets the (simple) value in the structure
            setattr(structure, name, value)

class GenericElement:
    """
    The generic element class.
    """

    element_name = "none"
    """ The name of the element """

    def __init__(self, element_name = "none"):
        self.element_name = element_name

class BuildAutomation:
    """
    The build automation class.
    """

    parent = None
    """ The parent build automation structure """

    artifact = None
    """ The associated artifact structure """

    modules = []
    """ The list of modules """

    build = None
    """ The associated build structure """

    profiles = []
    """ The list of profiles """

    def __init__(self, parent = None, artifact = None, build = None):
        self.parent = parent
        self.artifact = artifact
        self.build = build
        self.profiles = []

class Parent:
    """
    The parent class.
    """

    id = "none"
    """ The id of the parent """

    version = "none"
    """ The version of the parent """

    def __init__(self, id = "none", version = "none"):
        self.id = id
        self.version = version

class Artifact:
    """
    The artifact class.
    """

    id = "none"
    """ The id of the artifact """

    version = "none"
    """ The version of the artifact """

    type = "none"
    """ The type of the artifact """

    name = "none"
    """ The name of the artifact """

    description = "none"
    """ The description of the artifact """

    def __init__(self, id = "none", version = "none", type = "none", name = "none", description = "none"):
        self.id = id
        self.version = version
        self.type = type
        self.name = name
        self.description = description

class Module:
    """
    The module class.
    """

    id = "none"
    version = "none"
    stage = None

    def __init__(self, id = "none", version = "none", stage = None):
        self.id = id
        self.version = version
        self.stage = stage

class Build:
    """
    The build class.
    """

    default_stage = "none"
    """ The default stage for the build """

    execution_directory = "none"
    """ The directory to be used for execution """

    target_directory = "none"
    """ The target directory """

    classes_directory = "none"
    """ The classes directory """

    plugins_directory = "none"
    """ The plugins directory """

    documentation_directory = "none"
    """ The documentation directory """

    repository_directory = "none"
    """ The repository directory """

    resources_directory = "none"
    """ The resources directory """

    log_directory = "none"
    """ The log directory """

    source_directory = "none"
    """ The source directory """

    final_name = "none"
    """ The final name of the build """

    clean_target_directory = "none"
    """ The clean target directory """

    dependencies = []
    """ The list of dependencies """

    plugins = []
    """ The list of plugins """

    def __init__(self, default_stage = "none", execution_directory = "none", target_directory = "none", classes_directory = "none", plugins_directory = "none", documentation_directory = "none", repository_directory = "none", resources_directory = "none", log_directory = "none", source_directory = "none", final_name = "none", clean_target_directory = "none"):
        self.default_stage = default_stage
        self.execution_directory = execution_directory
        self.target_directory = target_directory
        self.classes_directory = classes_directory
        self.plugins_directory = plugins_directory
        self.documentation_directory = documentation_directory
        self.repository_directory = repository_directory
        self.resources_directory = resources_directory
        self.log_directory = log_directory
        self.source_directory = source_directory
        self.final_name = final_name
        self.clean_target_directory = clean_target_directory
        self.dependencies = []
        self.plugins = []

class Dependency:
    """
    The dependency class.
    """

    id = "none"
    """ The id of the dependency """

    version = "none"
    """ The version of the dependency """

    scope = "none"
    """ The scope of the dependency """

    def __init__(self, id = "none", version = "none", scope = "none"):
        self.id = id
        self.version = version
        self.scope = scope

class Plugin:
    """
    The plugin class.
    """

    id = "none"
    """ The id of the plugin """

    version = "none"
    """ The version of the plugin """

    stage = "none"
    """ The minimum stage to "activate" the plugin operation """

    stage_dependency = "none"
    """ The stages that this plugin requires as minimum (only valid to post-build stage) """

    configuration = None
    """ The plugin configuration """

    def __init__(self, id = "None", version = "none", stage = "none", stage_dependency = "none", configuration = None):
        self.id = id
        self.version = version
        self.stage = stage
        self.stage_dependency = stage_dependency
        self.configuration = configuration

class Configuration:
    """
    The configuration class.
    """

    def __init__(self):
        """
        Constructor of the class.
        """

        pass

class Profile:
    """
    The profile class.
    """

    id = "none"
    """ The profile id """

    activation = None
    """ The profile activation """

    build = None
    """ The associated build """

    def __init__(self, id = "none", activation = None, build = None):
        """
        Constructor of the class.

        @type id: String
        @param id: The profile id.
        @type activation: Activation
        @param activation: The profile activation.
        @type build: Build
        @param build: The associated build.
        """

        self.id = id
        self.activation = activation
        self.build = build

class Activation:
    """
    The activation class.
    """

    property = None
    """ The property for activation """

    def __init__(self, property = None):
        """
        Constructor of the class.

        @type property: Property
        @param property: The property for activation.
        """

        self.property = property

class Property:
    """
    The property class.
    """

    name = "none"
    """ The name of the property """

    value = "none"
    """ The value of the property """

    def __init__(self, name = "none", value = "none"):
        """
        Constructor of the class.

        @type name: String
        @param name: The name of the property.
        @type value: Object
        @param value: The value of the property.
        """

        self.name = name
        self.value = value

def valid_node(node):
    """
    Gets if a node is valid or not for parsing.

    @type node: Node
    @param node: The Xml node to be validated.
    @rtype: bool
    @return: The valid or not valid value.
    """

    # in case the node is of type element
    if node.nodeType == xml.dom.minidom.Node.ELEMENT_NODE:
        # returns true (valid)
        return True
    # otherwise
    else:
        # returns false (invalid)
        return False
