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

__revision__ = "$LastChangedRevision: 72 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2008-10-21 23:29:54 +0100 (Ter, 21 Out 2008) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import os
import pysvn

HEAD_VALUE = "head"
""" The head value """

class Svn:
    """
    The svn class.
    """

    svn_plugin = None
    """ The svn plugin """

    svn_client = None
    """ The svn client instance """

    def __init__(self, svn_plugin):
        """
        Constructor of the class.

        @type svn_plugin: SvnPlugin
        @param svn_plugin: The svn plugin.
        """

        self.svn_plugin = svn_plugin

        # creates the base svn client
        self.create_base_svn_client()

    def create_base_svn_client(self):
        # retrieves the plugin manager
        manager = self.svn_plugin.manager

        # retrieves the svn plugin temporary path
        svn_plugin_temporary_path = manager.get_temporary_plugin_path_by_id(self.svn_plugin.id, "svn_client")

        # sets the svn client path path
        svn_client_path = svn_plugin_temporary_path

        # in case the svn client path does not exists
        if not os.path.exists(svn_client_path):
            # creates the directories to the svn client  path
            os.makedirs(svn_client_path)

        # creates the svn client
        self.svn_client = self.create_svn_client(svn_client_path)

    def create_svn_client(self, svn_client_path):
        # creates a new svn client instance
        svn_client = SvnClient(svn_client_path)

        # returns the created svn client
        return svn_client

    def svn_set_default_username(self, username):
        self.svn_client.svn_set_default_username(username)

    def svn_add_login(self, realm, username, password):
        self.svn_client.svn_add_login(realm, username, password)

    def svn_checkin(self, checkin_path, message):
        self.svn_client.svn_checkin(checkin_path, message)

    def svn_checkout(self, repository_url, checkout_directory, revision):
        self.svn_client.svn_checkout(repository_url, checkout_directory, revision)

    def svn_get_login_callback(self, realm, username, may_save):
        self.svn_client.svn_get_login_callback(realm, username, may_save)

class SvnClient:
    """
    The svn client class.
    """

    svn_client = None
    """ The pysvn client """

    svn_client_path = "."
    """ The svn client files path """

    svn_realm_login_map = {}
    """ The map associating the realm with the logins """

    def __init__(self, svn_client_path = "."):
        self.svn_realm_login_map = {}

        # sets the svn client path
        self.svn_client_path = svn_client_path

        # creates the svn client
        self.create_svn_client()

        # sets the svn callbacks
        self.set_svn_callbacks()

    def create_svn_client(self):
        # creates the svn client with the given svn client path
        self.svn_client = pysvn.Client(self.svn_client_path)

    def set_svn_callbacks(self):
        # sets the get login callback
        self.svn_client.callback_get_login = self.svn_get_login_callback

    def svn_set_default_username(self, username):
        self.svn_client.set_default_username(username)

    def svn_add_login(self, realm, username, password):
        if not realm in self.svn_realm_login_map:
            self.svn_realm_login_map[realm] = {}

        # retrieves the username password map
        realm_login_username_password_map = self.svn_realm_login_map[realm]

        # sets the username password relation
        realm_login_username_password_map[username] = password

    def svn_checkin(self, checkin_path, message):
        # sets the checkin path
        svn_checkin_path = checkin_path

        # sets the checkin message
        svn_checkin_message = message

        # checks in the given svn path with the given message
        self.svn_client.checkin(svn_checkin_path, svn_checkin_message)

    def svn_checkout(self, repository_url, checkout_directory, revision):
        # sets the repository url
        svn_repository_url = repository_url

        # sets the checkout directory
        svn_checkout_directory = checkout_directory

        # in case the revision is of type head
        if revision == HEAD_VALUE:
            # creates the pysvn revision object
            svn_revision = pysvn.Revision(pysvn.opt_revision_kind.head)

        # executes the checkout command
        self.svn_client.checkout(svn_repository_url, svn_checkout_directory, revision = svn_revision)

    def svn_get_login_callback(self, realm, username, may_save):
        # in case the realm does not exist in the realm login map
        if not realm in self.svn_realm_login_map:
            return

        # retrieves the username password map
        realm_login_username_password_map = self.svn_realm_login_map[realm]

        # in case the username exists in the map
        if username in realm_login_username_password_map:
            # retrieves the password for the given username
            password = realm_login_username_password_map[username]

            # returns the tuple representing the return code (valid/invalid), the username,
            # the password and the save (persist) data in the svn client directory
            return (
                True, username, password, False
            )
