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

// the valid status code
VALID_STATUS_CODE = 200

function messageProcessor(data) {
    // parses the data retrieving the json
    var jsonData = jQuery.parseJSON(data);

    // retrieves the message id and contents
    var messageId = jsonData["id"];
    var messageContents = jsonData["contents"];

    if (messageId == "web_mvc_manager/plugin/change_status") {
        // parses the data (json) retrieving the status
        var status = jQuery.parseJSON(messageContents);

        // retrieves the unloaded plugins
        var unloadedPlugins = status["unloaded"];

        // retrieves the notification area contents
        var notificationAreaContents = jQuery("#notification-area-contents");

        // iterates over all the unloaded plugins
        jQuery(unloadedPlugins).each(function(index, element) {
            var switchButtonElement = jQuery("#plugin-table .switch-button[plugin="
                    + element + "]");
            switchButtonElement.removeClass("on");
            switchButtonElement.addClass("off");

            // sets the message in the plugin unloaded window
            PLUGIN_UNLOADED_WINDOW["message"] = element;

            // shows the notification window
            notificationAreaContents.notificationwindow("default",
                    PLUGIN_UNLOADED_WINDOW);
        });

        // retrieves the loaded plugins
        var loadedPlugins = status["loaded"];

        // iterates over all the loaded plugins
        jQuery(loadedPlugins).each(function(index, element) {
            var switchButtonElement = jQuery("#plugin-table .switch-button[plugin="
                    + element + "]");
            switchButtonElement.removeClass("off");
            switchButtonElement.addClass("on");

            // sets the message in the plugin loaded window
            PLUGIN_LOADED_WINDOW["message"] = element;

            // shows the notification window
            notificationAreaContents.notificationwindow("default",
                    PLUGIN_LOADED_WINDOW);
        });
    } else if (messageId == "web_mvc_manager/plugin/install") {
        // parses the data (json) retrieving the status
        var status = jQuery.parseJSON(messageContents);

        // retrieves the uninstalled plugins
        var uninstalledPlugins = status["uninstalled"];

        // retrieves the notification area contents
        var notificationAreaContents = jQuery("#notification-area-contents");

        // iterates over all the uninstalled plugins
        jQuery(uninstalledPlugins).each(function(index, element) {
            // sets the message in the plugin uninstalled window
            PLUGIN_UNINSTALLED_WINDOW["message"] = element;

            // shows the notification window
            notificationAreaContents.notificationwindow("default",
                    PLUGIN_UNINSTALLED_WINDOW);
        });

        // retrieves the installed plugins
        var installedPlugins = status["installed"];

        // iterates over all the installed plugins
        jQuery(installedPlugins).each(function(index, element) {
            // sets the message in the plugin installed window
            PLUGIN_INSTALLED_WINDOW["message"] = element;

            // shows the notification window
            notificationAreaContents.notificationwindow("default",
                    PLUGIN_INSTALLED_WINDOW);
        });
    } else if (messageId == "web_mvc_manager/header/reload") {
        // reloads the header
        jQuery("body").page("reloadHeader");
    } else if (messageId == "web_mvc_manager/side_panel/reload") {
        // retrieves the current active menu as the target menu
        var targetMenu = jQuery("#main-container").data("menu");

        // reloads the metadata in the main container
        jQuery("#main-container").maincontainer("loadMetadata", {
                    forceReload : true,
                    target : targetMenu
                });
    }
}

jQuery(document).ready(function() {
    // register the communication for the communig+cation
    // url given
    jQuery("body").communication("default", {
                url : "communication",
                timeout : 500,
                dataCallbackFunctions : [messageProcessor]
            });

    jQuery("#account-description").click(function() {
                if (!jQuery("#account-float-panel").is(":visible")) {
                    jQuery("#account-float-panel").fadeIn(200, function() {
                                jQuery("#account-float-panel").click(
                                        function(event) {
                                            event.stopPropagation();

                                        });
                                jQuery(document).click(function(event) {
                                            jQuery("#account-float-panel").hide();
                                            jQuery(document).unbind("click");
                                        });
                            });
                }
            });

    // loads the file drop
    fileDropLoad();

    // loads the file install
    fileInstallLoad();

    // loads the contents
    contentsLoad();
});

