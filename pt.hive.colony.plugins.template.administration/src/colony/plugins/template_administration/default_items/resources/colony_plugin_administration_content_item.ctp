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

<div id="colonyPluginAdministrationContentItem">
    <h2 class="mainTitle">The plugins list</h2>
    <p>Here you can do some plugin manager management: </p>
    <?colony
# retrieves all the plugins
all_plugins = plugin_manager.get_all_plugins()
print "<table id=pluginManagement class=\"pluginsTable\">"
print "<thead> <tr> <th class=\"mainTitle tableHeader\">PLUGIN ID</th> <th class=\"mainTitle tableHeader\">NAME</th> <th class=\"mainTitle tableHeader\">AUTHOR</th>  <th class=\"mainTitle tableHeader\">STATUS</th> </tr> </thead>"
print "<tbody>"
for plugin in all_plugins:
    print "<tr>"
    print "<td class=\"mainTitle\" onclick=\"$('#details-" + self.escape_dots(plugin.id) + "').slideToggle('normal')\" class=\"itemValue\">" + plugin.id + "</td>"
    print "<td class=\"itemValue\">" + plugin.name + "</td>"
    print "<td class=\"itemValue\">" + plugin.author + "</td>"
    if plugin.is_loaded():
        print "<td style=\"border: 1px dashed #888897;\" id=\"" + self.escape_dots(plugin.id) + "\" class=\"loaded\" onclick=\"loadPlugin('" + plugin.id + "')\">LOADED</td>"
    else:
        print "<td style=\"border: 1px dashed #888897;\" id=\"" + self.escape_dots(plugin.id) + "\" class=\"unloaded\" onclick=\"loadPlugin('" + plugin.id + "')\">UNLOADED</td>"
    print "</tr>"
    print "<tr class=\"hiddenItemValue\">"
    print "<td colspan=4>"
    print "<div id=\"details-" + self.escape_dots(plugin.id) + "\" class=\"hiddenPluginDetails hidable\">"
    print "<table>"
    print "<tr><td class=\"pluginDetailsIdColumn\"><b>ID</b></td><td>" + plugin.id + "</td></tr>"
    print "<tr><td class=\"pluginDetailsIdColumn\"><b>SHORT NAME</b></td><td>" + plugin.short_name + "</td></tr>"
    print "<tr><td class=\"pluginDetailsIdColumn\"><b>NAME</b></td><td>" + plugin.name + "</td></tr>"
    print "<tr><td class=\"pluginDetailsIdColumn\"><b>DESCRIPTION</b></td><td>" + plugin.description + "</td></tr>"
    print "<tr><td class=\"pluginDetailsIdColumn\"><b>VERSION</b></td><td>" + plugin.version + "</td></tr>"
    print "<tr><td class=\"pluginDetailsIdColumn\"><b>AUTHOR</b></td><td>" + plugin.author + "</td></tr>"
    print "<tr><td class=\"pluginDetailsIdColumn\"><b>LOADING TYPE</b></td><td>" + str(plugin.loading_type) + "</td></tr>"
    print "<tr><td class=\"pluginDetailsIdColumn\"><b>PLATFORMS</b></td><td>" + str(plugin.platforms) + "</td></tr>"
    print "<tr><td class=\"pluginDetailsIdColumn\"><b>CAPABILITIES</b></td><td>" + str(plugin.capabilities) + "</td></tr>"
    print "<tr><td class=\"pluginDetailsIdColumn\"><b>CAPABILITIES ALLOWED</b></td><td>" + str(plugin.capabilities_allowed) + "</td></tr>"
    print "<tr><td class=\"pluginDetailsIdColumn\"><b>DEPENDENCIES</b></td><td>" + str(plugin.dependencies) + "</td></tr>"
    print "</table>"
    print "</div>"
    print "</td>"
    print "</tr>"
print "</tbody>"
print "</table>"
    ?>
</div>
