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

        // iterates over all the unloaded plugins
        jQuery(unloadedPlugins).each(function(index, element) {
            var switchButtonElement = jQuery("#plugin-table .switch-button[plugin="
                    + element + "]");
            switchButtonElement.removeClass("on");
            switchButtonElement.addClass("off");

            jQuery("#notification-area-contents").notificationwindow("default",
                    {
                        "title" : "<span class=\"red\">Plugin Unloaded</span>",
                        "subTitle" : "",
                        "message" : element,
                        "timeout" : 5000
                    });
        });

        // retrieves the loaded plugins
        var loadedPlugins = status["loaded"];

        // iterates over all the loaded plugins
        jQuery(loadedPlugins).each(function(index, element) {
            var switchButtonElement = jQuery("#plugin-table .switch-button[plugin="
                    + element + "]");
            switchButtonElement.removeClass("off");
            switchButtonElement.addClass("on");

            jQuery("#notification-area-contents").notificationwindow("default",
                    {
                        "title" : "<span class=\"green\">Plugin Loaded</span>",
                        "subTitle" : "",
                        "message" : element,
                        "timeout" : 5000
                    });
        });
    } else if (messageId == "web_mvc_manager/plugin/install") {
        // parses the data (json) retrieving the status
        var status = jQuery.parseJSON(messageContents);

        // retrieves the uninstalled plugins
        var uninstalledPlugins = status["uninstalled"];

        // iterates over all the uninstalled plugins
        jQuery(uninstalledPlugins).each(function(index, element) {
            jQuery("#notification-area-contents").notificationwindow("default",
                    {
                        "title" : "<span class=\"red\">Plugin Uninstalled</span>",
                        "subTitle" : "",
                        "message" : element,
                        "timeout" : 5000
                    });
        });

        // retrieves the installed plugins
        var installedPlugins = status["installed"];

        // iterates over all the installed plugins
        jQuery(installedPlugins).each(function(index, element) {
            jQuery("#notification-area-contents").notificationwindow("default",
                    {
                        "title" : "<span class=\"green\">Plugin Installed</span>",
                        "subTitle" : "",
                        "message" : element,
                        "timeout" : 5000
                    });
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
    jQuery("body").communication("default", {
                url : "communication",
                timeout : 500,
                dataCallbackFunctions : [messageProcessor]
            });

    jQuery("body").bind("dragenter", function(event) {
                // stops the event propagation and prevents
                // the default event operation
                event.stopPropagation();
                event.preventDefault();

                jQuery("body").messagewindow("default", {
                            "title" : "Install new plugin",
                            "subTitle" : "",
                            "message" : "Drop the file to install the new plugin.",
                            "icon" : "resources/images/icon/icon-plugin-install.png"
                        });
            });

    jQuery("#overlay").bind("dragleave", function(event) {
                // stops the event propagation and prevents
                // the default event operation
                event.stopPropagation();
                event.preventDefault();

                // closes the message window
                jQuery("body").messagewindow("close");
            });

    jQuery("#overlay").bind("drop", function(event) {
        // stops the event propagation and prevents
        // the default event operation
        event.stopPropagation();
        event.preventDefault();

        // closes the message window
        jQuery("body").messagewindow("close");

        // retrieves the data tranfer and the files
        // rom the original event
        var dataTransfer = event.originalEvent.dataTransfer;
        var files = dataTransfer.files;

        // retrieves the first file
        var file = files[0];

        // retrieves the file name
        var fileName = file.name;

        // splits the file name to retrieve
        // the file extension
        var fileNameSplit = fileName.split(".");
        var fileNameSplitLength = fileNameSplit.length;
        var fileExtension = fileNameSplit[fileNameSplitLength - 1];

        // creates a new file reader, to read
        // the file contents (ad binary data)
        var fileReader = new FileReader();
        fileReader.readAsBinaryString(file);

        fileReader.onload = function() {
            // retrieves the file contents from
            // the file reader
            var fileContents = fileReader.result;

            // encodes the file contents into base64
            var fileContentsBase64 = Base64.encode(fileContents);

            // creates a new cml http request
            var xmlHttpRequest = new XMLHttpRequest();

            // retrieves the upload element
            var uploadElement = jQuery(xmlHttpRequest.upload);

            uploadElement.bind("progress", function(event) {
                if (event.lengthComputable) {
                    // calculates the percentage of loading
                    var percentage = Math.round((event.loaded * 100)
                            / event.total);

                    // sets the progress indicator percentage
                    jQuery(".message-message .progress-indicator", "body").progressindicator(
                            "change", {
                                percentage : percentage
                            });
                }
            });

            uploadElement.bind("load", function(event) {
                // sets the progress indicator percentage
                jQuery(".message-message .progress-indicator", "body").progressindicator(
                        "change", {
                            percentage : 100
                        });

                // sets a timeout to close the message window
                setTimeout(function() {
                    // closes the message window
                    jQuery("body").messagewindow("close");

                    if (xmlHttpRequest.status == 200) {
                        jQuery("#notification-area-contents").notificationwindow(
                                "default", {
                                    "title" : "<span class=\"green\">Plugin Installed</span>",
                                    "subTitle" : "",
                                    "message" : "Plugin installed successfully",
                                    "timeout" : 5000
                                });
                    } else {
                        // parses the response text to get the response
                        var response = jQuery.parseJSON(xmlHttpRequest.responseText);

                        // retrieves the exception from the response
                        var exception = response["exception"];

                        // retrieves the exception message
                        var exceptionMessage = exception["message"];

                        // shows a dialob window in the body
                        jQuery("body").dialogwindow("default", {
                            "title" : "Warning",
                            "subTitle" : "Problem Installing Plugin",
                            "message" : "There was a problem installing plugin: "
                                    + exceptionMessage,
                            "buttonMessage" : "Do you want to continue ?"
                        });
                    }
                }, 500);
            });

            // switches over the file extension
            switch(fileExtension) {
                // in case it's a bundle extension
                case "cbx":
                     // sets the bundles json url
                    var url = "bundles.json";

                    // breaks the switch
                    break;

                // in case it's a plugin extension
                case "cpx":
                     // sets the plugins json url
                    var url = "plugins.json";

                    // breaks the switch
                    break;
            }

            debugger;

            // opens the xml http request
            xmlHttpRequest.open("post", url);

            // sets the content type header
            xmlHttpRequest.setRequestHeader("Content-Type",
                    "application/octet-stream")

            // sends the file contents (in base64)
            xmlHttpRequest.send(fileContentsBase64);

            // creates a message windows with for the progress of
            // the installation
            jQuery("body").messagewindow("default", {
                        "title" : "Installing new plugin",
                        "subTitle" : "The systems is installing the new plugin",
                        "message" : "<div class=\"progress-indicator\"></div>",
                        "icon" : "resources/images/icon/icon-plugin-install.png"
                    });

            // starts the progress indicator
            jQuery(".message-message .progress-indicator", "body").progressindicator();
        };
    });

    jQuery("#overlay").bind("dragover", function(event) {
                // stops the event propagation and prevents
                // the default event operation
                event.stopPropagation();
                event.preventDefault();
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

    // loads the contents
    contentsLoad();
});

/**
 * Loads the initial contents, modifing the internal DOM structure if necessary.
 */
function contentsLoad() {
    // sets the page in the body
    jQuery("body").page();

    // sets the main container
    jQuery("#main-container").maincontainer();

    // reloads the contents page
    jQuery("#main-container").maincontainer("reload");
}

/**
 * Loads the page for the given hahs value.
 *
 * @param {String}
 *            hash The hash value to be reloaded.
 */
function pageLoad(hash) {
    changeContents(hash);
}

/**
 * Changes the contents of the main container.
 *
 * @param {String}
 *            target The target to be used in the update of the main container.
 */
function changeContents(target) {
    jQuery("#main-container").maincontainer("changeMenu", {
                target : target
            });

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
