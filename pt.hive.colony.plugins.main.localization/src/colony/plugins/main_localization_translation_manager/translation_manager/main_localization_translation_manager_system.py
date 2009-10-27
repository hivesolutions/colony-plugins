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

__revision__ = "$LastChangedRevision: 5629 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2009-10-19 10:11:40 +0100 (seg, 19 Out 2009) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import re

BUNDLES_VALUE = "bundles"
""" The bundles value """

OPTIONS_REGEX = "(?<=\{)[a-zA-Z0-9_]*(?=\})"
""" The options regular expression """

class MainLocalizationTranslationManager:
    """
    The main localization translation manager class.
    """

    main_localization_translation_manager_plugin = None
    """ The main localization translation manager plugin """

    localization_translation_bundle_handler_name_localization_translation_bundle_handler_plugin_map = {}
    """ The localization translation bundle handler name localization translation bundle handler plugin map """

    localization_translation_bundle_type_localization_translation_bundles_map = {}
    """ The localization translation bundle type localization translation bundles map """

    localization_translation_bundle_locale_identifier_localization_translation_bundles_map = {}
    """ The localization translation bundle locale identifier localization translation bundles map """

    localization_translation_bundle_locale_identifier_translation_map = {}
    """ The localization translation bundle locale identifier translation map """

    options_regex = None
    """ The options regular expression """

    def __init__(self, main_localization_translation_manager_plugin):
        """
        Constructor of the class.

        @type main_localization_translation_manager_plugin: MainLocalizationTranslationManagerPlugin
        @param main_localization_translation_manager_plugin: The main localization translation manager plugin.
        """

        self.main_localization_translation_manager_plugin = main_localization_translation_manager_plugin

        self.localization_translation_bundle_handler_name_localization_translation_bundle_handler_plugin_map = {}
        self.localization_translation_bundle_type_localization_translation_bundles_map = {}
        self.localization_translation_bundle_locale_identifier_localization_translation_bundles_map = {}
        self.localization_translation_bundle_locale_identifier_translation_map = {}

        # compiles the options regular expression
        self.options_regex = re.compile(OPTIONS_REGEX)

    def load_localization_translation_bundle_handler_plugin(self, localization_translation_bundle_handler_plugin):
        # retrieves the localization translation bundle handler name
        localization_translation_bundle_handler_name = localization_translation_bundle_handler_plugin.get_handler_name()

        # sets the localization translation bundle handler plugin
        self.localization_translation_bundle_handler_name_localization_translation_bundle_handler_plugin_map[localization_translation_bundle_handler_name] = localization_translation_bundle_handler_plugin

    def load_localization_translation_bundle_plugin(self, localization_translation_bundle_plugin):
        # generates the translation bundle
        translation_bundle = self._generate_translation_bundle(localization_translation_bundle_plugin)

        # retrieves the translation bundle type
        translation_bundle_type = translation_bundle.get_bundle_type()

        # retrieves the translation bundle locale identifier
        translation_bundle_locale_identifier = translation_bundle.get_bundle_locale_identifier()

        # retrieves the translation bundle namespace
        translation_bundle_namespace = translation_bundle.get_bundle_namespace()

        # in case the translation bundle type is not defined in the localization translation bundle type localization translation bundles map
        if not translation_bundle_type in self.localization_translation_bundle_type_localization_translation_bundles_map:
            self.localization_translation_bundle_type_localization_translation_bundles_map[translation_bundle_type] = []

        # retrieves the localization translation bundles list for the translation bundle type
        localization_translation_bundles_list = self.localization_translation_bundle_type_localization_translation_bundles_map[translation_bundle_type]

        # adds the translation bundle to the localization translation bundles list
        localization_translation_bundles_list.append(translation_bundle)

        # in case the translation bundle type is not defined in the localization translation bundle locale identifier localization translation bundles map
        if not translation_bundle_type in self.localization_translation_bundle_locale_identifier_localization_translation_bundles_map:
            self.localization_translation_bundle_locale_identifier_localization_translation_bundles_map[translation_bundle_locale_identifier] = {}

        # retrieves the localization translation bundles map the translation bundle locale identifier
        localization_translation_bundles_map = self.localization_translation_bundle_locale_identifier_localization_translation_bundles_map[translation_bundle_locale_identifier]

        # splits the translation bundle namespace
        translation_bundle_namespace_splitted = translation_bundle_namespace.split(".")

        for translation_bundle_namespace_split in translation_bundle_namespace_splitted:
            if not translation_bundle_namespace_split in localization_translation_bundles_map:
                localization_translation_bundles_map[translation_bundle_namespace_split] = {}

            localization_translation_bundles_map = localization_translation_bundles_map[translation_bundle_namespace_split]

        if not BUNDLES_VALUE in localization_translation_bundles_map:
            localization_translation_bundles_map[BUNDLES_VALUE] = []

        localization_translation_bundles_list = localization_translation_bundles_map[BUNDLES_VALUE]

        # adds the translation bundle to the localization translation bundles list
        localization_translation_bundles_list.append(translation_bundle)

    def unload_localization_translation_bundle_handler_plugin(self, localization_translation_bundle_handler_plugin):
        pass

    def unload_localization_translation_bundle_plugin(self, localization_translation_bundle_plugin):
        pass

    def get_locale(self, locale_identifier, locale_type, locale_properties):
        """
        Retrieves the locale for the given local identifier, locale type and local properties.

        @type locale_identifier: String
        @param locale_identifier: The identifier of the local to retrieve.
        @type locale_type: String
        @param locale_type: The type of the local to retrieve.
        @type locale_properties: Map
        @param locale_properties: The properties of the local to retrieve.
        @rtype: Object
        @return: The locale for the given locale type and local properties.
        """

        return None

    def get_locale_string(self, locale_identifier, locale_string, locale_string_properties):
        # splits the locale string
        locale_string_splitted = locale_string.split(".")

        # retrieves the local string namespace list from the locale string splitted
        locale_string_namespace_list = locale_string_splitted[:-1]

        # retrieves the translation bundles for the given
        # locale identifier and locale string namespace list, this method assures the loading
        # of the bundles
        self.get_translation_bundles(locale_identifier, locale_string_namespace_list)

        if not locale_identifier in self.localization_translation_bundle_locale_identifier_translation_map:
            return None

        # retrieves the translation map
        translation_map = self.localization_translation_bundle_locale_identifier_translation_map[locale_identifier]

        if not locale_string in translation_map:
            return None

        # retrieves the translation item map
        translation_item_map = translation_map[locale_string]

        # creates the locale string properties string
        locale_string_properties_string = "".join(locale_string_properties.keys())

        if not locale_string_properties_string in translation_item_map:
            return None

        # retrieves the translation string for the given locale string properties string
        translation_string = translation_item_map[locale_string_properties_string]

        # in case there are local string properties defined
        if locale_string_properties:
            # in case the format method is not defined in the translation string
            # python interpreter older than 2.6
            if not translation_string.format:
                # sets the string format method
                translation_string.format = self._string_format

            # formats the translation string retrieving the real translation string
            translation_string = translation_string.format(translation_string, **locale_string_properties)

        # returns the translation string
        return translation_string

    def get_translation_bundles(self, locale_identifier, namespace_list):
        if not locale_identifier in self.localization_translation_bundle_locale_identifier_localization_translation_bundles_map:
            return []

        # retrieves the localization translation map
        localization_translation_bundles_map = self.localization_translation_bundle_locale_identifier_localization_translation_bundles_map[locale_identifier]

        # iterates over all the namespace items in the namespace list
        for namespace_item in namespace_list:
            if not namespace_item in localization_translation_bundles_map:
                return []

            # sets the current localization translation bundles map
            localization_translation_bundles_map = localization_translation_bundles_map[namespace_item]

        if not BUNDLES_VALUE in localization_translation_bundles_map:
            return []

        # retrieves the translation bundles list for the current
        # translation map
        translation_bundles_list = localization_translation_bundles_map[BUNDLES_VALUE]

        # iterates over all the translation bundle in the
        # translation bundles list
        for translation_bundle in translation_bundles_list:
            # in case the translation bundle is not loaded
            if not translation_bundle.is_loaded():
                # loads the translation bundle
                self.load_translation_bundle(translation_bundle)

        # returns the translation bundles list
        return translation_bundles_list

    def load_translation_bundle(self, translation_bundle):
        self.main_localization_translation_manager_plugin.debug("Loading translation bundle: %s" % translation_bundle)

        # loads the translation bundle
        self._load_translation_bundle(translation_bundle)

        # sets the loaded flag in the translation bundle
        translation_bundle.set_loaded(True)

    def _generate_translation_bundle(self, localization_translation_bundle_plugin):
        # retrieves the bundle path
        bundle_path = localization_translation_bundle_plugin.get_bundle_path()

        # retrieves the bundle type
        bundle_type = localization_translation_bundle_plugin.get_bundle_type()

        # retrieves the bundle locale identifier
        bundle_locale_identifier = localization_translation_bundle_plugin.get_bundle_locale_identifier()

        # retrieves the bundle namespace
        bundle_namespace = localization_translation_bundle_plugin.get_bundle_namespace()

        # creates the translation bundle
        translation_bundle = TranslationBundle(bundle_path, bundle_type, bundle_locale_identifier, bundle_namespace)

        # returns the translation bundle
        return translation_bundle

    def _load_translation_bundle(self, translation_bundle):
        # retrieves the translation bundle type
        translation_bundle_type = translation_bundle.get_bundle_type()

        # retrieves the localization translation bundle handler plugin
        # for the given translation bundle type
        localization_translation_bundle_handler_plugin = self.localization_translation_bundle_handler_name_localization_translation_bundle_handler_plugin_map[translation_bundle_type]

        # handles the translation bundle
        localization_translation_bundle_handler_plugin.handle_bundle(translation_bundle)

        # retrieves the translation bundle locale identifier
        translation_bundle_locale_identifier = translation_bundle.get_bundle_locale_identifier()

        # retrieves the translation bundle namespace
        translation_bundle_namespace = translation_bundle.get_bundle_namespace()

        # retrieves the translation bundle contents
        translation_bundle_contents = translation_bundle.get_bundle_contents()

        # in case the translation bundle locale identifier is not defined in the localization
        # translation bundle locale identifier translation map
        if not translation_bundle_locale_identifier in self.localization_translation_bundle_locale_identifier_translation_map:
            self.localization_translation_bundle_locale_identifier_translation_map[translation_bundle_locale_identifier] = {}

        # retrieves the translation map
        translation_map = self.localization_translation_bundle_locale_identifier_translation_map[translation_bundle_locale_identifier]

        # iterates over the translation bundle contents
        for translation_bundle_contents_key in translation_bundle_contents:
            # creates the translation bundle contents full key
            # prepending the translation bundle namespace
            translation_bundle_contents_full_key = translation_bundle_namespace + "." + translation_bundle_contents_key

            # in case the translation bundle contents full key is not defined in the translation map
            if not translation_bundle_contents_key in translation_map:
                translation_map[translation_bundle_contents_full_key] = {}

            # retrieves the translation bundle contents
            translation_bundle_contents_map = translation_bundle_contents[translation_bundle_contents_key]

            # retrieves the translation item map
            translation_item_map = translation_map[translation_bundle_contents_full_key]

            # iterates over all the all the translation bundle content items
            for translation_bundle_content_item in translation_bundle_contents_map:
                # retrieves the translation bundle content item arguments
                translation_bundle_content_item_arguments = self.options_regex.findall(translation_bundle_content_item)

                # creates the translation bundle content item string
                translation_bundle_content_item_arguments_string = "".join(translation_bundle_content_item_arguments)

                # sets the translation bundle content item in the translation item map
                translation_item_map[translation_bundle_content_item_arguments_string] = translation_bundle_content_item

    def _string_format(self, format_string, *args, **kwargs):
        pass

