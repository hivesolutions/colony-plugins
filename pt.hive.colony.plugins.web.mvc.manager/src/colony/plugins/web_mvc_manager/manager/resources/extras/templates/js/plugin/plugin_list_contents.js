// Take The Bill Service
// Copyright (C) 2010 Hive Solutions Lda.
//
// This file is part of Take The Bill Service.
//
// Take The Bill Service is confidential and property of Hive Solutions Lda,
// its usage is constrained by the terms of the Hive Solutions
// Confidential Usage License.
//
// Take The Bill Service should not be distributed under any circumstances,
// violation of this may imply legal action.
//
// If you have any questions regarding the terms of this license please
// refer to <http://www.hive.pt/licenses/>.

// __author__    = Tiago Sílva <tsilva@hive.pt>
// __version__   = 1.0.0
// __revision__  = $LastChangedRevision$
// __date__      = $LastChangedDate$
// __copyright__ = Copyright (c) 2010 Hive Solutions Lda.
// __license__   = Hive Solutions Confidential Usage License (HSCUL)

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
                type : "POST",
                data : previousButtonData,
                success : tableContentCallback
            });

    // registers the handler for the previous button
    $("#previous-button").click(function() {
                $.ajax({
                            url : url,
                            type : "POST",
                            data : previousButtonData,
                            success : tableContentCallback
                        });
            });

    // registers the handler for the next button
    $("#next-button").click(function() {
                $.ajax({
                            url : url,
                            type : "POST",
                            data : nextButtonData,
                            success : tableContentCallback
                        });
            });
});
