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

__revision__ = "$LastChangedRevision: 421 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2008-11-20 15:16:53 +0000 (Qui, 20 Nov 2008) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import datetime

class TorrentParser:
    """
    The torrent parser class.
    """

    metafile_map = {}
    """ The map with the decoded metafile information """

    torrent_structure = None
    """ The torrent structure """

    def __init__(self, metafile_map):
        self.metafile_map = metafile_map

    def parse(self):
        self.torrent_structure = TorrentStructure()

        announce = self.metafile_map.get("announce", None)
        announce_list = self.metafile_map.get("announce-list", [])
        creation_date = self.metafile_map.get("creation date", None)
        comment = self.metafile_map.get("comment", None)
        created_by = self.metafile_map.get("created by", None)
        encoding = self.metafile_map.get("encoding", None)

        info_map = self.metafile_map.get("info", {})

        piece_length = info_map.get("piece length", None)
        pieces = info_map.get("pieces", None)
        name = info_map.get("name", None)
        files = info_map.get("files", [])

        self.torrent_structure.main_tracker_url = announce
        self.torrent_structure.tracker_url_list = announce_list
        self.torrent_structure.creation_date = datetime.datetime.fromtimestamp(int(creation_date))
        self.torrent_structure.comment = comment

        self.torrent_structure.author = created_by
        self.torrent_structure.encoding = encoding
        self.torrent_structure.piece_size = piece_length
        self.torrent_structure.pieces_hash_list = pieces
        self.torrent_structure.name = name

        self.torrent_structure.info_map = info_map

        for file in files:
            file_path = file.get("path", None)
            file_length = file.get("length", None)

            # creates a new file structure to hold the file
            # information
            file_structure = TorrentFile()

            file_structure.name = "/".join(file_path)
            file_structure.size = file_length

            self.torrent_structure.files.append(file_structure)

        print self.torrent_structure

    def get_value(self):
        return self.torrent_structure

    def get_torrent_structure(self):
        return self.torrent_structure

class TorrentStructure:
    """
    The torrent structure class, used to represent
    the properties of a torrent and its current state.
    """

    main_tracker_url = None
    """ The url to the main tracker """

    tracker_url_list = []
    """ The list of url to trackers """

    creation_date = None
    """ The date of creation of the torrent """

    comment = "none"
    """ A simple comment describing the torrent """

    author = "none"
    """ The original author of the torrent """

    encoding = "none"
    """ The encoding of the info part of the torrent """

    piece_size = None
    """ The size of each piece """

    pieces_hash_list = []
    """ The list containing the hashes of all pieces """

    name = "none"
    """ The name of the torrent file """

    files = []
    """ A list of files for the torrent """

    info_map = {}
    """ The info map of the torrent """

    def __init__(self):
        """
        Constructor of the class.
        """

        self.tracker_url_list = []
        self.pieces_hash_list = []
        self.files = []
        self.info_map = {}

class TorrentFile:
    """
    The torrent file structure, representing one of
    the internal file represented by the torrent.
    """

    name = "none"
    """ The name of the file """

    size = None
    """ The size (in bytes) of the file """

    def __init__(self, name = "none", size = None):
        """
        Constructor of the class.
        """

        self.name = name
        self.size = size

    def get_name(self):
        """
        Retrieves the name.

        @rtype: String
        @return: The name.
        """

        return self.name

    def set_name(self, name):
        """
        Sets the name.

        @type name: String
        @param name: The name.
        """

        self.name = name

    def get_size(self):
        """
        Retrieves the size.

        @rtype: int
        @return: The size.
        """

        return self.name

    def set_size(self, size):
        """
        Sets the size.

        @type size: int
        @param size: The size.
        """

        self.size = size
