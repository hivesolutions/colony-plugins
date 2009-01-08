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

<div id="searchIndexManagementContentItem">
    <h2 class="mainTitle">Search Index Management</h2>

	<span id="searchIndexListNew" class="button smallIconButton" style="width: 50px;"><img id="buttonIcon" src="pics/add.png"/><span id="buttonTextImage">new</span></span>
    <span id="searchIndexListRefresh" class="button smallIconButton" style="width: 70px;"><img id="buttonIcon" src="pics/arrow_refresh.png"/><span id="buttonTextImage">refresh</span></span>
</div>

<div id="newSearchIndexWindow" class="window" title="New Search Index">
	<div class="window-body">
		<div style="margin-right: 30px">
			<div class="optionBlock">
				<div class="optionTitle">
					<span class="mainTitle" style="text-indent: 4px;">Name:</span>
				</div>
				<div>
					<input type="text" class="box" style="width: 100%;"/>
				</div>
			</div>
			<div class="optionBlock">
				<div class="optionTitle">
					<span class="mainTitle" style="text-indent: 4px;">Options:</span>
				</div>
				<table>
					<tr style="vertical-align: top;">
						<td>
							<div id="propertiesSelector" class="listBox">
								<div class="listBoxElement">Type</div>
								<div class="listBoxElement">Metrics</div>
								<div class="listBoxElement">File Extensions</div>
							</div>
							<div class="listBoxButtons">
								<span id="searchIndexListRefresh" class="simple-button listBoxIconButton" style="width: 70px"><img id="buttonIcon" src="pics/icons/add.png"/><span id="buttonTextImage">Add</span></span>
								<span id="searchIndexListRefresh" class="simple-button listBoxIconButton" style="width: 70px;"><img id="buttonIcon" src="pics/icons/delete.png"/><span id="buttonTextImage">Remove</span></span>
							</div>
						</td>
						<td>
							<div id="propertiesEditor">
								<div id="newSearchIndexWindowPropertiesType">
									<div id="propertiesTypeSelector" class="listBox newSearchIndexWindowPropertiesListBox">
										<div class="listBoxElement">File System</div>
										<div class="listBoxElement">Database</div>
									</div>
								</div>
								<div id="newSearchIndexWindowPropertiesMetrics">
									<div id="propertiesTypeSelector" class="listBox newSearchIndexWindowPropertiesListBox">
										<div class="listBoxElement">Term Frequency</div>
										<div class="listBoxElement">Document Hits</div>
										<div class="listBoxElement">Word Document Frequency</div>
										<div class="listBoxElement">Hit Distance to Top</div>
									</div>
								</div>
								<div id="newSearchIndexWindowPropertiesFileExtensions">
									<div id="propertiesTypeSelector" class="listBox newSearchIndexWindowPropertiesListBox">
										<div class="listBoxElement">Text (*.txt)</div>
										<div class="listBoxElement">Python Source (*.py)</div>
										<div class="listBoxElement">JavaScript Source (*.js)</div>
										<div class="listBoxElement">Java Source (*.java)</div>
										<div class="listBoxElement">XML (*.xml)</div>
									</div>
								</div>
							</div>
						</td>
						<td>
							<div id="propertiesVisualizer">
								<div id="newSearchIndexWindowPropertiesTypeFileSystem">
									<span class="mainTitle">File System</span>
									<p>The File system based profiles...</p>
								</div>
								<div id="newSearchIndexWindowPropertiesTypeDatabase">
									<span class="mainTitle">Database</span>
									<p>The database based file system...</p>
								</div>
							</div>
						</td>
					</tr>
				</table>
			</div>
		</div>
	</div>
	<div class="window-buttons">
		<span id="searchIndexListRefresh" class="button smallIconButton" style="width: 70px;"><img id="buttonIcon" src="pics/accept.png"/><span id="buttonTextImage">Confirm</span></span>
		<span id="searchIndexListRefresh" class="button smallIconButton" style="width: 70px;"><img id="buttonIcon" src="pics/cancel.png"/><span id="buttonTextImage">Cancel</span></span>
	</div>
</div>

