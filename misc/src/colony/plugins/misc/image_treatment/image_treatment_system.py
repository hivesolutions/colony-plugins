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

import types

import PIL.Image

import colony.libs.string_buffer_util

SEEK_VALUE = "seek"
""" The seeek value """

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

    def resize_image(self, image_path, width, height, image_type = JPEG_VALUE):
        """
        Resizes the image in the given file path (or buffer)
        to the target width and height.
        The resizing is made stretching it if necessary.

        @type image_path: String/File
        @param image_path: The image path (or file) to be
        resized according to the specification.
        @type width: int
        @param width: The target width to the resize image.
        @type height: int
        @param height: The target height to the resize image.
        @type image_type: String
        @param image_type: The target image type to the resize image.
        @rtype: File
        @return: The file object containing the buffer information
        on the resized image.
        """

        # resets the image path
        self._reset_image_path(image_path)

        # opens the image file
        image = PIL.Image.open(image_path)

        # resizes the images
        image_resize = image.resize((width, height), PIL.Image.ANTIALIAS)

        # creates a new string buffer for the image
        string_buffer = colony.libs.string_buffer_util.StringBuffer(False)

        # saves the image into the string buffer
        image_resize.save(string_buffer, image_type)

        # seeks the buffer to the beginning of the file
        string_buffer.seek(0)

        # returns the string buffer
        return string_buffer

    def resize_image_aspect(self, image_path, width, height, image_type = PNG_VALUE):
        """
        Resizes the image in the given file path (or buffer)
        to the target width and height.
        The resizing is made respecting the original image
        aspect ratio.

        @type image_path: String/File
        @param image_path: The image path (or file) to be
        resized according to the specification.
        @type width: int
        @param width: The target width to the resize image.
        @type height: int
        @param height: The target height to the resize image.
        @type image_type: String
        @param image_type: The target image type to the resize image.
        @rtype: File
        @return: The file object containing the buffer information
        on the resized image.
        """

        # resets the image path
        self._reset_image_path(image_path)

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
        return self.resize_image(image_path, resize_width, resize_height, image_type)

    def resize_image_aspect_background(self, image_path, width, height, image_type = PNG_VALUE):
        """
        Resizes the image in the given file path (or buffer)
        to the target width and height.
        The resizing is made respecting the original image
        aspect ratio.
        The (unused) background is set as transparent.

        @type image_path: String/File
        @param image_path: The image path (or file) to be
        resized according to the specification.
        @type width: int
        @param width: The target width to the resize image.
        @type height: int
        @param height: The target height to the resize image.
        @type image_type: String
        @param image_type: The target image type to the resize image.
        @rtype: File
        @return: The file object containing the buffer information
        on the resized image.
        """

        # retrieves the resized image
        resized_image_file = self.resize_image_aspect(image_path, width, height)

        # resets the image path
        self._reset_image_path(image_path)

        # opens the resized image file
        resized_image = PIL.Image.open(resized_image_file)

        # retrieves the resized image width and the resized image height
        resized_image_width, resized_image_height = resized_image.size

        # creates the new image
        new_image = PIL.Image.new(RGBA_VALUE, (width, height))

        # pastes the resized image into the new image
        new_image.paste(resized_image, ((width - resized_image_width) / 2, (height - resized_image_height) / 2))

        # creates a new string buffer for the image
        string_buffer = colony.libs.string_buffer_util.StringBuffer(False)

        # saves the new image into the string buffer
        new_image.save(string_buffer, image_type)

        # seeks the buffer to the beginning of the file
        string_buffer.seek(0)

        # returns the new image
        return string_buffer

    def _reset_image_path(self, image_path):
        """
        Resets the image path in order to make it ready
        for file opening.

        @type image_path: String/File
        @param image_path: The image path (or file) to be
        set ready for file opening.
        """

        # retrieves the image path type
        image_path_type = type(image_path)

        # in case the image path is of type string
        if image_path_type == types.StringType:
            # returns immediately (nothing
            # to do)
            return

        # in case the image path contains the seek
        # attribute (file object)
        if hasattr(image_path, SEEK_VALUE):
            # sets the image (path) to
            # the original position
            image_path.seek(0)
