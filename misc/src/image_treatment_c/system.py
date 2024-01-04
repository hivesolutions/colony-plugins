#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Colony Framework
# Copyright (c) 2008-2023 Hive Solutions Lda.
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

__copyright__ = "Copyright (c) 2008-2023 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "Apache License, Version 2.0"
""" The license for the module """

import PIL.Image

import colony

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

class ImageTreatment(colony.System):
    """
    The image treatment class.
    """

    def resize_image(self, image_path, width, height, image_type = JPEG_VALUE):
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
        :type image_type: String
        :param image_type: The target image type to the resize image.
        :rtype: File
        :return: The file object containing the buffer information
        on the resized image.
        """

        # resets the image path
        self._reset_image_path(image_path)

        # opens the image file, resizes the image
        # ands saves it into an in memory buffer
        # setting the offset position to the initial one
        image = PIL.Image.open(image_path)
        algorithm = PIL.Image.ANTIALIAS if hasattr(PIL.Image, "ANTIALIAS") else\
            (PIL.Image.LANCZOS if hasattr(PIL.Image, "LANCZOS") else None)
        image_resize = image.resize((width, height), algorithm)
        string_buffer = colony.StringBuffer(False)
        image_resize.save(string_buffer, image_type)
        string_buffer.seek(0)

        # returns the string buffer
        return string_buffer

    def resize_image_aspect(self, image_path, width, height, image_type = PNG_VALUE):
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
        :type image_type: String
        :param image_type: The target image type to the resize image.
        :rtype: File
        :return: The file object containing the buffer information
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

        :type image_path: String/File
        :param image_path: The image path (or file) to be
        resized according to the specification.
        :type width: int
        :param width: The target width to the resize image.
        :type height: int
        :param height: The target height to the resize image.
        :type image_type: String
        :param image_type: The target image type to the resize image.
        :rtype: File
        :return: The file object containing the buffer information
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
        new_image.paste(
            resized_image,
            (
                int((width - resized_image_width) / 2),
                int((height - resized_image_height) / 2)
            )
        )

        # creates a new string buffer for the image
        string_buffer = colony.StringBuffer(False)

        # saves the new image into the string buffer
        new_image.save(string_buffer, image_type)

        # seeks the buffer to the beginning of the file
        string_buffer.seek(0)

        # returns the new image
        return string_buffer

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

        if data[:4] == b"\xff\xd8\xff\xe0" and data[6:11] == b"JFIF\0": return "image/jpeg"
        elif data[1:4] == b"PNG": return "image/png"
        elif data[:2] == b"BM": return "image/x-ms-bmp"
        else: return "image/unknown-type"

    def _reset_image_path(self, image_path):
        """
        Resets the image path in order to make it ready
        for file opening.

        :type image_path: String/File
        :param image_path: The image path (or file) to be
        set ready for file opening.
        """

        # retrieves the image path type
        image_path_type = type(image_path)

        # in case the image path is of type string
        # (also known as bytes for buffer parsing)
        if image_path_type == colony.legacy.BYTES:
            # returns immediately (nothing
            # to do)
            return

        # in case the image path contains the seek
        # attribute (file object)
        if hasattr(image_path, SEEK_VALUE):
            # sets the image (path) to
            # the original position
            image_path.seek(0)
