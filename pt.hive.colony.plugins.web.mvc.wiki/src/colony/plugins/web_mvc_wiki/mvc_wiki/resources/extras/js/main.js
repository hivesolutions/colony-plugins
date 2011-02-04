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

function textGetSelection(token, endToken, space) {
    var spaceValue = space ? " " : "";

    var text = document.getElementById("wiki-page-contents-text-area");

    var delta = text.selectionEnd - text.selectionStart;

    var first = text.value.slice(0, text.selectionStart);
    var second = text.value.slice(text.selectionStart, text.selectionEnd);
    var third = text.value.slice(text.selectionEnd, text.value.length);

    var finalValue = first + token + spaceValue + second + spaceValue
            + endToken + third;

    text.value = finalValue;
}

$(document).ready(function() {

    $(".wiki-button").each(function(index, element) {
                var elemento = $(element).clone();

                var html = "<div class=\"wiki-button-container\"></div>";

                var elemento = $(html);

                var novoElement = $(element).replaceWith(elemento);

                elemento.append($(element))

                var classes = $(element).attr("class");

                var classesList = classes.split(" ")

                for (var i = 0; i < classesList.length; i++) {
                    var classValue = classesList[i].trim();

                    if (classValue != "wiki-button") {
                        elemento.addClass(classValue);
                    }
                }
            });

    $("#wiki-options-button").click(function() {
                window.location = $("#wiki-page-title").html() + ".prt";
            });

    $(".wiki-button").mousedown(function() {
                $(this).addClass("click");
            });

    $(".wiki-button").mouseup(function() {
                $(this).removeClass("click");
            });

    $("#wiki-page-edit-button").click(function(event) {
                if ($("#wiki-page-edit").is(":visible")) {
                    $("#wiki-page-edit").fadeOut(200);
                } else {
                    $("#wiki-page-edit").fadeIn(300);
                }

                // stops the event propagation
                event.stopPropagation();
            });

    $(document).click(function() {
                $("#wiki-page-edit").fadeOut(200);
            });

    $("#wiki-page-edit").click(function(event) {
                // stops the event propagation to avoid handling by the body
                event.stopPropagation();
            });

    $("#wiki-more-button").click(function() {
                if ($("#wiki-sub-header").is(":visible")) {
                    $("#wiki-sub-header").fadeOut(200);
                } else {
                    $("#wiki-sub-header").fadeIn(300);
                }
            });

    $(".wiki-input, .wiki-text-area").focus(function() {
                $(this).addClass("selected");
            });

    $(".wiki-input, .wiki-text-area").blur(function() {
                $(this).removeClass("selected");
            });

    $(".wiki-control-icon-bold").click(function() {
                textGetSelection("**", "**", false);
            });

    $(".wiki-control-icon-italic").click(function() {
                textGetSelection("//", "//", false);
            });

    $(".wiki-control-icon-quote").click(function() {
                textGetSelection("<quote author=\"...\">", "</quote>", false);
            });

    $("#wiki-page-new-publish-button").click(function() {
                $(this).parents("form").submit();
            });

    $("#wiki-page-edit-publish-button").click(function() {
                // retrieves the contents value
                var contents = $("#wiki-page-edit-contents-text-area").attr("value");

                // retrieves the symmary value
                var summary = $("#wiki-page-edit-summary-input").attr("value");

                // retrieves the wiki page value
                var wikiPage = $("#wiki-page-title").html();

                // creates the complete url
                var completeUrl = "pages/" + wikiPage + "/update";

                // calls the edit resource
                $.ajax({
                            type : "post",
                            url : completeUrl,
                            data : {
                                "page[contents]" : contents,
                                "page[summary]" : summary
                            },
                            success : function(data) {
                                $.ajax({
                                            type : "get",
                                            url : wikiPage + ".ajx",
                                            success : function(data) {
                                                $("#wiki-contents").html(data);
                                                $("#wiki-page-edit").fadeOut(200);
                                            }
                                        });
                            }
                        });
            });

    $(".wiki-input").each(function(index, value) {
                // retrieves the value reference
                var valueReference = $(value);

                // retrieves the current status
                var currentStatus = valueReference.attr("current_status");

                // retrieves the original value
                var originalValue = valueReference.attr("original_value");

                // in case the current status is invalid
                if (currentStatus == "invalid") {
                    // adds the invalid mode class
                    valueReference.addClass("invalid");
                } else if (currentStatus != "") {
                    valueReference.attr("value", currentStatus);
                }

                // retrieves the current value
                var currentValue = valueReference.attr("value");

                // in case the current value is the original one
                if (currentValue == originalValue) {
                    // adds the lower (background) mode class
                    valueReference.addClass("lower");
                }

                // registers for the focus event
                valueReference.focus(function(event) {
                            // retrieves the current value
                            var currentValue = valueReference.attr("value");

                            // in case the current value is
                            // the original one
                            if (currentValue == originalValue) {
                                valueReference.attr("value", "");
                                valueReference.removeClass("lower");
                                if (currentStatus == "invalid") {
                                    // removes the invalid mode class
                                    valueReference.removeClass("invalid");
                                }
                            }
                        });

                // registers for the blur event
                valueReference.blur(function(event) {
                            // retrieves the current value
                            var currentValue = valueReference.attr("value");

                            // in case the current value is empty
                            if (currentValue == "") {
                                valueReference.attr("value", originalValue);
                                valueReference.addClass("lower");
                                if (currentStatus == "invalid") {
                                    // adds the invalid mode class
                                    valueReference.addClass("invalid");
                                }
                            }
                        });
            });
});
