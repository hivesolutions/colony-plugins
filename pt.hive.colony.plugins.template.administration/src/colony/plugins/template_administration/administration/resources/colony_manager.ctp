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

<!DOCTYPE html 
    PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" 
    "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd"> 
<html xmlns="http://www.w3.org/1999/xhtml" lang="en" xml:lang="en"> 

<!-- the head of the html -->
<head> 
    <title><?colony print "Hive Colony Manager" ?></title>
    <?colony self.import_js_library("jquery") ?>
    <?colony self.import_js_library("jquery.ui.all") ?>
    <?colony self.import_js_library("jquery.tablesorter") ?>
    <?colony self.import_js_library("jquery.contextmenu") ?>
    <?colony self.import_js_library("jquery.jgrowl") ?>
	<script type="text/javascript" src="jquery_plugins/js/colony_base_components.js"></script>
	<script type="text/javascript" src="jquery_plugins/js/colony_base_logic.js"></script>
    <script type="text/javascript" src="js/colony_manager.js"></script>

    <?colony
# retrieves the template administrator plugin
template_administrator_plugin = plugin_manager.get_plugin_by_id("pt.hive.colony.plugins.template.administration")

# retrieves the js files
js_files = template_administrator_plugin.get_js_files()

# iterates over all the js files
for js_file in js_files:
	print "<script type=\"text/javascript\" src=\""
	print js_file
	print "\"></script>"
	?>

    <link rel="stylesheet" href="css/jquery.contextmenu.css" type="text/css">
    <link rel="stylesheet" href="css/jquery.jgrowl.css" type="text/css">
    <link rel="stylesheet" href="jquery_themes/humanity/ui.theme.css" type="text/css" media="screen" title="Themeroller (Default)">
    <link rel="stylesheet" href="jquery_plugins/css/colony_base_components.css" type="text/css">
    <link rel="stylesheet" href="css/colony_manager.css" type="text/css">

    <?colony
# retrieves the template administrator plugin
template_administrator_plugin = plugin_manager.get_plugin_by_id("pt.hive.colony.plugins.template.administration")

# retrieves the css files
css_files = template_administrator_plugin.get_css_files()

# iterates over all the css files
for css_file in css_files:
	print "<link rel=\"stylesheet\" href=\""
	print css_file
	print "\" type=\"text/css\""
	?>

</head>

<body>

<span id="testBox"></span>

<div id="testDiv" style="width:200px;"></div>

<div id="jgrowlNotifier"></div>

<div id="tooltip">
    <div id="tooltipTitle">
    </div>
    <div id="tooltipBody">
    </div>
</div>

<div id="settingsWindow" class="window" title="Settings">
	<div class="window-body">
		<table>
			<tr>
				<td>
					<table class="settingsTableCell">
						<tr><td><img src="pics/icons/48x48/computer.png"/></td></tr>
						<tr><td>General</td></tr>
					</table>
				</td>
				<td>
					<table class="settingsTableCell">
						<tr><td><img src="pics/icons/48x48/search.png"/></td></tr>
						<tr><td>Search</td></tr>
					</table>
				</td>
				<td>
					<table class="settingsTableCell">
						<tr><td><img src="pics/icons/48x48/mail.png"/></td></tr>
						<tr><td>Email</td></tr>
					</table>
				</td>
				<td>
				<table class="settingsTableCell">
						<tr><td><img src="pics/icons/48x48/personal_security.png"/></td></tr>
						<tr><td>Personal Security</td></tr>
					</table>
				</td>
			</tr>
		</table>
	</div>
</div>

<div id="loginFormContainer">
    <div id="loginFormShaker">
        <div id="loginForm">
            <fieldset>
                <label for="Login" class="mainTitle">Login:</label>
                <input id="login" type="text" />
                <label for="Password" class="mainTitle">Password:</label>
                <input id="password" type="password" />
                <label for="Login Type" class="mainTitle">Login Type:</label>
                <input id="login_type" type="text" />
                <table>
                <tr>
                    <td><input id="submitLogin" class="mainTitle" value="Login" type="submit" name="submit" onclick="tryLogin($('#login').attr('value'), $('#password').attr('value'))" /></td>
                    <td><span id="loginMessage" class="mainTitle">Trying to login...</span></td>
                </tr>
                </table>
            </fieldset>
        </div>
        <div id="loginLink"></div>
    </div>
</div>

<div id="mainDiv">
    <table id="mainTable">
        <tr>
            <div style="float: right;">
                <p id="topMenuBar" class="mainTitle">username: tobias | <a id="settingsButton" class="simpleButton">Settings</a> | Help | About | Sign Out</p>
            </div>
            <div>
                <p class="mainTitle">Manager | Forum | Development</p>
            </div>
        </tr>
        <tr>
            <td>
                <img src="./pics/hive_logo_development.png">
            </td>
            <td class="mainPanelCell3">
                <div id="mainStatusBar">
                    <!-- The search Form -->
                    <div id="searchForm">
                        <table align="right">
                            <tr>
                                <td>
                                    <div style="text-align: right;">
                                        <span class="mainTitle" style="text-align: right;">
                                            <img id="bugIcon" src="./pics/icons/bug.png"/>
                                            <img src="pics/icons/brick.png"/>
                                            <img src="pics/icons/building.png"/>
                                            <img id="emailIcon" src="./pics/icons/email.png"/>
                                        </span>
                                    </div>
                                </td>
                            </tr>
                            <tr>
                                <td><input id="searchInput" type="text" /></td>
                            </tr>
                        </table>
                    </div>
                </div>
            </td>
        </tr>
        <tr>
            <td class="mainPanelCell">
                <div class="lateralMenu">
                    <table id="menuTable">
                        <?colony
# retrieves the template administrator plugin
template_administrator_plugin = plugin_manager.get_plugin_by_id("pt.hive.colony.plugins.template.administration")

# retrieves the menu items
menu_items = template_administrator_plugin.get_menu_items()

# iterates over all the menu items
for menu_item in menu_items:
	print "<tr>"
	self.interpret(menu_item)
	print "</tr>"
						?>
                    </table>
                </div>
            </td>
            <td class="mainPanelCell2">
                <div id="mainTabPanel">
                    <ul>
                    	<li><a href="#homeContentItem"><span>Home <img src='pics/icons/bullet_green.png' style='border:0px;'/></span></a></li>
                    </ul>
                    <div id="homeContentItem">
                   	home
                    </div>
                    <div id="extraContentItems" class="hidable">
               	        <?colony
# retrieves the template administrator plugin
template_administrator_plugin = plugin_manager.get_plugin_by_id("pt.hive.colony.plugins.template.administration")

# retrieves the content items
content_items = template_administrator_plugin.get_content_items()

# iterates over all the content items
for content_item in content_items:
	self.interpret(content_item)
					    ?>
					</div>
                </div>
            </td>
        </tr>
    </table>
    <div class="copyright">
        <span class="mainTitle">Copyright 08 Hive Solutions Lda.</span>
        <div id="clickNotification">Notify</div>
    </div>
</div>

<ul id="pluginContextMenu" class="contextMenu">
    <li><a class="textType" href="#unload">Unload</a></li>
    <li><a class="textType" href="#load">Load</a></li>
    <li><a class="textType" href="#remove">Remove</a></li>
</ul>

</body>
