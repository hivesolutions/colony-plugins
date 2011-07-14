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

__revision__ = "$LastChangedRevision: 7147 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2009-12-21 16:50:46 +0000 (seg, 21 Dez 2009) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import xmlrpclib

ENCODER_NAME = "xml"
""" The encoder name """

CONTENT_TYPE = "text/xml"
""" The content type """

class MainRestEncoderXml:
    """
    The main rest encoder xml class.
    """

    main_rest_encoder_xml_plugin = None
    """ The main rest encoder xml plugin """

    def __init__(self, main_rest_encoder_xml_plugin):
        """
        Constructor of the class.

        @type main_rest_encoder_xml_plugin: MainRestEncoderXmlPlugin
        @param main_rest_encoder_xml_plugin: The main rest encoder xml plugin.
        """

        self.main_rest_encoder_xml_plugin = main_rest_encoder_xml_plugin

    def get_encoder_name(self):
        """
        Retrieves the encoder name.

        @rtype: String
        @return: The encoder name.
        """

        return ENCODER_NAME

    def get_content_type(self):
        """
        Retrieves the content type.

        @rtype: String
        @return: The content type.
        """

        return CONTENT_TYPE

    def encode_value(self, value):
        """
        Encodes the given value.

        @type value: Object
        @param value: The value to be encoded.
        @rtype: String
        @return: The encoded value.
        """

        # encodes the value into xml
        encoded_value = xmlrpclib.dumps((value,), None, True, allow_none = True)

        # returns the encoded value
        return encoded_value
