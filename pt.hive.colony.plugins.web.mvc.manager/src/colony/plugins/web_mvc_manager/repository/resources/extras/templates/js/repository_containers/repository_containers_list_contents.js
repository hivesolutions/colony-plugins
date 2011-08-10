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

            // retrieves the container id and version from the button
            var containerId = button.attr("data-container_id");
            var containerVersion = button.attr("data-container_version");
            var containerStatus = button.attr("data-container_status");

            // starts the install container flag
            var installContainer = false;

            // switches over the container status
            switch (containerStatus) {
                case "not_installed" :
                    // sets the install container flag
                    installContainer = true;

                    // breaks the switch
                    break;
                case "newer_version" :
                    // sets the install container flag
                    installContainer = true;

                    // breaks the switch
                    break;
                case "older_version" :
                    // breaks the switch
                    break;
                case "same_version" :
                    // breaks the switch
                    break;
                case "different_digest" :
                    // sets the install container flag
                    installContainer = true;

                    // breaks the switch
                    break;
            }

            // disables the button
            button.button("disable");

            // in case the install container flag is not set
            // no need to install the container
            if (!installContainer) {
                // creates the uninstall dialog properties
                var uninstallDialogProperties = {
                    title : "Warning",
                    subTitle : "Uninstall existing container",
                    message : "This action is going to uninstall container <b>"
                            + containerId
                            + "</b> after that all the dependent containers are going to be disabled.",
                    buttonMessage : "Do you want to continue ?",
                    successCallbackFunctions : [function() {
                        // resolves the uninstall container url
                        var uninstallContainerUrl = jQuery.resolveurl("repositories/uninstall_container.json");

                        // processes a remote call for container installation
                        jQuery.ajax({
                                    type : "post",
                                    url : uninstallContainerUrl,
                                    data : {
                                        container_id : containerId,
                                        container_version : containerVersion
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

            // resolves the install container url
            var installContainerUrl = jQuery.resolveurl("repositories/install_container.json");

            // processes a remote call for container installation
            jQuery.ajax({
                        type : "post",
                        url : installContainerUrl,
                        data : {
                            container_id : containerId,
                            container_version : containerVersion
                        },
                        complete : function() {
                            button.button("enable");
                        }
                    });
        });

        // bns the body to the container install event
        _body.bind("container_install", function(event, status) {
                    // retrieves the installed and uninstalled containers
                    var installedContainers = status["installed"];
                    var uninstalledContainers = status["uninstalled"];

                    // iterates over all the uninstalled containers
                    jQuery(uninstalledcontainers).each(
                            function(index, element) {
                                // retrieves the container button reference
                                var containerButton = jQuery(".button[data-container_id="
                                        + element + "]");

                                // removes the previous container button classes
                                containerButton.removeClass("button-blue");
                                containerButton.removeClass("button-gray");

                                // adds the not installed container button class
                                containerButton.addClass("button-green");

                                // updates the container button contents
                                containerButton.html("Install");

                                // sets the new container status
                                containerButton.attr("data-container_status",
                                        "not_installed");
                            });

                    // iterates over all the installed containers
                    jQuery(installedcontainers).each(function(index, element) {
                        // retrieves the container button reference
                        var containerButton = jQuery(".button[data-container_id="
                                + element + "]");

                        // removes the previous container button classes
                        containerButton.removeClass("button-blue");
                        containerButton.removeClass("button-green");

                        // adds the installed container button class
                        containerButton.addClass("button-gray");

                        // updates the container button contents
                        containerButton.html("Remove");

                        // sets the new container status
                        containerButton.attr("data-container_status",
                                "same_version");
                    });
                });
    };

    // retrieves the repository containers table
    var repositoryContainersTable = jQuery("#repository-containers-table");

    // retrieves the table body from the repository containers table
    var tableBody = jQuery("#table-body", repositoryContainersTable);

    // registers the extra handlers for the repository containers table
    // table body
    _registerExtraHandlers(tableBody);

    // binds the repository containers table to the
    // content change event
    repositoryContainersTable.bind("content_change",
            function(event, targetElements) {
                _registerExtraHandlers(targetElements);
            });

    // sets the logic loaded data
    jQuery("#contents").data("logic_loaded", true);
});
