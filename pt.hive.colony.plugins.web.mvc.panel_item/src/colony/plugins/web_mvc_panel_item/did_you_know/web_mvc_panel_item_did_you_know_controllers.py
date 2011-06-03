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

__author__ = "João Magalhães <joamag@hive.pt> & Tiago Silva <tsilva@hive.pt>"
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

import random

WEB_MVC_PANEL_ITEM_DID_YOU_KNOW_RESOURCES_PATH = "web_mvc_panel_item/did_you_know/resources"
""" The web panel item did you know resources path """

RANDOM_MESSAGE = False
""" The random message flag """

DID_YOU_KNOW_LIST = (
    "Chuck Norris once shot down a German fighter plane with his finger, by yelling, \"Bang!\"",
    "A Handicapped parking sign does not signify that this spot is for handicapped people. It is actually in fact a warning, that the spot belongs to Chuck Norris and that you will be handicapped if you park there.",
    "Everybody loves Raymond. Except Chuck Norris.",
    "Chuck Norris once round-house kicked a salesman. Over the phone."
)
""" The list of did you know sentences """

class MainController:
    """
    The web mvc panel item did you know main controller.
    """

    web_mvc_panel_item_did_you_know_plugin = None
    """ The web mvc panel item did you know plugin """

    web_mvc_panel_item_did_you_know = None
    """ The web mvc panel item did you know """

    def __init__(self, web_mvc_panel_item_did_you_know_plugin, web_mvc_panel_item_did_you_know):
        """
        Constructor of the class.

        @type web_mvc_panel_item_did_you_know_plugin: WebMvcPanelItemDidYouKnowPlugin
        @param web_mvc_panel_item_did_you_know_plugin: The web mvc panel item did you know plugin.
        @type web_mvc_panel_item_did_you_know: WebMvcPanelItemDidYouKnow
        @param web_mvc_panel_item_did_you_know: The web mvc panel item did you know.
        """

        self.web_mvc_panel_item_did_you_know_plugin = web_mvc_panel_item_did_you_know_plugin
        self.web_mvc_panel_item_did_you_know = web_mvc_panel_item_did_you_know

    def start(self):
        """
        Method called upon structure initialization.
        """

        # sets the relative resources path
        self.set_relative_resources_path(WEB_MVC_PANEL_ITEM_DID_YOU_KNOW_RESOURCES_PATH)

    def get_panel_item(self):
        # retrieves the template file
        template_file = self.retrieve_template_file("panel_item_did_you_know.html.tpl")

        # assigns the did you know variables
        self.__assign_did_you_know_variables(template_file)

        # processes the template file
        processed_template_file = self.process_template_file(template_file)

        # returns the processed template file
        return processed_template_file

    def __assign_did_you_know_variables(self, template_file):
        # in case random message value is set
        if RANDOM_MESSAGE:
            # sets the value as a random value
            value = self.__get_random_value()
        else:
            # sets the value as zero the (first one)
            value = 0

        # retrieves the random did you know sentence
        did_you_know = DID_YOU_KNOW_LIST[value]

        # assigns the did you know to the template
        template_file.assign("did_you_know", did_you_know)

    def __get_random_value(self):
        # retrieves the did you know list length
        did_you_know_list_length = len(DID_YOU_KNOW_LIST)

        # generates the random value
        random_value = random.randint(0, did_you_know_list_length - 1)

        return random_value