class TranslationBundle:
    """
    The translation bundle class.
    """

    bundle_path = "none"
    """ The bundle path """

    bundle_type = "none"
    """ The bundle type """

    bundle_locale_identifier = "none"
    """ The bundle locale identifier """

    bundle_namespace = "none"
    """ The bundle namespace """

    bundle_contents = {}
    """ The bundle contents """

    loaded = False
    """ The loaded flag """

    def __init__(self, bundle_path = "none", bundle_type = "none", bundle_locale_identifier = "none", bundle_namespace = "none"):
        self.bundle_path = bundle_path
        self.bundle_type = bundle_type
        self.bundle_locale_identifier = bundle_locale_identifier
        self.bundle_namespace = bundle_namespace

        self.bundle_contents = {}
        self.loaded = False

    def __repr__(self):
        return "<type: %s, locale: %s, namespace: %s>" % (self.bundle_type, self.bundle_locale_identifier, self.bundle_namespace)

    def is_loaded(self):
        """
        Returns if the bundle is loaded.

        @rtype: bool
        @return: If the bundle is loaded.
        """

        return self.loaded

    def get_bundle_path(self):
        """
        Retrieves the bundle path.

        @rtype: String
        @return: The bundle path.
        """

        return self.bundle_path

    def set_bundle_path(self, bundle_path):
        """
        Sets the bundle path.

        @type bundle_path: String
        @param bundle_path: The bundle path.
        """

        self.bundle_path = bundle_path


    def get_bundle_type(self):
        """
        Retrieves the bundle type.

        @rtype: String
        @return: The bundle type.
        """

        return self.bundle_type

    def set_bundle_type(self, bundle_type):
        """
        Sets the bundle type.

        @type bundle_type: String
        @param bundle_type: The bundle type.
        """

        self.bundle_type = bundle_type

    def get_bundle_locale_identifier(self):
        """
        Retrieves the bundle locale identifier.

        @rtype: String
        @return: The bundle locale identifier.
        """

        return self.bundle_locale_identifier

    def set_bundle_locale_identifier(self, bundle_locale_identifier):
        """
        Sets the bundle locale identifier.

        @type bundle_locale_identifier: String
        @param bundle_locale_identifier: The locale identifier.
        """

        self.bundle_locale_identifier = bundle_locale_identifier

    def get_bundle_namespace(self):
        """
        Retrieves the bundle namespace.

        @rtype: String
        @return: The bundle namespace.
        """

        return self.bundle_namespace

    def set_bundle_namespace(self, bundle_namespace):
        """
        Sets the bundle namespace.

        @type bundle_namespace: String
        @param bundle_namespace: The bundle namespace.
        """

        self.bundle_namespace = bundle_namespace

    def get_bundle_contents(self):
        """
        Retrieves the bundle contents.

        @rtype: String
        @return: The bundle contents.
        """

        return self.bundle_contents

    def set_bundle_contents(self, bundle_contents):
        """
        Sets the bundle contents.

        @type bundle_contents: String
        @param bundle_contents: The bundle contents.
        """

        self.bundle_contents = bundle_contents

    def get_loaded(self):
        """
        Retrieves the loaded.

        @rtype: bool
        @return: The loaded.
        """

        return self.loaded

    def set_loaded(self, loaded):
        """
        Sets the loaded.

        @type loaded: bool
        @param loaded: The loaded.
        """

        self.loaded = loaded
