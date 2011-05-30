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

// __author__    = João Magalhães <joamag@hive.pt>
// __version__   = 1.0.0
// __revision__  = $LastChangedRevision: 7693 $
// __date__      = $LastChangedDate: 2010-03-25 08:40:31 +0000 (qui, 25 Mar 2010) $
// __copyright__ = Copyright (c) 2008 Hive Solutions Lda.
// __license__   = GNU General Public License (GPL), Version 3

jQuery(document).ready(function() {
    // sets the logic loaded data
    var logicLoaded = jQuery("#contents").data("logic_loaded");

    // in case the logic is already loaded
    if (logicLoaded) {
        // returns immediately
        return;
    }

    var _registerExtraHandlers = function(targetElement) {
        // retrieves the buttons from the target element
        var buttons = jQuery(".button", targetElement)

        // creates the buttons
        buttons.button();

        // registers the callback for the click event
        buttons.click(function(event, element, status) {
                    // retrieves the button
                    var button = jQuery(this);

                    // retrieves the plugin id and version from the button
                    var pluginId = button.attr("plugin_id");
                    var pluginVersion = button.attr("plugin_version");

                    jQuery.ajax({
                                type : "post",
                                url : "repositories/install_plugin.json",
                                data : {
                                    plugin_id : pluginId,
                                    plugin_version : pluginVersion
                                }
                            });
                });
    };

    // retrieves the repository plugins plugin table
    var repositoryPluginsTable = jQuery("#repository-plugins-table");

    // registers the extra handlers for the repository plugins table
    _registerExtraHandlers(repositoryPluginsTable);

    repositoryPluginsTable.bind("content_change",
            function(event, targetElements) {
                _registerExtraHandlers(targetElements);
            });

    // sets the logic loaded data
    jQuery("#contents").data("logic_loaded", true);
});
