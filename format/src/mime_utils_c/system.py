#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Colony Framework
# Copyright (c) 2008-2018 Hive Solutions Lda.
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

__version__ = "1.0.0"
""" The version of the module """

__revision__ = "$LastChangedRevision$"
""" The revision number of the module """

__date__ = "$LastChangedDate$"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008-2018 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "Apache License, Version 2.0"
""" The license for the module """

import os

import colony

CONTENT_TYPE_VALUE = "Content-Type"
""" The content type value, to be used in the definition
of the ender that contains the content type """

CONTENT_TRANSFER_ENCODING_VALUE = "Content-Transfer-Encoding"
""" The content transfer encoding value, the name
of the header that defines the type of transfer encoding """

CONTENT_ID_VALUE = "Content-ID"
""" The content id value, representing the header that identifies
in an unique way the attachment to be inserted """

BASE64_VALUE = "base64"
""" The base 64 value representing the type of transfer encoding
where the contents are encoded using the base 64 encoding """

DEFAULT_MIME_TYPE = "application/octet-stream"
""" The default mime type for an attachment based part, to be
used in connection with the base 64 (transfer) encoding """

class MimeUtils(colony.System):
    """
    The mime utils class, responsible for the management
    of extra functions related with the mime standard.
    """

    def add_mime_message_attachment_contents(self, mime_message, contents, file_name, mime_type = None):
        # retrieves the mime plugin
        mime_plugin = self.plugin.mime_plugin

        # creates the mime message part for the attachment
        mime_message_attachment_part = mime_plugin.create_message_part({})

        # creates the content id from the file name
        content_id = "<" + file_name + ">"

        # retrieves the mime type
        mime_type = mime_type or DEFAULT_MIME_TYPE

        # creates the content type from the mime type and the file name
        content_type = mime_type + ";name=\"" + file_name + "\""

        # sets the mime message attachment part headers
        mime_message_attachment_part.write_base_64(contents)
        mime_message_attachment_part.set_header(CONTENT_TYPE_VALUE, content_type)
        mime_message_attachment_part.set_header(CONTENT_TRANSFER_ENCODING_VALUE, BASE64_VALUE)
        mime_message_attachment_part.set_header(CONTENT_ID_VALUE, content_id)

        # adds the mime message attachment part to the mime message
        mime_message.add_part(mime_message_attachment_part)

    def add_mime_message_contents(self, mime_message, contents_path, content_extensions, recursive = True):
        # lists the directory, retrieving the directory entries
        directory_entries = os.listdir(contents_path)

        # iterates over all the directory entries
        for directory_entry in directory_entries:
            # creates the content path appending the directory entry (name)
            # to the (base) contents path
            content_path = os.path.join(contents_path, directory_entry)

            # retrieves the content extension from the content path
            content_extension = os.path.splitext(content_path)[1].lstrip(".")

            # in case the content path refers a directory
            if recursive and os.path.isdir(content_path):
                # adds the directory contents
                self.add_mime_message_contents(mime_message, content_path, content_extensions, recursive)
            elif content_extension in content_extensions:
                # adds the content to the mime message
                self._add_mime_message_content(mime_message, content_path)

    def _add_mime_message_content(self, mime_message, content_path):
        # retrieves the mime plugin
        mime_plugin = self.plugin.mime_plugin

        # creates the mime message part for the content
        mime_message_content_part = mime_plugin.create_message_part({})

        # opens the content file
        content_file = open(content_path, "rb")

        try:
            # reads the content file contents
            content_file_contents = content_file.read()

            # writes the content file contents in base 64 to
            # the mime message content part
            mime_message_content_part.write_base_64(content_file_contents)

            # retrieves the content rtype for the file name
            content_type = mime_plugin.get_mime_type_file_name(content_path)

            # retrieves the base name from the content path
            base_name = os.path.basename(content_path)

            # creates the content id from the base name
            content_id = "<" + base_name + ">"

            # sets the mime message content part headers
            mime_message_content_part.set_header(CONTENT_TYPE_VALUE, content_type)
            mime_message_content_part.set_header(CONTENT_TRANSFER_ENCODING_VALUE, BASE64_VALUE)
            mime_message_content_part.set_header(CONTENT_ID_VALUE, content_id)

            # adds the mime message content part to the mime message
            mime_message.add_part(mime_message_content_part)
        finally:
            # closes the content file
            content_file.close()
