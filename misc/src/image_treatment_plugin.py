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


class ImageTreatmentPlugin(colony.Plugin):
    """
    The main class for the Image Treatment plugin.
    """

    id = "pt.hive.colony.plugins.misc.image_treatment"
    name = "Image Treatment"
    description = "Image Treatment Plugin"
    version = "1.0.0"
    author = "Hive Solutions Lda. <development@hive.pt>"
    platforms = [colony.CPYTHON_ENVIRONMENT]
    capabilities = ["image_treatment"]
    dependencies = [colony.PackageDependency("Python Imaging Library (PIL)", "PIL")]
    main_modules = ["image_treatment_c"]

    def load_plugin(self):
        colony.Plugin.load_plugin(self)
        import image_treatment_c

        self.system = image_treatment_c.ImageTreatment(self)

    def resize_image(self, image_path, width, height):
        """
        Resizes the image in the given file path (or buffer)
        to the target width and height.
        The resizing is made stretching it if necessary.

        :type image_path: String/File
        :param image_path: The image path (or file) to be
        resized according to the specification.
        :type width: int
        :param width: The target width to the resize image.
        :type height: int
        :param height: The target height to the resize image.
        :rtype: File
        :return: The file object containing the buffer information
        on the resized image.
        """

        return self.system.resize_image(image_path, width, height)

    def resize_image_aspect(self, image_path, width, height):
        """
        Resizes the image in the given file path (or buffer)
        to the target width and height.
        The resizing is made respecting the original image
        aspect ratio.

        :type image_path: String/File
        :param image_path: The image path (or file) to be
        resized according to the specification.
        :type width: int
        :param width: The target width to the resize image.
        :type height: int
        :param height: The target height to the resize image.
        :rtype: File
        :return: The file object containing the buffer information
        on the resized image.
        """

        return self.system.resize_image_aspect(image_path, width, height)

    def resize_image_aspect_background(self, image_path, width, height):
        """
        Resizes the image in the given file path (or buffer)
        to the target width and height.
        The resizing is made respecting the original image
        aspect ratio.
        The (unused) background is set as transparent.

        :type image_path: String/File
        :param image_path: The image path (or file) to be
        resized according to the specification.
        :type width: int
        :param width: The target width to the resize image.
        :type height: int
        :param height: The target height to the resize image.
        :rtype: File
        :return: The file object containing the buffer information
        on the resized image.
        """

        return self.system.resize_image_aspect_background(image_path, width, height)

    def guess_image_type(self, data):
        """
        Uses a series of simplistic heuristics to determine the
        proper (image) mime type of the provided binary data.

        Note that the accuracy of this method is quite limited
        by its simplistic approach.

        :type data: String
        :param data: The string of bytes containing the data that
        is going to be used in the image type detection.
        :rtype: String
        :return: The detected mime type string value for the provided
        string of binary data.
        """

        return self.system.guess_image_type(data)
