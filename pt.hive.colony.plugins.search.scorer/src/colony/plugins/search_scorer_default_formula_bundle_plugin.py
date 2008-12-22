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

__author__ = "João Magalhães <joamag@hive.pt> & Luís Martinho <lmartinho@hive.pt>"
""" The author(s) of the module """

__version__ = "1.0.0"
""" The version of the module """

__revision__ = "$LastChangedRevision: 684 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2008-12-08 15:16:55 +0000 (Seg, 08 Dez 2008) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import colony.plugins.plugin_system

class SearchScorerDefaultFormulaBundlePlugin(colony.plugins.plugin_system.Plugin):
    """
    The main class for the Search Scorer Default Formula Bundle Plugin.
    """

    id = "pt.hive.colony.plugins.search.scorer.default_formula_bundle"
    name = "Search Scorer Default Formula Bundle Plugin"
    short_name = "Search Scorer Scorer Formula Bundle"
    description = "Plugin that provides a default set of scorer formulas"
    version = "1.0.0"
    author = "Hive Solutions Lda. <development@hive.pt>"
    loading_type = colony.plugins.plugin_system.EAGER_LOADING_TYPE
    platforms = [colony.plugins.plugin_system.CPYTHON_ENVIRONMENT]
    capabilities = ["search_scorer_formula_bundle"]
    capabilities_allowed = []
    dependencies = []
    events_handled = []
    events_registrable = []

    default_scorer_formula_bundle = None

    def load_plugin(self):
        colony.plugins.plugin_system.Plugin.load_plugin(self)
        global search_scorer
        import search_scorer.default_formula_bundle.search_scorer_default_formula_bundle_system
        self.default_scorer_formula_bundle = search_scorer.default_formula_bundle.search_scorer_default_formula_bundle_system.SearchScorerDefaultFormulaBundle(self)

    def end_load_plugin(self):
        colony.plugins.plugin_system.Plugin.end_load_plugin(self)    

    def unload_plugin(self):
        colony.plugins.plugin_system.Plugin.unload_plugin(self)

    def end_unload_plugin(self):
        colony.plugins.plugin_system.Plugin.end_unload_plugin(self)

    def load_allowed(self, plugin, capability):
        colony.plugins.plugin_system.Plugin.load_allowed(self, plugin, capability)

    def unload_allowed(self, plugin, capability):
        colony.plugins.plugin_system.Plugin.unload_allowed(self, plugin, capability)

    def get_formula_types(self):
        return self.default_scorer_formula_bundle.get_formula_types()

    def calculate_value(self, document_id, search_result, search_index, search_scorer_formula_type, properties):
        return self.default_scorer_formula_bundle.calculate_value(document_id, search_result, search_index, search_scorer_formula_type, properties)
