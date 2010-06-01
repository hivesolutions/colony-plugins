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

$(document).ready(function() {
    // the enter key code
    var ENTER = 13;

    // the number of record to be retrieved at each time
    var NUMBER_RECORDS = 15;

    // sets the logic loaded data
    var logicLoaded = $("#contents").data("logicLoaded");

    // in case the logic is already loaded
    if (logicLoaded) {
        // returns immediately
        return
    }

    var search = function() {
        // retrieves the current search query value
        var searchQuery = $("#search-query").attr("value");

        currentFinalRecord = 0;

        // assembles the form data to submit with the search button click event
        var searchButtonData = {
            search_query : searchQuery,
            start_record : currentFinalRecord,
            number_records : NUMBER_RECORDS
        };

        // processes the ajax request
        $.ajax({
            url : "plugins/partial",
            type : "post",
            data : searchButtonData,
            success : function(data) {
                // retrieves the data element
                var dataElement = $(data);

                // retrieves the table body data
                var tableBody = $("#table-body", dataElement);

                // retrieves the table metadata data
                var tableMetadata = $("#meta-data", dataElement);

                // removes the metadata components
                $("#plugin-table > #meta-data").remove();

                // replaces the table body contents
                $("#plugin-table > tbody").replaceWith(tableBody);

                // appends the table metadata to the plugin table
                $("#plugin-table").append(tableMetadata);

                // creates the switch buttons for the table
                $("#plugin-table .switch-button").switchbutton();

                $("#plugin-table .switch-button").bind("status_change",
                        function(event, element, status) {
                            // retrieves the switch button
                            var switchButton = $(this);

                            // retrieves the plugin id from the switch button
                            var pluginId = switchButton.attr("plugin");

                            // retrieves the plugin status, from the stauts of the switch button
                            var pluginStatus = status == "on"
                                    ? "load"
                                    : "unload";

                            // retrieves the oposite status
                            var opositeStatus = status == "on" ? "off" : "on";

                            switchButton.removeClass(status);
                            switchButton.addClass(opositeStatus);

                            $.ajax({
                                url : "plugins/change_status.json",
                                type : "post",
                                data : {
                                    plugin_id : pluginId,
                                    plugin_status : pluginStatus
                                },
                                success : function(data) {
                                    // parses the data (json) retrieving the status
                                    var status = $.parseJSON(data);

                                    // retrieves the unloaded plugins
                                    var unloadedPlugins = status["unloaded"];

                                    $(unloadedPlugins).each(
                                            function(index, element) {
                                                var switchButtonElement = $("#plugin-table .switch-button[plugin="
                                                        + element + "]");
                                                switchButtonElement.removeClass("on");
                                                switchButtonElement.addClass("off");

                                                $("#notification-area-contents").notificationwindow(
                                                        "default", {
                                                            "title" : "<span class=\"red\">Plugin Unloaded</span>",
                                                            "subTitle" : "",
                                                            "message" : element,
                                                            "timeout" : 5000
                                                        });
                                            });

                                    // retrieves the loaded plugins
                                    var loadedPlugins = status["loaded"];

                                    $(loadedPlugins).each(
                                            function(index, element) {
                                                var switchButtonElement = $("#plugin-table .switch-button[plugin="
                                                        + element + "]");
                                                switchButtonElement.removeClass("off");
                                                switchButtonElement.addClass("on");

                                                $("#notification-area-contents").notificationwindow(
                                                        "default", {
                                                            "title" : "<span class=\"green\">Plugin Loaded</span>",
                                                            "subTitle" : "",
                                                            "message" : element,
                                                            "timeout" : 5000
                                                        });
                                            });
                                }
                            });
                        });

                $("#main-container").maincontainer("update");
            }
        });
    }

    // registers the handler for the next button
    $("#search-query").keydown(function(event) {
                var keyCode = event.keyCode;

                if (keyCode == ENTER) {
                    // performs the search
                    search();
                }
            });

    // registers the handler for the key event in the search query field
    $("#search-query").keyup(function(event) {
                // performs the search
                search();
            });

    $("#plugin-table .switch-button").bind("status_change",
            function(event, element, status) {
                // retrieves the switch button
                var switchButton = $(this);

                // retrieves the plugin id from the switch button
                var pluginId = switchButton.attr("plugin");

                // retrieves the plugin status, from the stauts of the switch button
                var pluginStatus = status == "on" ? "load" : "unload";

                // retrieves the oposite status
                var opositeStatus = status == "on" ? "off" : "on";

                switchButton.removeClass(status);
                switchButton.addClass(opositeStatus);

                $.ajax({
                    url : "plugins/change_status.json",
                    type : "post",
                    data : {
                        plugin_id : pluginId,
                        plugin_status : pluginStatus
                    },
                    success : function(data) {
                        // parses the data (json) retrieving the status
                        var status = $.parseJSON(data);

                        // retrieves the unloaded plugins
                        var unloadedPlugins = status["unloaded"];

                        $(unloadedPlugins).each(function(index, element) {
                            var switchButtonElement = $("#plugin-table .switch-button[plugin="
                                    + element + "]");
                            switchButtonElement.removeClass("on");
                            switchButtonElement.addClass("off");

                            $("#notification-area-contents").notificationwindow(
                                    "default", {
                                        "title" : "<span class=\"red\">Plugin Unloaded</span>",
                                        "subTitle" : "",
                                        "message" : element,
                                        "timeout" : 5000
                                    });
                        });

                        // retrieves the loaded plugins
                        var loadedPlugins = status["loaded"];

                        $(loadedPlugins).each(function(index, element) {
                            var switchButtonElement = $("#plugin-table .switch-button[plugin="
                                    + element + "]");
                            switchButtonElement.removeClass("off");
                            switchButtonElement.addClass("on");

                            $("#notification-area-contents").notificationwindow(
                                    "default", {
                                        "title" : "<span class=\"green\">Plugin Loaded</span>",
                                        "subTitle" : "",
                                        "message" : element,
                                        "timeout" : 5000
                                    });
                        });
                    }
                });
            });

    // sets the logic loaded data
    $("#contents").data("logicLoaded", true);
});
