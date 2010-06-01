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
    // defines the number of records retrieved per page
    var numberRecords = 10;

    // defines the customer data retrieval url
    var url = "invoices/partial";

    // defines the request arguments for the previous button
    var previousButtonData = "start_record=0&number_records=" + numberRecords;

    // defines the request arguments for the next button
    var nextButtonData = "start_record=0&number_records=" + numberRecords;

    // defines the contents of the page indicator
    var pageIndicator = "";

    // the table content callback function
    var tableContentCallback = function(result) {
        // parses the result
        var tableBody = result.split("<tbody id=\"invoice-table-body\">")[1].split("</tbody>")[0];
        var startRecord = parseInt(result.split("<div id=\"start-record\">")[1].split("</div>")[0]);
        var endRecord = parseInt(result.split("<div id=\"end-record\">")[1].split("</div>")[0]);
        var previousStartRecord = parseInt(result.split("<div id=\"previous-start-record\">")[1].split("</div>")[0]);
        var nextStartRecord = parseInt(result.split("<div id=\"next-start-record\">")[1].split("</div>")[0]);
        var totalNumberRecords = parseInt(result.split("<div id=\"total-number-records\">")[1].split("</div>")[0]);

        // updates the table
        $("#invoice-table tbody").empty();
        $("#invoice-table tbody").append(tableBody);

        // updates the start record for the next button and previous buttons
        previousButtonData = "start_record=" + previousStartRecord
                + "&number_records=" + numberRecords;
        nextButtonData = "start_record=" + nextStartRecord + "&number_records="
                + numberRecords;

        // updates the current page
        if (totalNumberRecords) {
            pageIndicator = (startRecord + 1) + " - " + endRecord + " of "
                    + totalNumberRecords;
        } else {
            pageIndicator = "0 - 0 of 0";
        }
        $("#page-indicator").empty();
        $("#page-indicator").append(pageIndicator);
    };

    // fetches the first page
    $.ajax({
                url : url,
                type : "post",
                data : previousButtonData,
                success : tableContentCallback
            });

    // registers the handler for the previous button
    $("#previous-button").click(function() {
                $.ajax({
                            url : url,
                            type : "post",
                            data : previousButtonData,
                            success : tableContentCallback
                        });
            });

    // registers the handler for the next button
    $("#next-button").click(function() {
                $.ajax({
                            url : url,
                            type : "post",
                            data : nextButtonData,
                            success : tableContentCallback
                        });
            });
});
