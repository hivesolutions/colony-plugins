// Hive Colony Framework
// Copyright (C) 2008 Hive Solutions Lda.
//
// This file is part of Hive Colony Framework.
//
// Hive Colony Framework is free software: you can redistribute it and/or modify
// it under the terms of the GNU General Public License as published by
// the Free Software Foundation, either version 3 of the License, or
// (at your option) any later version.
//
// Hive Colony Framework is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
// GNU General Public License for more details.
//
// You should have received a copy of the GNU General Public License
// along with Hive Colony Framework. If not, see <http://www.gnu.org/licenses/>.

// __author__    = João Magalhães <joamag@hive.pt> & Luís Martinho <lmartinho@hive.pt>
// __version__   = 1.0.0
// __revision__  = $LastChangedRevision: 7693 $
// __date__      = $LastChangedDate: 2010-03-25 08:40:31 +0000 (qui, 25 Mar 2010) $
// __copyright__ = Copyright (c) 2008 Hive Solutions Lda.
// __license__   = GNU General Public License (GPL), Version 3

/**
 * The plugin loaded window definition map.
 *
 * @type Map
 */
PLUGIN_LOADED_WINDOW = {
    title : "<span class=\"green\">Plugin Loaded</span>",
    subTitle : "",
    timeout : 5000
};

/**
 * The plugin unloaded window definition map.
 *
 * @type Map
 */
PLUGIN_UNLOADED_WINDOW = {
    title : "<span class=\"red\">Plugin Unloaded</span>",
    subTitle : "",
    timeout : 5000
};

/**
 * The plugin installed window definition map.
 *
 * @type Map
 */
PLUGIN_INSTALLED_WINDOW = {
    title : "<span class=\"green\">Plugin Installed</span>",
    subTitle : "",
    timeout : 5000
};

/**
 * The plugin uninstalled window definition map.
 *
 * @type Map
 */
PLUGIN_UNINSTALLED_WINDOW = {
    title : "<span class=\"red\">Plugin Uninstalled</span>",
    subTitle : "",
    timeout : 5000
};

/**
 * The installing new plugin window definition map.
 *
 * @type Map
 */
INSTALLING_NEW_PLUGIN_WINDOW = {
    title : "Installing new plugin",
    subTitle : "The systems is installing the new plugin",
    message : "<div class=\"progress-indicator\"></div>",
    icon : "resources/images/icon/icon-plugin-install.png"
};

/**
 * The installed new plugin window definition map.
 *
 * @type Map
 */
INSTALLED_NEW_PLUGIN_WINDOW = {
    title : "<span class=\"green\">Plugin Installed</span>",
    subTitle : "",
    message : "Plugin installed successfully",
    timeout : 5000
};

/**
 * The problem new plugin window definition map.
 *
 * @type Map
 */
PROBLEM_NEW_PLUGIN_WINDOW = {
    title : "Warning",
    subTitle : "Problem Installing Plugin",
    buttonMessage : "Do you want to continue ?"
};
