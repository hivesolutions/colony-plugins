<?colony
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

__revision__ = "$LastChangedRevision: 516 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2008-11-28 14:30:47 +0000 (Sex, 28 Nov 2008) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """
?>

<?colony
values_map = self.parse_request_attributes(request)

if "searchValue" in values_map:
    search_value = values_map["searchValue"]

# retrieves the search plugin
search_plugin = plugin_manager.get_plugin_by_id("pt.hive.colony.plugins.search")

properties = {"query_evaluator_type" : "query_parser", "search_scorer_function_identifier" : "frequency_location_distance_scorer_function"}
test_results = search_plugin.search_index_by_identifier("pt.hive.colony.plugins.search.test_index_identifier", search_value, properties)

for test_result in test_results:
    print test_result["score"]
    print test_result["document_id"]
?>