function fileDropLoad() {
    // retrieves the body element
    var _body = jQuery("body");

    // register the file drop in the overlay
    _body.filedrop()

    // registers the handler for the file drop event
    // in the overlay
    _body.bind("file_drop", function(event, files) {
                // retrievs the files element
                var _files = jQuery(files);

                // iterates over the files
                _files.each(function(index, element) {
                            // installs the package file
                            _body.installpackagefile({
                                        file : element
                                    });
                        });
            });
}

function fileInstallLoad() {
    // retrieves the body element
    var _body = jQuery("body");

    _body.bind("file_loading", function(event) {
        // creates a message windows with for the progress of
        // the installation
        _body.messagewindow("default", INSTALLING_NEW_PLUGIN_WINDOW);

        // starts the progress indicator
        jQuery(".message-message .progress-indicator", "body").progressindicator();
    });

    _body.bind("file_progress_change", function(event, percentage) {
        // sets the progress indicator percentage
        jQuery(".message-message .progress-indicator", "body").progressindicator(
                "change", {
                    percentage : percentage
                });
    });

    _body.bind("file_loaded",
            function(event, responseText, responseStatus, xmlHttpRequest) {
                // sets the progress indicator percentage
                jQuery(".message-message .progress-indicator", "body").progressindicator(
                        "change", {
                            percentage : 100
                        });

                // closes the message window
                _body.messagewindow("close");

                // in case the response status is valid
                if (responseStatus == VALID_STATUS_CODE) {
                    jQuery("#notification-area-contents").notificationwindow(
                            "default", INSTALLED_NEW_PLUGIN_WINDOW);
                }
                // otherwise it must be an invalid status
                else {
                    // parses the response text to get the response
                    var response = jQuery.parseJSON(responseText);

                    // retrieves the exception from the response
                    var exception = response["exception"];

                    // retrieves the exception message
                    var exceptionMessage = exception["message"];

                    // creates the complete error message
                    var errorMessage = "There was a problem installing plugin: "
                            + exceptionMessage;

                    // sets the error message in the problem new plugi window
                    PROBLEM_NEW_PLUGIN_WINDOW["message"] = errorMessage;

                    // shows a dialob window in the body
                    _body.dialogwindow("default", PROBLEM_NEW_PLUGIN_WINDOW);
                }
            });
}

/**
 * Loads the initial contents, modifing the internal DOM structure if necessary.
 */
function contentsLoad() {
    // sets the page in the body and configures it
    // to allow history load for the given history handler
    jQuery("body").page("default", {
                historyLoad : true,
                historyHandler : changeContents
            });

    // sets the main container
    jQuery("#main-container").maincontainer();

    // reloads the contents page
    jQuery("#main-container").maincontainer("reload");
}

/**
 * Changes the contents of the main container.
 *
 * @param {String}
 *            target The target to be used in the update of the main container.
 */
function changeContents(target) {
    // changes the menu to the new contents from the target
    jQuery("#main-container").maincontainer("changeMenu", {
                target : target
            });

    // changes the main container to the new contents from the target
    jQuery("#main-container").maincontainer("change", {
                target : target
            });
}

/**
 * Retrieves the base path based on a component placed in the dom.
 *
 * @return {String} The base path.
 */
function getBasePath() {
    // returns the base path, based on the
    // component in the dom
    return jQuery("#environment-variables > #base-path").html();
}

/**
 * Retrieves the ajax submit value based on a component placed in the dom.
 *
 * @return {String} The ajax submit.
 */
function getAjaxSubmit() {
    // returns the ajax submit value, based on the
    // component in the dom
    return jQuery("#environment-variables > #ajax-submit").html();
}
