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

class Extension(object):
    """
    The extension class.
    """

    extension_id = "none"
    """ The extension id """

    extension_version = "none"
    """ The extension version """

    def __init__(self):
        pass

class WikiExtension(Extension):
    """
    The wiki extension class.
    """

    def __init__(self):
        pass

class ExtensionManager:
    """
    The extension manager class.
    """

    refered_modules = []
    """ The refered modules """

    def __init__(self):
        pass

    def load_system(self):
        """
        Starts the process of loading the plugin system.
        """

        self.logger.info("Starting extension manager...")

        # gets all modules from all extension paths
        for extension_path in self.extension_paths:
            self.refered_modules.extend(self.get_all_modules(extension_path))

        # starts the extension loading process
        self.init_extension_system({"extension_paths": self.extension_paths, "extensions": self.refered_modules})

    def init_extension_system(self, configuration):
        """
        Starts the extension loading process.

        @type configuration: Dictionary
        @param configuration: The configuration structure.
        """

        # adds the defined extension paths to the system python path
        self.set_python_path(configuration["extension_paths"])

        # loads the extension files into memory
        self.load_extensions(configuration["extensions"])

        # starts all the available the extensions
        self.start_extensions()

        # loads the main extensions
        self.load_main_extensions()

    def load_extensions(self, plugins):
        """
        Imports a module starting the extension,

        @type extensions: List
        @param extensions: The list of extensions to be loaded.
        """

        # iterates over all the available extensions
        for extension in extensions:
            # in case the extension module is not currently loaded
            if not extension in sys.modules:
                try:
                    # imports the extension module file
                    __import__(plugin)
                except:
                    self.logger.error("Problem importing module %s" % extension)

    def get_all_modules(self, path):
        """
        Retrieves all the modules in a given path.

        @type path: String
        @param path: The path to retrieve the modules.
        @rtype: List
        @return: All the modules in the given path.
        """

        # starts the modules list
        modules = []

        # in case the path does not exist
        if not os.path.exists(path):
            self.logger.warning("Path '%s' does not exist in the current filesystem" % (path))
            return modules

        # retrieves the directory list for the path
        dir_list = os.listdir(path)

        # iterates over all the file names
        # in the directory list
        for file_name in dir_list:
            # creates the full file path
            full_path = path + "/" + file_name

            # retrieves the file mode
            mode = os.stat(full_path)[stat.ST_MODE]

            # in case the file is not a directory
            if not stat.S_ISDIR(mode):
                # splits the path
                split = os.path.splitext(file_name)

                # retrieves the extension
                extension = split[-1]

                # in case the extension is a valid python extension
                if extension == ".py" or extension == ".pyc":
                    # retrieves the module name from the file name
                    module_name = "".join(split[:-1])

                    # in case the module name is not defined
                    # in the modules list
                    if not module_name in modules:
                        # adds the module name to the modules list
                        modules.append(module_name)

        # returns the modules list
        return modules

    def start_extensions(self):
        """
        Starts all the available extension, creating a singleton instance for each of them.
        """

        # retrieves all the extension classes available
        extension_classes = self.get_all_extension_classes()

        # iterates over all the available extension classes
        for extension in extension_classes:
            # tests the extension for loading
            if not extension in self.loaded_extensions:
                # starts the extension
                self.start_extension(extension)

    def start_extension(self, extension):
        """
        Starts the given extension, creating a singleton instance.

        @type extension: Class
        @param extension: The extension to start.
        """

        # retrieves the extension id
        extension_id = extension.id

        # retrieves the extension version
        extension_version = extension.version

        # retrieves the extension description
        extension_description = extension.description

        # instantiates the extension to create the singleton extension instance
        extension_instance = extension(self)

        # retrieves the path to the extension file
        extension_path = inspect.getfile(extension)

        # retrieves the absolute path to the extension file
        absolute_extension_path = os.path.abspath(extension_path)

        # retrieves the path to the directory containing the extension file
        extension_dir = os.path.dirname(absolute_extension_path)

        # starts all the extension manager structures related with extensions
        self.loaded_extensions.append(extension)
        self.loaded_extension_map[extension_id] = extension
        self.loaded_extensions_id_map[extension_id] = self.current_id
        self.id_loaded_extensions_map[self.current_id] = extension_id
        self.loaded_extensions_descriptions.append(extension_description)
        self.extension_instances.append(extension_instance)
        self.extension_instances_map[extension_id] = extension_instance
        self.extension_dirs_map[extension_id] = extension_dir

        # registers the extension capabilities in the extension manager
        self.register_extension_capabilities(extension_instance)

        # increments the current id
        self.current_id += 1

    def get_all_extension_classes(self, base_extension_class = Extension):
        """
        Retrieves all the available extension classes, from the defined base extension class.

        @type base_extension_class: Class
        @param base_extension_class: The base extension class to retrieve the extension classes.
        @rtype: List
        @return: The list of extension classes.
        """

        # creates the extension classes list
        extension_classes = []

        # retrieves the extension sub classes
        self.get_extension_sub_classes(base_extension_class, extension_classes)

        # returns the extension classes
        return extension_classes

    def get_extension_sub_classes(self, extension, extension_classes):
        """
        Retrieves all the sub classes for the given extension class.

        @type extension: Class
        @param extension: The extension class to retrieve the sub classes.
        @type extension_classes: List
        @param extension_classes: The current list of extension sub classes.
        @rtype: List
        @return: The list of all the sub classes for the given extension class.
        """

        # retrieves all the extension sub classes
        sub_classes = extension.__subclasses__()

        # iterates over all the extension sub classes
        for sub_class in sub_classes:
            self.get_extension_sub_classes(sub_class, extension_classes)
            if sub_class.valid and not sub_class in self.deleted_extension_classes:
                extension_classes.append(sub_class)
