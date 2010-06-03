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

// the enter key code
var ENTER = 13;

// the number of record to be retrieved at each time
var NUMBER_RECORDS = 15;

$(document).ready(function() {
            // sets the logic loaded data
            var logicLoaded = $("#contents").data("logicLoaded");

            // in case the logic is already loaded
            if (logicLoaded) {
                // returns immediately
                return
            }

            resetTableSearch();
            baseTableHandlers();

            // registers the handler for the next button
            $("#search-query").keydown(function(event) {
                        var keyCode = event.keyCode;

                        if (keyCode == ENTER) {
                            // resets the table search
                            resetTableSearch();

                            // performs the search
                            search(false);
                        }
                    });

            // registers the handler for the key event in the search query field
            $("#search-query").keyup(function(event) {
                        // resets the table search
                        resetTableSearch();

                        // performs the search
                        search(false);
                    });

        });

function search(update) {
    // retrieves the current search query value
    var searchQuery = $("#search-query").attr("value");

    // retrieves the current final record
    var currentFinalRecord = $("#plugin-table").data("currentFinalRecord",
            currentFinalRecord);

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
                    partialCallback(data, update);
                }
            });
}

function partialCallback(data, update) {
    // retrieves the data element
    var dataElement = $(data);

    // retrieves the table body data
    var tableBody = $("#table-body", dataElement);

    // retrieves the table metadata data
    var tableMetadata = $("#meta-data", dataElement);

    // creates the switch buttons for the table
    $(".switch-button", tableBody).switchbutton();

    // register the base table handlers
    baseTableHandlers(tableBody);

    if (update) {
        $("#plugin-table > tbody").append($("tr", tableBody));
    } else {
        // replaces the table body contents
        $("#plugin-table > tbody").replaceWith(tableBody);
    }

    // retrieves the number of records retrieves
    var numberRecords = parseInt($("#number-records", tableMetadata).html());
    var totalNumberRecords = parseInt($("#total-number-records", tableMetadata).html());

    // sets the initial table data
    var currentFinalRecord = $("#plugin-table").data("currentFinalRecord");
    currentFinalRecord += numberRecords;

    // removes the more button
    $("#more-button").remove();

    if (currentFinalRecord < totalNumberRecords) {
        // creates the button html code
        var htmlCode = "<div id=\"more-button\" class=\"button button-green center\">More</div>";

        // appends the button html code
        $("#plugin-table").after(htmlCode);

        // creates the more button
        $("#more-button").button();

        // register the click callback for the more button
        $("#more-button").click(function() {
                    // performs a search
                    search(true);
                });
    }

    // sets the new table values
    $("#plugin-table").data("currentFinalRecord", currentFinalRecord);
    $("#plugin-table").data("totalNumberRecords", totalNumberRecords);

    // updates the main container (size)
    $("#main-container").maincontainer("update");

    if (update) {
        $.scrollTo($("#plugin-table > tfoot"), 400, {
                    offset : {
                        top : -50,
                        left : 0
                    }
                });
    }
}

function resetTableSearch() {
    // sets the initial table data
    $("#plugin-table").data("currentFinalRecord", 0);
    $("#plugin-table").data("totalNumberRecords", 0);
}

function baseTableHandlers(context) {
    // retrieves the context or the default one
    var context = context ? context : $("#plugin-table");

    $(".switch-button", context).bind("status_change",
            function(event, element, status) {
                // retrieves the switch button
                var switchButton = $(this);

                // retrieves the plugin id from the switch button
                var pluginId = switchButton.attr("plugin");

                // retrieves the plugin status, from the stauts of the switch button
                var pluginStatus = status == "on" ? "load" : "unload";

                // retrieves the oposite status
                var opositeStatus = status == "on" ? "off" : "on";

                // removes the status class, and adds
                // the oposite class (changing status)
                switchButton.removeClass(status);
                switchButton.addClass(opositeStatus);

                $.ajax({
                    url : "plugins/change_status.json",
                    type : "post",
                    data : {
                        plugin_id : pluginId,
                        plugin_status : pluginStatus
                    }
                });
            });

    // sets the logic loaded data
    $("#contents").data("logicLoaded", true);
}
