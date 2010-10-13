#!/usr/bin/python
# -*- coding: Cp1252 -*-

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

DEFAULT_ENCODING = "utf-8"
""" The default encoding """

ADAPTER_VALUE = "adapter"
""" The adapter value """

PATH_VALUE = "path"
""" The path value """

TARGET_PATH_VALUE = "target_path"
""" The target path value """

REPOSITORY_PATH_VALUE = "repository_path_value"
""" The repository path value """

VERSION_FILE_PATH_VALUE = "version_file_path"
""" The version file path value """

PREVIOUS_VERSION_FILE_PATH_VALUE = "previous_version_file_path"
""" The previous version file path value """

CHANGELOG_FILE_PATH_VALUE = "changelog_file_path"
""" The changelog file path value """

NUMBER_VALUE = "number"
""" The number value """

IDENTIFIER_VALUE = "identifier"
""" The identifier value """

DATE_VALUE = "date"
""" The date value """

AUTHOR_VALUE = "author"
""" The author value """

MESSAGE_VALUE = "message"
""" The message value """

USER_VALUE = "user"
""" The user value """

VERSION_VALUE = "version"
""" The version value """

NAME_VALUE = "name"
""" The name list value """

USERNAME_VALUE = "username"
""" The username list value """

CHANGELOG_LIST_VALUE = "changelog_list"
""" The changelog list value """

CHANGERS_LIST_VALUE = "changers_list"
""" The changers list value """

UNKNOWN_VALUE = "Unknown"
""" The unknown value """

