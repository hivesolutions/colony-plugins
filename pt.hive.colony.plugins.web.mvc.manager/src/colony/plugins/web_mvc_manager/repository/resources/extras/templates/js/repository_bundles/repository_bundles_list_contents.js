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

            // retrieves the bundle id and version from the button
            var bundleId = button.attr("data-bundle_id");
            var bundleVersion = button.attr("data-bundle_version");
            var bundleStatus = button.attr("data-bundle_status");

            // starts the install bundle flag
            var installBundle = false;

            // switches over the bundle status
            switch (bundleStatus) {
                case "not_installed" :
                    // sets the install bundle flag
                    installBundle = true;

                    // breaks the switch
                    break;
                case "newer_version" :
                    // sets the install bundle flag
                    installBundle = true;

                    // breaks the switch
                    break;
                case "older_version" :
                    // breaks the switch
                    break;
                case "same_version" :
                    // breaks the switch
                    break;
                case "different_digest" :
                    // sets the install bundle flag
                    installBundle = true;

                    // breaks the switch
                    break;
            }

            // disables the button
            button.button("disable");

            // in case the install bundle flag is not set
            // no need to install the bundle
            if (!installBundle) {
                // creates the uninstall dialog properties
                var uninstallDialogProperties = {
                    title : "Warning",
                    subTitle : "Uninstall existing bundle",
                    message : "This action is going to uninstall bundle <b>"
                            + bundleId
                            + "</b> after that all the dependent bundles are going to be disabled.",
                    buttonMessage : "Do you want to continue ?",
                    successCallbackFunctions : [function() {
                        // resolves the uninstall bundle url
                        var uninstallBundleUrl = jQuery.resolveurl("repositories/uninstall_bundle.json");

                        // processes a remote call for bundle installation
                        jQuery.ajax({
                                    type : "post",
                                    url : uninstallBundleUrl,
                                    data : {
                                        bundle_id : bundleId,
                                        bundle_version : bundleVersion
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

            // resolves the install bundle url
            var installBundleUrl = jQuery.resolveurl("repositories/install_bundle.json");

            // processes a remote call for bundle installation
            jQuery.ajax({
                        type : "post",
                        url : installBundleUrl,
                        data : {
                            bundle_id : bundleId,
                            bundle_version : bundleVersion
                        },
                        complete : function() {
                            button.button("enable");
                        }
                    });
        });

        // bns the body to the bundle install event
        _body.bind("bundle_install", function(event, status) {
                    // retrieves the installed and uninstalled bundles
                    var installedBundles = status["installed"];
                    var uninstalledBundles = status["uninstalled"];

                    // iterates over all the uninstalled bundles
                    jQuery(uninstalledBundles).each(function(index, element) {
                        // retrieves the bundle button reference
                        var bundleButton = jQuery(".button[data-bundle_id="
                                + element + "]");

                        // removes the previous bundle button classes
                        bundleButton.removeClass("button-blue");
                        bundleButton.removeClass("button-gray");

                        // adds the not installed bundle button class
                        bundleButton.addClass("button-green");

                        // updates the bundle button contents
                        bundleButton.html("Install");

                        // sets the new bundle status
                        bundleButton.attr("data-bundle_status", "not_installed");
                    });

                    // iterates over all the installed bundles
                    jQuery(installedBundles).each(function(index, element) {
                        // retrieves the bundle button reference
                        var bundleButton = jQuery(".button[data-bundle_id="
                                + element + "]");

                        // removes the previous bundle button classes
                        bundleButton.removeClass("button-blue");
                        bundleButton.removeClass("button-green");

                        // adds the installed bundle button class
                        bundleButton.addClass("button-gray");

                        // updates the bundle button contents
                        bundleButton.html("Remove");

                        // sets the new bundle status
                        bundleButton.attr("data-bundle_status", "same_version");
                    });
                });
    };

    // retrieves the repository bundles table
    var repositoryBundlesTable = jQuery("#repository-bundles-table");

    // retrieves the table body from the repository bundles table
    var tableBody = jQuery("#table-body", repositoryBundlesTable);

    // registers the extra handlers for the repository bundles table
    // table body
    _registerExtraHandlers(tableBody);

    // binds the repository bundles table to the
    // content change event
    repositoryBundlesTable.bind("content_change",
            function(event, targetElements) {
                _registerExtraHandlers(targetElements);
            });

    // sets the logic loaded data
    jQuery("#contents").data("logic_loaded", true);
});
