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

import os
import random

import colony.libs.string_buffer_util

import PIL.Image
import PIL.ImageDraw
import PIL.ImageFont

RESOURCES_PATH = "captcha/resources"
""" The resources path """

DEFAULT_IMAGE_WIDTH = 300
""" The default image width """

DEFAULT_IMAGE_HEIGHT = 50
""" The default image height """

DEFAULT_NUMBER_LETTERS = 5
""" The default number of letters """

DEFAULT_FONT_SIZE = 36
""" The default font size """

IMAGE_WIDTH_VALUE = "image_width"
""" The image width value """

IMAGE_HEIGHT_VALUE = "image_height"
""" The image height value """

NUMBER_LETTERS_VALUE = "number_letters"
""" The number of letters value """

RGBA_VALUE = "RGBA"
""" The rgba value """

JPEG_VALUE = "jpeg"
""" The jpeg value """

class Captcha:
    """
    The captcha class.
    """

    captcha_plugin = None
    """ The captcha plugin """

    def __init__(self, captcha_plugin):
        """
        Constructor of the class.

        @type captcha_plugin: CaptchaPlugin
        @param captcha_plugin: The captcha plugin.
        """

        self.captcha_plugin = captcha_plugin

    def generate_captcha(self, string_value, properties):
        # retrieves the plugin manager
        plugin_manager = self.captcha_plugin.manager

        # tries to retrieve the image width
        image_width = properties.get(IMAGE_WIDTH_VALUE, DEFAULT_IMAGE_WIDTH)

        # tries to retrieve the image height
        image_height = properties.get(IMAGE_HEIGHT_VALUE, DEFAULT_IMAGE_HEIGHT)

        # tries to retrieve the number of letters
        number_letters = properties.get(NUMBER_LETTERS_VALUE, DEFAULT_NUMBER_LETTERS)

        # retrieves the captcha plugin path
        captcha_plugin_path = plugin_manager.get_plugin_path_by_id(self.captcha_plugin.id)

        # creates the resources path from the "base" captcha plugin path
        resources_path = captcha_plugin_path + "/" + RESOURCES_PATH

        # retrieves the font for the current resources path
        text_font = self._get_font(resources_path)

        # retrieves the pattern for the current resources path
        pattern = self._get_pattern(resources_path)

        # in case no string value is defined
        if not string_value:
            # generates a string value
            string_value = self._generate_string_value(number_letters)

        # creates a background image
        image = PIL.Image.new(RGBA_VALUE, (image_width, image_height), (255, 255, 255, 255))

        # fill the image with the pattern
        self._fill_pattern(image, pattern)

        # draw the string value into the image
        self._draw_text(image, text_font, string_value)

        # creates a new string buffer for the image
        string_buffer = colony.libs.string_buffer_util.StringBuffer()

        # saves the image into the string buffer
        image.save(string_buffer, JPEG_VALUE)

        # seeks the buffer to the beginning of the file
        string_buffer.seek(0)

        # returns a tuple with the string value and
        # the string buffer
        return (
            string_value,
            string_buffer
        )

    def generate_captcha_string_value(self, properties):
        # tries to retrieve the number of letters
        number_letters = properties.get(NUMBER_LETTERS_VALUE, DEFAULT_NUMBER_LETTERS)

        # generates the string value for the given number of letters
        string_value = self._generate_string_value(number_letters)

        # returns the generated string value
        return string_value

    def _generate_string_value(self, number_letters):
        """
        Generates a string value with the given number
        of letters.

        @type number_letters: int
        @param number_letters: The number of letters for the
        string value to be generated.
        @rtype: String
        @return: The generated string value.
        """

        # creates the list of letters
        letters_list = []

        # iterates over the number of letters
        for _index in range(number_letters):
            # generates a random letter
            letter = random.randint(97, 122)

            # adds the letter to the list of letters
            letters_list.append(chr(letter))

        # creates the string value by joining the
        # letters in the letters list
        string_value = "".join(letters_list)

        # returns the string value
        return string_value

    def _draw_text(self, image, text_font, string_value, rotate = True):
        # retrieves the image width and height
        image_width, image_height = image.size

        # creates a text image
        text_image = PIL.Image.new(RGBA_VALUE, (image_width, image_height), (255, 255, 255, 0))

        # creates the text draw (temporary) from the text image
        text_draw = PIL.ImageDraw.Draw(text_image)

        # in case the rotate flag is set
        if rotate:
            # draws the text into the text image in rotate mode
            text_size = self._draw_text_rotate(text_image, text_font, string_value)
        else:
            # draws the text into the text image in simple mode mode
            text_size = self._draw_text_simple(text_draw, text_font, string_value)

        # unpacks the text size retrieving the text width and height
        text_width, text_height = text_size

        # calculates the initial text x position
        initial_text_x = (image_width / 2) - (text_width / 2)

        # calculates the initial text y position
        initial_text_y = (image_height / 2) - (text_height / 2)

        # paste text image with the mask into the image
        image.paste(text_image, (initial_text_x, initial_text_y), text_image)

    def _draw_text_simple(self, text_draw, text_font, string_value):
        # draw the text to the text draw
        text_draw.text((0, 0), string_value, font = text_font, fill = (220, 220, 220))

        # retrieves the text size from the text font
        text_size = text_font.getsize(string_value)

        # returns the text size
        return text_size

    def _draw_text_rotate(self, text_image, text_font, string_value):
        # start the current letter x position
        current_letter_x = 0

        # start the maximum letter height
        maximum_letter_height = 0

        # iterates over all the letters in the string value
        for letter_value in string_value:
            # retrieves the letter width and height from the text font
            letter_width, letter_height = text_font.getsize(letter_value)

            # creates a letter image
            letter_image = PIL.Image.new(RGBA_VALUE, (letter_width, letter_height), (255, 255, 255, 0))

            # creates the letter draw (temporary) from the letter image
            letter_draw = PIL.ImageDraw.Draw(letter_image)

            # draw the text to the text draw
            letter_draw.text((0, 0), letter_value, font = text_font, fill = (220, 220, 220))

            # generates a random rotation angle
            rotation = random.randint(-45, 45)

            # rotates the text image
            letter_image = letter_image.rotate(rotation, PIL.Image.BICUBIC, 1)

            # retrieves the letter image width and height
            letter_image_width, letter_image_height = letter_image.size

            # paste letter image with the mask into the image
            text_image.paste(letter_image, (current_letter_x, 0), letter_image)

            # increments the current letter z position
            # with the letter width
            current_letter_x += letter_image_width

            # in case the current letter image height is the largest
            if letter_image_height > maximum_letter_height:
                # sets the maximum letter height as the
                # current letter image height
                maximum_letter_height = letter_image_height

        # creates the string value size tuple
        size = (current_letter_x, maximum_letter_height)

        # returns the string value size tuple
        return size

    def _fill_pattern(self, image, pattern):
        # retrieves the image width and height
        image_width, image_height = image.size

        # retrieves the pattern width and height
        pattern_width, pattern_height = pattern.size

        # sets the initial y position
        current_pattern_y = 0

        # iterates while there is height available
        while current_pattern_y < image_height:
            # sets the beginning of the line x position
            current_pattern_x = 0

            # iterates while there is width available
            while current_pattern_x < image_width:
                # "pastes"  the pattern into the image
                image.paste(pattern, (current_pattern_x, current_pattern_y))

                # increments the x position with the pattern width
                current_pattern_x += pattern_width

            # increments the y position with the pattern height
            current_pattern_y += pattern_height

    def _get_font(self, resources_path, font_name = None, font_size = DEFAULT_FONT_SIZE):
        # retrieves the fonts path for the resources path
        fonts_path = resources_path + "/fonts"

        # in case the font name is not defined
        if not font_name:
            # retrieves a random font name from the fonts path
            font_name = self._get_random_file_path(fonts_path, (".ttf", ".otf"))

        # creates the font full path from the font name
        # and the base fonts path
        font_full_path = fonts_path + "/" + font_name

        # loads the front for the given path and size
        font = PIL.ImageFont.truetype(font_full_path, font_size)

        # returns the font
        return font

    def _get_pattern(self, resources_path, pattern_name = None):
        # retrieves the fonts path for the resources path
        patterns_path = resources_path + "/patterns"

        # in case the pattern name is not defined
        if not pattern_name:
            # retrieves a random pattern name from the patterns path
            pattern_name = self._get_random_file_path(patterns_path, (".jpg", ".jpeg"))

        # creates the pattern full path from the pattern name
        # and the base patterns path
        pattern_full_path = patterns_path + "/" + pattern_name

        # opens the pattern file
        pattern = PIL.Image.open(pattern_full_path)

        # returns the pattern
        return pattern

    def _get_random_file_path(self, directory_path, extensions = []):
        # retrieves the list of files within
        # the directory path
        file_paths = os.listdir(directory_path)

        # filters the file paths based on the extensions
        file_paths = [value for value in file_paths if os.path.splitext(value)[1] in extensions]

        # retrieves the length of the list of file paths,
        # the quantity of files available
        file_paths_length = len(file_paths)

        # retrieves a random file index
        file_index = random.randint(0, file_paths_length - 1)

        # sets the "random" file path
        file_path = file_paths[file_index]

        # returns the file path
        return file_path
