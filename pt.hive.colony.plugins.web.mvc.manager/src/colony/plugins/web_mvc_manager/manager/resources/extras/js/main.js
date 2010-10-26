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
    var jsonData = $.parseJSON(data);

    // retrieves the message id and contents
    var messageId = jsonData["id"];
    var messageContents = jsonData["contents"];

    if (messageId == "web_mvc_manager/plugin/change_status") {
        // parses the data (json) retrieving the status
        var status = $.parseJSON(messageContents);

        // retrieves the unloaded plugins
        var unloadedPlugins = status["unloaded"];

        // iterates over all the unloaded plugins
        $(unloadedPlugins).each(function(index, element) {
            var switchButtonElement = $("#plugin-table .switch-button[plugin="
                    + element + "]");
            switchButtonElement.removeClass("on");
            switchButtonElement.addClass("off");

            $("#notification-area-contents").notificationwindow("default", {
                        "title" : "<span class=\"red\">Plugin Unloaded</span>",
                        "subTitle" : "",
                        "message" : element,
                        "timeout" : 5000
                    });
        });

        // retrieves the loaded plugins
        var loadedPlugins = status["loaded"];

        // iterates over all the loaded plugins
        $(loadedPlugins).each(function(index, element) {
            var switchButtonElement = $("#plugin-table .switch-button[plugin="
                    + element + "]");
            switchButtonElement.removeClass("off");
            switchButtonElement.addClass("on");

            $("#notification-area-contents").notificationwindow("default", {
                        "title" : "<span class=\"green\">Plugin Loaded</span>",
                        "subTitle" : "",
                        "message" : element,
                        "timeout" : 5000
                    });
        });
    } else if (messageId == "web_mvc_manager/plugin/install") {
        // parses the data (json) retrieving the status
        var status = $.parseJSON(messageContents);

        // retrieves the uninstalled plugins
        var uninstalledPlugins = status["uninstalled"];

        // iterates over all the uninstalled plugins
        $(uninstalledPlugins).each(function(index, element) {
            $("#notification-area-contents").notificationwindow("default", {
                        "title" : "<span class=\"red\">Plugin Uninstalled</span>",
                        "subTitle" : "",
                        "message" : element,
                        "timeout" : 5000
                    });
        });

        // retrieves the installed plugins
        var installedPlugins = status["installed"];

        // iterates over all the installed plugins
        $(installedPlugins).each(function(index, element) {
            $("#notification-area-contents").notificationwindow("default", {
                        "title" : "<span class=\"green\">Plugin Installed</span>",
                        "subTitle" : "",
                        "message" : element,
                        "timeout" : 5000
                    });
        });
    } else if (messageId == "web_mvc_manager/header/reload") {
        // reloads the header
        $("body").page("reloadHeader");
    } else if (messageId == "web_mvc_manager/side_panel/reload") {
        // retrieves the current active menu as the target menu
        var targetMenu = $("#main-container").data("menu");

        // reloads the metadata in the main container
        $("#main-container").maincontainer("loadMetadata", {
                    forceReload : true,
                    target : targetMenu
                });
    }
}

$(document).ready(function() {
    $("body").communication("default", {
                url : "communication",
                timeout : 500,
                dataCallbackFunctions : [messageProcessor]
            });

    $("body").bind("dragenter", function(event) {
                // stops the event propagation and prevents
                // the default event operation
                event.stopPropagation();
                event.preventDefault();

                $("body").messagewindow("default", {
                            "title" : "Install new plugin",
                            "subTitle" : "",
                            "message" : "Drop the file to install the new plugin.",
                            "icon" : "resources/images/icon/icon-plugin-install.png"
                        });
            });

    $("#overlay").bind("dragleave", function(event) {
                // stops the event propagation and prevents
                // the default event operation
                event.stopPropagation();
                event.preventDefault();

                // closes the message window
                $("body").messagewindow("close");
            });

    $("#overlay").bind("drop", function(event) {
        // stops the event propagation and prevents
        // the default event operation
        event.stopPropagation();
        event.preventDefault();

        // closes the message window
        $("body").messagewindow("close");

        // retrieves the data tranfer and the files
        // rom the original event
        var dataTransfer = event.originalEvent.dataTransfer;
        var files = dataTransfer.files;

        // retrieves the first file
        var file = files[0];

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
            var uploadElement = $(xmlHttpRequest.upload);

            uploadElement.bind("progress", function(event) {
                if (event.lengthComputable) {
                    // calculates the percentage of loading
                    var percentage = Math.round((event.loaded * 100)
                            / event.total);

                    // sets the progress indicator percentage
                    $(".message-message .progress-indicator", "body").progressindicator(
                            "change", {
                                percentage : percentage
                            });
                }
            });

            uploadElement.bind("load", function(event) {
                // sets the progress indicator percentage
                $(".message-message .progress-indicator", "body").progressindicator(
                        "change", {
                            percentage : 100
                        });

                // sets a timeout to close the message window
                setTimeout(function() {
                    // closes the message window
                    $("body").messagewindow("close");

                    if (xmlHttpRequest.status == 200) {
                        $("#notification-area-contents").notificationwindow(
                                "default", {
                                    "title" : "<span class=\"green\">Plugin Installed</span>",
                                    "subTitle" : "",
                                    "message" : "Plugin installed successfully",
                                    "timeout" : 5000
                                });
                    } else {
                        $("body").dialogwindow("default", {
                            "title" : "Warning",
                            "subTitle" : "Problem Installing Plugin",
                            "message" : "There was a problem installing plugin, this indicates a problem in the server or a problem in the sent file.",
                            "buttonMessage" : "Do you want to continue ?"
                        });
                    }
                }, 500);
            });

            // opens the xml http request
            xmlHttpRequest.open("post", "plugins/new");

            // sets the content type header
            xmlHttpRequest.setRequestHeader("Content-Type",
                    "application/octet-stream")

            // sends the file contents (in base64)
            xmlHttpRequest.send(fileContentsBase64);

            // creates a message windows with for the progress of
            // the installation
            $("body").messagewindow("default", {
                        "title" : "Installing new plugin",
                        "subTitle" : "The systems is installing the new plugin",
                        "message" : "<div class=\"progress-indicator\"></div>",
                        "icon" : "resources/images/icon/icon-plugin-install.png"
                    });

            // starts the progress indicator
            $(".message-message .progress-indicator", "body").progressindicator();
        };
    });

    $("#overlay").bind("dragover", function(event) {
                // stops the event propagation and prevents
                // the default event operation
                event.stopPropagation();
                event.preventDefault();
            });

    $("#account-description").click(function() {
                if (!$("#account-float-panel").is(":visible")) {
                    $("#account-float-panel").fadeIn(200, function() {
                                $("#account-float-panel").click(
                                        function(event) {
                                            event.stopPropagation();

                                        });
                                $(document).click(function(event) {
                                            $("#account-float-panel").hide();
                                            $(document).unbind("click");
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
    $("body").page();

    // sets the main container
    $("#main-container").maincontainer();

    // reloads the contents page
    $("#main-container").maincontainer("reload");
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
    $("#main-container").maincontainer("changeMenu", {
                target : target
            });

    $("#main-container").maincontainer("change", {
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
    return $("#environment-variables > #base-path").html();
}

/**
 * Retrieves the ajax submit value based on a component placed in the dom.
 *
 * @return {String} The ajax submit.
 */
function getAjaxSubmit() {
    // returns the ajax submit value, based on the
    // component in the dom
    return $("#environment-variables > #ajax-submit").html();
}
