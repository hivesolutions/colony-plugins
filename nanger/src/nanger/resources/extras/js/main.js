// Hive Colony Framework
// Copyright (c) 2008-2012 Hive Solutions Lda.
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
// __revision__  = $LastChangedRevision$
// __date__      = $LastChangedDate$
// __copyright__ = Copyright (c) 2008-2012 Hive Solutions Lda.
// __license__   = GNU General Public License (GPL), Version 3

jQuery(document).ready(function() {
    jQuery(".console").click(function() {
                var element = jQuery(this);
                var text = jQuery(".text", element);
                text.focus();
            });

    jQuery(".console .text").keyup(function() {
                var element = jQuery(this);
                var value = element.val();
                word = splitValue(value, true);

                jQuery(".console .line").html(word);
            });

    jQuery(".console .text").keydown(function() {
        // retrieves the key value
        var keyValue = event.keyCode ? event.keyCode : event.charCode
                ? event.charCode
                : event.which;

        console.info(keyValue);

        switch (keyValue) {
            case 37 :
                break;

            case 39 :
                break;

            default :
                break;
        }

        var element = jQuery(this);

        var value = element.val();
        word = splitValue(value, true);

        jQuery(".console .line").html(word);
    });

    jQuery(".console .text").keypress(function(event) {
        // retrieves the element
        var element = jQuery(this);

        // retrieves the key value
        var keyValue = event.keyCode ? event.keyCode : event.charCode
                ? event.charCode
                : event.which;

        // switches over the key value
        switch (keyValue) {
            case 13 :
                var value = element.val();
                var command = jQuery.trim(value);

                switch (value) {
                    case "clear" :
                        clear();

                        break;

                    default :
                        // tenho de chamar a execucao do comando
                        // neste ponto
                        jQuery.ajax({
                            url : "console/execute",
                            data : {
                                command : command,
                                instance : jQuery(".console").data("instance")
                            },
                            success : function(data) {
                                // unpacks the resulting json data into the result
                                // and the instance part, so that they may be used
                                // in the processing and printing of the result
                                var result = data["result"];
                                var instance = data["instance"];

                                // sets the instance (identifier) value in the console
                                // for latter usage of the value
                                jQuery(".console").data("instance", instance);

                                // resets the element value (virtual value) and clear the
                                // console line (to the original value)
                                element.val("");
                                jQuery(".console .line").html("");

                                jQuery(".console .previous").append("<div><span class=\"prompt\"># </span><span>"
                                        + splitValue(value, true)
                                        + "</span></div>");
                                var resultLine = jQuery("<span></span>");

                                var line = splitValue(result, true);
                                jQuery(".console .previous").append("<div>"
                                        + line + "</div>");
                                jQuery(".console").scrollTop(jQuery(".console")[0].scrollHeight);
                            }
                        });

                        break;
                }

                // breaks the switch
                break;

            default :
                var value = element.val();
                word = splitValue(value, true);

                jQuery(".console .line").html(word);

                break;
        }
    });

    jQuery(".console .text").focus(function() {
                jQuery(".console .cursor").css("display", "inline-block");
            });

    jQuery(".console .text").blur(function() {
                jQuery(".console .cursor").css("display", "none");
            });

    var escapeHtml = function(value) {
        return value.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g,
                "&gt;").replace(/\n/g, "<br/>").replace(/ /g, "&nbsp;");
    }

    var splitValue = function(value, escape) {
        var length = value.length;

        var slices = [];

        for (var index = 0; index < length; index += 1) {
            var slice = value.slice(index, index + 1);
            slices.push(slice);
        }

        var word = "";
        var slice = "";

        var sliceLength = slices.length;
        for (var index = 0; index < sliceLength; index++) {
            slice = escape ? escapeHtml(slices[index]) : slices[index];
            word += slice + "<wbr></wbr>";
        }

        return word;
    };

    var clear = function() {
        jQuery(".console .text").val("");
        jQuery(".console .line").empty();
        jQuery(".console .previous").empty();
    };

    // resets the console text to avoid any possible auto
    // complete operation
    jQuery(".console .text").val("");

    // "clicks" in the console so that the focus is started
    // at the console (immediate interaction)
    jQuery(".console").click();
});
