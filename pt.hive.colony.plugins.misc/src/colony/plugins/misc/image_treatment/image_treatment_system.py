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

__author__ = "João Magalhães <joamag@hive.pt>"
""" The author(s) of the module """

__version__ = "1.0.0"
""" The version of the module """

__revision__ = "$LastChangedRevision: 1089 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2009-01-22 23:19:39 +0000 (qui, 22 Jan 2009) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import cStringIO

import PIL.Image

RGBA_VALUE = "RGBA"
""" The rgba value """

JPEG_VALUE = "jpeg"
""" The jpeg value """

PNG_VALUE = "png"
""" The png value """

MAXIMUM_SIZE = 2147483647
""" The maximum size value """

class ImageTreatment:
    """
    The image treatment class.
    """

    image_treatment_plugin = None
    """ The image treatment plugin """

    def __init__(self, image_treatment_plugin):
        """
        Constructor of the class.

        @type image_treatment_plugin: ImageTreatmentPlugin
        @param image_treatment_plugin: The image treatment plugin.
        """

        self.image_treatment_plugin = image_treatment_plugin

    def resize_image(self, image_path, width, height):
        # opens the image file
        image = PIL.Image.open(image_path)

        # resizes the images
        image_resize = image.resize((width, height), PIL.Image.ANTIALIAS)

        # creates a new string buffer for the image
        string_buffer = cStringIO.StringIO()

        # saves the image into the string buffer
        image_resize.save(string_buffer, JPEG_VALUE)

        # seeks the buffer to the beginning of the file
        string_buffer.seek(0)

        # returns the string buffer
        return string_buffer

    def resize_image_aspect(self, image_path, width, height):
        # opens the image file
        image = PIL.Image.open(image_path)

        # retrieves the image width and the image height
        image_width, image_height = image.size

        # calculates the width and height ratios
        ratio_width = width and float(width) / float(image_width) or MAXIMUM_SIZE
        ratio_height = height and float(height) / float(image_height) or MAXIMUM_SIZE

        # checks if the image is landscape or portrait
        if ratio_width < ratio_height:
            ratio = ratio_width
        else:
            ratio = ratio_height

        # calculates the resize image dimensions
        resize_width = int(image_width * ratio)
        resize_height = int(image_height * ratio)

        # returns the resized image
        return self.resize_image(image_path, resize_width, resize_height)

    def resize_image_aspect_background(self, image_path, width, height):
        # retrieves the resized image
        resized_image_file = self.resize_image_aspect(image_path, width, height)

        # opens the resized image file
        resized_image = PIL.Image.open(resized_image_file)

        # retrieves the resized image width and the resized image height
        resized_image_width, resized_image_height = resized_image.size

        # creates the new image
        new_image = PIL.Image.new(RGBA_VALUE, (width, height))

        # pastes the resized image into the new image
        new_image.paste(resized_image, ((width - resized_image_width) / 2, (height - resized_image_height) / 2))

        # creates a new string buffer for the image
        string_buffer = cStringIO.StringIO()

        # saves the new image into the string buffer
        new_image.save(string_buffer, PNG_VALUE)

        # seeks the buffer to the beginning of the file
        string_buffer.seek(0)

        # returns the new image
        return string_buffer
