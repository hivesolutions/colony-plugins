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
    // retrieves the body
    var _body = jQuery("body");

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
            var pluginId = button.attr("data-plugin_id");
            var pluginVersion = button.attr("data-plugin_version");
            var pluginStatus = button.attr("data-plugin_status");

            // starts the install plugin flag
            var instalPlugin = false;

            // switches over the plugin status
            switch (pluginStatus) {
                case "not_installed" :
                    // sets the install plugin flag
                    instalPlugin = true;

                    // breaks the switch
                    break;
                case "newer_version" :
                    // sets the install plugin flag
                    instalPlugin = true;

                    // breaks the switch
                    break;
                case "older_version" :
                    // breaks the switch
                    break;
                case "same_version" :
                    // breaks the switch
                    break;
                case "different_digest" :
                    // sets the install plugin flag
                    instalPlugin = true;

                    // breaks the switch
                    break;
            }

            // disables the button
            button.button("disable");

            // in case the install plugin flag is not set
            // no need to install the plugin
            if (!instalPlugin) {
                // creates the uninstall dialog properties
                var uninstallDialogProperties = {
                    title : "Warning",
                    subTitle : "Uninstall existing plugin",
                    message : "This action is going to uninstall plugin <b>"
                            + pluginId
                            + "</b> after that all the dependent plugins are going to be disabled.",
                    buttonMessage : "Do you want to continue ?",
                    successCallbackFunctions : [function() {
                        // resolves the uninstall plugin url
                        var uninstallPluginUrl = jQuery.resolveurl("repositories/uninstall_plugin.json");

                        // processes a remote call for plugin installation
                        jQuery.ajax({
                                    type : "post",
                                    url : uninstallPluginUrl,
                                    data : {
                                        plugin_id : pluginId,
                                        plugin_version : pluginVersion
                                    },
                                    complete : function() {
                                        button.button("enable");
                                    }
                                });
                    }],
                    errorCallbackFunctions : [function() {
                                button.button("enable");
                            }]
                };

                // shows a dialog window in the body
                _body.dialogwindow("default", uninstallDialogProperties);

                // returns immediately
                return;
            }

            // resolves the install plugin url
            var installPluginUrl = jQuery.resolveurl("repositories/install_plugin.json");

            // processes a remote call for plugin installation
            jQuery.ajax({
                        type : "post",
                        url : installPluginUrl,
                        data : {
                            plugin_id : pluginId,
                            plugin_version : pluginVersion
                        },
                        complete : function() {
                            button.button("enable");
                        }
                    });
        });

        // bns the body to the plugin install event
        _body.bind("plugin_install", function(event, status) {
                    // retrieves the installed and uninstalled plugins
                    var installedPlugins = status["installed"];
                    var uninstalledPlugins = status["uninstalled"];

                    // iterates over all the uninstalled plugins
                    jQuery(uninstalledPlugins).each(function(index, element) {
                        // retrieves the plugin button reference
                        var pluginButton = jQuery(".button[data-plugin_id="
                                + element + "]");

                        // removes the previous plugin button classes
                        pluginButton.removeClass("button-blue");
                        pluginButton.removeClass("button-gray");

                        // adds the not installed plugin button class
                        pluginButton.addClass("button-green");

                        // updates the plugin button contents
                        pluginButton.html("Install");

                        // sets the new plugin status
                        pluginButton.attr("data-plugin_status", "not_installed");
                    });

                    // iterates over all the installed plugins
                    jQuery(installedPlugins).each(function(index, element) {
                        // retrieves the plugin button reference
                        var pluginButton = jQuery(".button[data-plugin_id="
                                + element + "]");

                        // removes the previous plugin button classes
                        pluginButton.removeClass("button-blue");
                        pluginButton.removeClass("button-green");

                        // adds the installed plugin button class
                        pluginButton.addClass("button-gray");

                        // updates the plugin button contents
                        pluginButton.html("Remove");

                        // sets the new plugin status
                        pluginButton.attr("data-plugin_status", "same_version");
                    });
                });
    };

    // retrieves the repository plugins plugin table
    var repositoryPluginsTable = jQuery("#repository-plugins-table");

    // retrieves the table body from the repository plugins table
    var tableBody = jQuery("#table-body", repositoryPluginsTable);

    // registers the extra handlers for the repository plugins table
    // table body
    _registerExtraHandlers(tableBody);

    // binds the repository plugins table to the
    // content change event
    repositoryPluginsTable.bind("content_change",
            function(event, targetElements) {
                _registerExtraHandlers(targetElements);
            });

    // sets the logic loaded data
    jQuery("#contents").data("logic_loaded", true);
});
