#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Colony Framework
# Copyright (c) 2008-2024 Hive Solutions Lda.
#
# This file is part of Hive Colony Framework.
#
# Hive Colony Framework is free software: you can redistribute it and/or modify
# it under the terms of the Apache License as published by the Apache
# Foundation, either version 2.0 of the License, or (at your option) any
# later version.
#
# Hive Colony Framework is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# Apache License for more details.
#
# You should have received a copy of the Apache License along with
# Hive Colony Framework. If not, see <http://www.apache.org/licenses/>.

__author__ = "João Magalhães <joamag@hive.pt>"
""" The author(s) of the module """

__copyright__ = "Copyright (c) 2008-2024 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "Apache License, Version 2.0"
""" The license for the module """

import colony


class ZipPlugin(colony.Plugin):
    """
    The main class for the Zip plugin.
    """

    id = "pt.hive.colony.plugins.misc.zip"
    name = "Zip"
    description = "A plugin to manage zip files"
    version = "1.0.0"
    author = "Hive Solutions Lda. <development@hive.pt>"
    platforms = [colony.CPYTHON_ENVIRONMENT]
    capabilities = ["zip"]
    main_modules = ["zip_c"]

    def load_plugin(self):
        colony.Plugin.load_plugin(self)
        import zip_c

        self.system = zip_c.Zip(self)

    def zip(self, zip_file_path, input_directory, file_path_list=None):
        """
        Compresses the contents of the provided directory into a zip file.

        :type zip_file_path: String
        :param zip_file_path: Full path to the zip file.
        :type input_directory: String
        :param input_directory: Full path to the directory one wants to compress.
        :type file_path_list: List
        :param file_path_list: List of relative file paths.
        """

        return self.system.zip(zip_file_path, input_directory, file_path_list)

    def unzip(self, zip_file_path, output_directory):
        """
        Extracts a zip file to the specified directory.

        :type file_path: String
        :param zip_file_path: Full path to the zip file.
        :type output_directory: String
        :param output_directory: Full path to the directory where one wants to extract the zip file to.
        """

        return self.system.unzip(zip_file_path, output_directory)

    def get_file_paths(self, file_path):
        """
        Returns a list with the paths to the files contained in the specified zip file.

        :type path: String
        :param path: Path to the zip file.
        :rtype: List
        :return: List of file paths.
        """

        return self.system.get_file_paths(file_path)

    def get_directory_paths(self, file_path):
        """
        Returns a list with the paths to the directories contained in the specified zip file.

        :type path: String
        :param path: Path to the zip file.
        :rtype: List
        :return: List of directory paths.
        """

        return self.system.get_directory_paths(file_path)
