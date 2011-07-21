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
    // initializes the spacer according to the parameter
    var spaceValue = space ? " " : "";

    // retrieves the text area element
    var text = document.getElementById("wiki-page-contents-text-area");

    // computes the delta for the selection
    var delta = text.selectionEnd - text.selectionStart;

    // retrieves the slice before the selection
    var first = text.value.slice(0, text.selectionStart);

    // retrieves the selection slice
    var second = text.value.slice(text.selectionStart, text.selectionEnd);

    // retrieves the slice after the selection
    var third = text.value.slice(text.selectionEnd, text.value.length);

    // assembles the final value placing the token and spacer between the slices
    var finalValue = first + token + spaceValue + second + spaceValue
            + endToken + third;

    // sets the text value
    text.value = finalValue;
}

jQuery(document).ready(function() {
    // for each wiki button
    jQuery(".wiki-button").each(function(index, element) {
        // retrieves the element
        var elementReference = jQuery(element);

        // clones the element
        elementReference.clone();

        // creates the wiki button container markup
        var wikiButtonContainerHtml = "<div class=\"wiki-button-container\"></div>";

        // creates the wiki button container element
        var wikiButtonContainer = jQuery(wikiButtonContainerHtml);

        // replaces the matched object with the new button container
        elementReference.replaceWith(wikiButtonContainer);

        // appends the element to the container to finish the wrapping
        wikiButtonContainer.append(elementReference);

        // retrieves the element class
        var classes = elementReference.attr("class");

        // splits the classes string
        var classesList = classes.split(" ")

        // for each class
        for (var i = 0; i < classesList.length; i++) {
            // retrieves the class value
            var classValue = classesList[i].trim();

            // in case the class is not the wiki button class
            if (classValue != "wiki-button") {
                // adds the matched object class to the container element
                wikiButtonContainer.addClass(classValue);
            }
        }
    });

    jQuery(".wiki-button").mousedown(function() {
                jQuery(this).addClass("click");
            });

    jQuery(".wiki-button").mouseup(function() {
                jQuery(this).removeClass("click");
            });

    jQuery("#wiki-page-edit-button").click(function(event) {
                if (jQuery("#wiki-page-edit").is(":visible")) {
                    jQuery("#wiki-page-edit").fadeOut(200);
                } else {
                    jQuery("#wiki-page-edit").fadeIn(300);
                }

                // stops the event propagation
                event.stopPropagation();
            });

    jQuery(document).click(function() {
                jQuery("#wiki-page-edit").fadeOut(200);
            });

    jQuery("#wiki-page-edit").click(function(event) {
                // stops the event propagation to avoid handling by the body
                event.stopPropagation();
            });


    jQuery(".wiki-input, .wiki-text-area").focus(function() {
                jQuery(this).addClass("selected");
            });

    jQuery(".wiki-input, .wiki-text-area").blur(function() {
                jQuery(this).removeClass("selected");
            });

    jQuery(".wiki-control-icon-bold").click(function() {
                textGetSelection("**", "**", false);
            });

    jQuery(".wiki-control-icon-italic").click(function() {
                textGetSelection("//", "//", false);
            });

    jQuery(".wiki-control-icon-quote").click(function() {
                textGetSelection("<quote author=\"...\">", "</quote>", false);
            });

    jQuery("#wiki-page-new-publish-button").click(function() {
                jQuery(this).parents("form").submit();
            });

    jQuery("#wiki-page-edit-publish-button").click(function() {
        // retrieves the contents value
        var contents = jQuery("#wiki-page-edit-contents-text-area").attr("value");

        // retrieves the symmary value
        var summary = jQuery("#wiki-page-edit-summary-input").attr("value");

        // retrieves the wiki page value
        var wikiPage = jQuery("#wiki-page-title").html();

        // creates the complete url
        var completeUrl = "pages/" + wikiPage + "/update.json";

        // calls the edit resource
        jQuery.ajax({
                    type : "post",
                    url : completeUrl,
                    data : {
                        "page[contents]" : contents,
                        "page[summary]" : summary
                    },
                    success : function(data) {
                        jQuery.ajax({
                                    type : "get",
                                    url : wikiPage + ".ajx",
                                    success : function(data) {
                                        jQuery("#wiki-contents").html(data);
                                        jQuery("#wiki-page-edit").fadeOut(200);
                                    }
                                });
                    }
                });
    });

    jQuery(".wiki-input").each(function(index, value) {
                // retrieves the value reference
                var valueReference = jQuery(value);

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
