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

import colony.base.system

class ImageTreatmentPlugin(colony.base.system.Plugin):
    """
    The main class for the Image Treatment plugin.
    """

    id = "pt.hive.colony.plugins.misc.image_treatment"
    name = "Image Treatment"
    description = "Image Treatment Plugin"
    version = "1.0.0"
    author = "Hive Solutions Lda. <development@hive.pt>"
    loading_type = colony.base.system.EAGER_LOADING_TYPE
    platforms = [
        colony.base.system.CPYTHON_ENVIRONMENT
    ]
    attributes = {
        "build_automation_file_path" : "$base{plugin_directory}/misc/image_treatment/resources/baf.xml"
    }
    capabilities = [
        "image_treatment",
        "build_automation_item"
    ]
    dependencies = [
        colony.base.system.PackageDependency("Python Imaging Library (PIL)", "PIL", "1.1.x", "http://www.pythonware.com/products/pil")
    ]
    main_modules = [
        "misc.image_treatment.image_treatment_system"
    ]

    image_treatment = None
    """ The image treatment """

    def load_plugin(self):
        colony.base.system.Plugin.load_plugin(self)
        import misc.image_treatment.image_treatment_system
        self.image_treatment = misc.image_treatment.image_treatment_system.ImageTreatment(self)

    def end_load_plugin(self):
        colony.base.system.Plugin.end_load_plugin(self)

    def unload_plugin(self):
        colony.base.system.Plugin.unload_plugin(self)

    def end_unload_plugin(self):
        colony.base.system.Plugin.end_unload_plugin(self)

    def load_allowed(self, plugin, capability):
        colony.base.system.Plugin.load_allowed(self, plugin, capability)

    def unload_allowed(self, plugin, capability):
        colony.base.system.Plugin.unload_allowed(self, plugin, capability)

    def dependency_injected(self, plugin):
        colony.base.system.Plugin.dependency_injected(self, plugin)

    def resize_image(self, image_path, width, height):
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
        @rtype: File
        @return: The file object containing the buffer information
        on the resized image.
        """

        return self.image_treatment.resize_image(image_path, width, height)

    def resize_image_aspect(self, image_path, width, height):
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
        @rtype: File
        @return: The file object containing the buffer information
        on the resized image.
        """

        return self.image_treatment.resize_image_aspect(image_path, width, height)

    def resize_image_aspect_background(self, image_path, width, height):
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
        @rtype: File
        @return: The file object containing the buffer information
        on the resized image.
        """

        return self.image_treatment.resize_image_aspect_background(image_path, width, height)