class RevisionControlBuildAutomationExtension:
    """
    The revision control build automation extension class.
    """

    revision_control_build_automation_extension_plugin = None
    """ The revision control build automation extension plugin """

    def __init__(self, revision_control_build_automation_extension_plugin):
        """
        Constructor of the class.

        @type revision_control_build_automation_extension_plugin: RevisionControlBuildAutomationExtensionPlugin
        @param revision_control_build_automation_extension_plugin: The revision control build automation extension plugin.
        """

        self.revision_control_build_automation_extension_plugin = revision_control_build_automation_extension_plugin

    def run_automation(self, plugin, stage, parameters, build_automation_structure, logger):
        # retrieves the revision control manager plugin
        revision_control_manager_plugin = self.revision_control_build_automation_extension_plugin.revision_control_manager_plugin

        # retrieves the build automation structure runtime
        build_automation_structure_runtime = build_automation_structure.runtime

        # retrieves the required parameters
        adapter = parameters[ADAPTER_VALUE]
        path = parameters[PATH_VALUE]
        target_path = parameters[TARGET_PATH_VALUE]
        version_file_path = parameters.get(VERSION_FILE_PATH_VALUE, None)
        previous_version_file_path = parameters.get(PREVIOUS_VERSION_FILE_PATH_VALUE, None)
        changelog_file_path = parameters.get(CHANGELOG_FILE_PATH_VALUE, None)

        # creates the revision control parameters
        revision_control_parameters = {REPOSITORY_PATH_VALUE : target_path}

        # loads a new revision control manager for the specified adapter name
        revision_control_manager = revision_control_manager_plugin.load_revision_control_manager(adapter, revision_control_parameters)

        # in case the target path already exists
        if os.path.exists(target_path):
            # print an info message
            logger.info("Running cleanup in %s" % target_path)

            # cleans the repository from locks
            revision_control_manager.cleanup([target_path])

            # print an info message
            logger.info("Running revert in %s" % target_path)

            # reverts the repository to the previous version
            # and removes unnecessary files
            revision_control_manager.revert([target_path])

            # print an info message
            logger.info("Running update in %s" % target_path)

            # updates the repository to the current head revision
            revision = revision_control_manager.update([target_path], None)
        else:
            # print an info message
            logger.info("Checking out repository %s out into %s" % (path, target_path))

            # checks out the repository to the target path
            revision = revision_control_manager.checkout(path, target_path)

        # in case the version file path is defined
        if version_file_path:
            # print an info message
            logger.info("Writing version number to file %s" % version_file_path)

            # writes the version number to the file
            self._write_version_number(version_file_path, revision)

        # in case previous version file path and the changelog file path are defined
        if previous_version_file_path and changelog_file_path:
            # print an info message
            logger.info("Writing changelog to file %s" % changelog_file_path)

            # retrieves the current revision number
            current_revision_number = revision.get_number()

            # reads the previous revision number from the
            previous_revision_number = self._read_version_number(previous_version_file_path)

            # in case the previous revision number is defined
            if previous_revision_number:
                # sets the base revision number as the previous revision
                # number plus one in case it's less than the current version
                # otherwise the base version is the current version
                base_revision_number = previous_revision_number < current_revision_number and previous_revision_number + 1 or current_revision_number
            # otherwise
            else:
                # sets the base revision number as invalid (start from zero)
                base_revision_number = None

            # retrieves the log of revision in the revision
            revision_list = revision_control_manager.log([target_path], base_revision_number, current_revision_number)

            # converts the revision list into a changelog list
            changelog_list = self._convert_revision_list_changelog(revision_list)

            # creates the changers list from the the revision list
            changers_list = self._create_changers_list(revision_list)

            # writes the changelog for the given file path and changelog list
            self._write_changelog(changelog_file_path, changelog_list)

        # sets the build automation structure runtime properties
        build_automation_structure_runtime.properties[VERSION_VALUE] = current_revision_number
        build_automation_structure_runtime.properties[CHANGELOG_LIST_VALUE] = changelog_list
        build_automation_structure_runtime.properties[CHANGERS_LIST_VALUE] = changers_list

        # returns true (success)
        return True

    def _read_version_number(self, version_file_path):
        # in case the version file path does not exist
        if not os.path.exists(version_file_path):
            # returns invalid
            return None

        # opens the version file
        version_file = open(version_file_path, "rb")

        try:
            # reads the revision number string value
            revision_number_string = version_file.read()

            # strips the revision number string
            revision_number_string = revision_number_string.strip()

            # converts the revision number string to integer
            revision_number = int(revision_number_string)
        finally:
            # closes the version file
            version_file.close()

        # returns the revision number
        return revision_number

    def _write_version_number(self, version_file_path, revision):
        # retrieves the revision number
        revision_number = revision.get_number()

        # converts the revision number to a string
        revision_number_string = str(revision_number)

        # opens the version file
        version_file = open(version_file_path, "wb")

        try:
            # writes the revision number string value
            version_file.write(revision_number_string)
        finally:
            # closes the version file
            version_file.close()

    def _write_changelog(self, changelog_file_path, changelog_list):
        # retrieves the json plugin
        json_plugin = self.revision_control_build_automation_extension_plugin.json_plugin

        # dumps (pretty) the changelog list using the json plugin
        changelog_json = json_plugin.dumps_pretty(changelog_list)

        # encodes the changelog json using the default encoding
        changelog_json_encoded = changelog_json.encode(DEFAULT_ENCODING)

        # opens the changelog file
        changelog_file = open(changelog_file_path, "wb")

        try:
            # writes the encoded changelog json
            changelog_file.write(changelog_json_encoded)
        finally:
            # closes the changelog file
            changelog_file.close()

    def _convert_revision_list_changelog(self, revision_list):
        # retrieves the information user plugin
        information_user_plugin = self.revision_control_build_automation_extension_plugin.information_user_plugin

        # creates the list to hold the changelog elements
        changelog_list = []

        # iterates over all the revision items in the revision
        # list to create the changelog elements
        for revision_item in revision_list:
            # retrieves the revision item attributes
            revision_item_number = revision_item.get_number()
            revision_item_identifier = revision_item.get_identifier()
            revision_item_date = revision_item.get_date()
            revision_item_author = revision_item.get_author()
            revision_item_message = revision_item.get_message()

            # retrieves the user from the information user plugin
            # using the revision item author as key
            revision_item_user = information_user_plugin.get_user_information_user_key(revision_item_author)

            # creates the changelog element using the attributes
            changelog_element = {}
            changelog_element[NUMBER_VALUE] = revision_item_number
            changelog_element[IDENTIFIER_VALUE] = revision_item_identifier
            changelog_element[DATE_VALUE] = revision_item_date
            changelog_element[AUTHOR_VALUE] = revision_item_author
            changelog_element[MESSAGE_VALUE] = revision_item_message
            changelog_element[USER_VALUE] = revision_item_user

            # adds the changelog element to the changelog list
            changelog_list.append(changelog_element)

        # returns the changelog list
        return changelog_list

    def _create_changers_list(self, revision_list):
        # retrieves the information user plugin
        information_user_plugin = self.revision_control_build_automation_extension_plugin.information_user_plugin

        # creates the list to hold the changers elements
        changers_list = []

        # iterates over all the revision items in the revision
        # list to create the changer elements
        for revision_item in revision_list:
            # retrieves the revision author
            revision_item_author = revision_item.get_author()

            # retrieves the changer element from the information user plugin
            # using the revision item author as key
            changer_element = information_user_plugin.get_user_information_user_key(revision_item_author)

            # in case the changer element does not exit in the changers lisr
            if not changer_element in changers_list:
                # adds the changer element to the changers list
                changers_list.append(changer_element)

        # returns the changers list
        return changers_list
