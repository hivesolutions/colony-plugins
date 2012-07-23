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
	// registers for the click event in the console to
	// propagate the focus event to the text area
    jQuery(".console").click(function() {
                var element = jQuery(this);
                var text = jQuery(".text", element);
                text.focus();
            });

    jQuery(".console .text").keydown(function(event) {
        // retrieves the current element
        var element = jQuery(this);

        // retrieves the text currently in used for the context
        // of the console (current command)
        var value = jQuery(".console").data("text") || "";

        // retrieves the key value
        var keyValue = event.keyCode ? event.keyCode : event.charCode
                ? event.charCode
                : event.which;

        // sets the default value for the canceling operation
        // (no default behavior) as true (most of the times)
        var cancel = true;

        switch (keyValue) {
            case 8 :
                var cursor = jQuery(".console").data("cursor");
                if (cursor == value.length - 1) {
                    break;
                }

                var first = value.slice(0, value.length - cursor - 2);
                var second = value.slice(value.length - cursor - 1,
                        value.length);
                var value = first + second;
                jQuery(".console").data("text", value)

                refresh();
                break;

            case 27 :
                jQuery(".console .autocomplete").hide();
                break;

            case 35 :
                jQuery(".console").data("cursor", -1);
                refresh();
                break;

            case 36 :
                jQuery(".console").data("cursor", value.length - 1);
                refresh();
                break;

            case 37 :
                var cursor = jQuery(".console").data("cursor");
                if (cursor == value.length - 1) {
                    break;
                }
                cursor++;
                jQuery(".console").data("cursor", cursor);

                refresh();

                break;

            case 38 :
                var history = jQuery(".console").data("history") || [];
                var historyIndex = jQuery(".console").data("history_index")
                        || 0;

                var value = history[history.length - historyIndex - 1];
                if (historyIndex != history.length - 1) {
                    historyIndex++;
                }

                console.info("history -> " + history);
                console.info("historyIndex -> " + historyIndex);

                jQuery(".console").data("text", value)
                jQuery(".console").data("history_index", historyIndex)

                refresh();
                break;

            case 39 :
                var cursor = jQuery(".console").data("cursor");
                if (cursor == -1) {
                    break;
                }
                cursor--;
                jQuery(".console").data("cursor", cursor);

                refresh();
                break;

            case 40 :
                var history = jQuery(".console").data("history") || [];
                var historyIndex = jQuery(".console").data("history_index")
                        || 0;

                var value = history[history.length - historyIndex - 1];
                if (historyIndex != 0) {
                    historyIndex--;
                }

                jQuery(".console").data("text", value)
                jQuery(".console").data("history_index", historyIndex)

                refresh();
                break;

            case 46 :
                var cursor = jQuery(".console").data("cursor");
                if (cursor == -1) {
                    break;
                }

                var first = value.slice(0, value.length - cursor - 1);
                var second = value.slice(value.length - cursor, value.length);
                var value = first + second;

                jQuery(".console").data("text", value)
                jQuery(".console").data("cursor", cursor - 1)

                refresh();
                break;

            default :
                cancel = false;
                break;
        }

        // updates the cancel data attribute in the
        // console to provide information to the hadling
        // of the key pressing in the next event
        jQuery(".console").data("cancel", cancel)

        // stops the event propagation this should be able
        // to avoid possible problems with double handling
        event.stopPropagation();
        event.stopImmediatePropagation();
    });

    jQuery(".console .text").bind("paste", function(event) {
        // retrieves the element
        var element = jQuery(this);

        setTimeout(function() {
                    // retrieves the current value of the element and clears
                    // the contents of the text element to avoid  any duplicate
                    // paste operation (unwanted behavior)
                    var character = element.val();
                    element.val("");

                    var text = jQuery(".console").data("text") || "";

                    // adds the new character into the text buffer
                    // by slicing the value around the current position,
                    // then joins the value back with the character
                    var cursor = jQuery(".console").data("cursor");
                    var first = text.slice(0, text.length - cursor - 1);
                    var second = text.slice(text.length - cursor - 1,
                            text.length);
                    var value = first + character + second;

                    // splits the various lines of the value arround
                    // the newline character to retrieve the commands
                    var commands = value.split("\n");

                    // in case there are multiple commands the multiline
                    // mode is activated and execution of the commands
                    // is ensured immediately
                    if (commands.length > 1) {
                        var _commands = jQuery(".console").data("commands")
                                || [];
                        for (var index = 0; index < commands.length; index++) {
                            _commands.push(commands[index]);
                        }
                        jQuery(".console").data("commands", _commands);
                        process();
                    }

                    // updates the text value of the console and refreshes
                    // the visual part of it
                    var value = commands[commands.length - 1];
                    jQuery(".console").data("text", value);
                    refresh();
                }, 0);
    });

    var isIgnorableKey = function(e) {
        // for now just filter alt+tab that we receive on some platforms when
        // user switches windows (goes away from the browser)
        return ((e.keyCode == 18 || e.keyCode == 192) && e.altKey);
    };

    jQuery(".console .text").keypress(function(event) {
        // retrieves the element
        var element = jQuery(this);

        // retrieves the key value
        var keyValue = event.keyCode ? event.keyCode : event.charCode
                ? event.charCode
                : event.which;

        var keyCode = event.keyCode || event.which;
        var character = String.fromCharCode(keyCode);
        var text = jQuery(".console").data("text") || "";
        var cancel = jQuery(".console").data("cancel") || false;

        if (cancel) {
            return false;
        }

        if ((event.ctrlKey || event.metaKey)
                && String.fromCharCode(keyCode).toLowerCase() == "v") {
            return true;
        }

        if ((event.ctrlKey || event.metaKey)
                && String.fromCharCode(keyCode).toLowerCase() == "r") {
            return true;
        }

        // switches over the key value
        switch (keyValue) {
            case 13 :
                var value = jQuery(".console").data("text") || "";

                switch (value) {
                    case "clear" :
                        // clears the current console display removing the various
                        // information contained in it
                        clear();
                        event.preventDefault();

                        // breaks the switch
                        break;

                    default :
                        // runs the process of the "remote" command this should trigger
                        // the execution of the server side execution
                        var commands = jQuery(".console").data("commands")
                                || [];
                        commands.push(value);
                        jQuery(".console").data("commands", commands)
                        process();

                        // breaks the switch
                        break;
                }

                // breaks the switch
                break;

            default :
                // adds the new character into the text buffer
                // by slicing the value around the current position,
                // then joins the value back with the character
                var cursor = jQuery(".console").data("cursor");
                var first = text.slice(0, text.length - cursor - 1);
                var second = text.slice(text.length - cursor - 1, text.length);
                var value = first + character + second;

                // updates the text value of the console and refreshes
                // the visual part of it
                jQuery(".console").data("text", value);
                refresh();
                autocomplete();

                // breaks the switch
                break;
        }

        event.stopPropagation();
        event.stopImmediatePropagation();
        event.preventDefault();
    });

    jQuery(".console .text").focus(function() {
                jQuery(".console .cursor").css("background-color", "#b0b0b0");
            });

    jQuery(".console .text").blur(function() {
                jQuery(".console .cursor").css("background-color",
                        "transparent");
            });

    var escapeHtml = function(value) {
        return value.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g,
                "&gt;").replace(/\n/g, "<br/>").replace(/ /g, "&nbsp;");
    };

    var splitValue = function(value, escape, cursor) {
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
            slice = length - cursor - 1 == index ? "<span class=\"cursor\">"
                    + slice + "</span>" : slice;
            word += slice + "<wbr></wbr>";
        }

        if (cursor == -1) {
            word += "<span class=\"cursor\">&nbsp;</span>"
        }

        return word;
    };

    var refresh = function() {
        var value = jQuery(".console").data("text") || "";
        var scrollHeight = jQuery(".console")[0].scrollHeight;
        var cursor = jQuery(".console").data("cursor");
        word = splitValue(value, true, cursor);
        jQuery(".console .line").html(word);
        jQuery(".console").scrollTop(scrollHeight);
        autocomplete();
    };

    /**
     * Clears the contents of the console, this should include the current line,
     * the previous lines and the text field. At the end of the execution the
     * console is refreshed.
     */
    var clear = function() {
        jQuery(".console").data("text", "");
        jQuery(".console").data("cursor", -1);
        jQuery(".console .text").val("");
        jQuery(".console .line").empty();
        jQuery(".console .previous").empty();
        refresh();
    };

    var autocomplete = function() {
        // retrieves the current console command in execution
        // to retrieve the associated autocomplete value
        var command = jQuery(".console").data("text");

        jQuery.ajax({
                    url : "console/autocomplete",
                    data : {
                        command : command,
                        instance : jQuery(".console").data("instance")
                    },
                    success : function(data) {
                        // unpacks the resulting json data into the result
                        // and the instance part, so that they may be used
                        // in the processing of the results
                        var result = data["result"];
                        var instance = data["instance"];

                        // retrieves the autocomplete list item and clears
                        // all of its items (component reset)
                        var list = jQuery(".console .autocomplete ul");
                        list.empty();

                        // iterates over all the values to be inserted into
                        // the autocomplete options list
                        for (var index = 0; index < result.length; index++) {
                            // retrieves the current value in iteration to
                            // adds it to the options list
                            var value = result[index];

                            // retrieves the highlight and the remainder part
                            // of the value using the command length as base
                            var highlight = value.slice(0, command.length);
                            var remainder = value.slice(command.length);

                            // creates the new item with both the highlight and
                            // the remaind part and adds it to the list of options
                            list.append("<li><span class=\"high\">" + highlight
                                    + "</span>" + remainder + "</li>");
                        }

                        // sets the instance (identifier) value in the console
                        // for latter usage of the value
                        jQuery(".console").data("instance", instance);

                        // sets the first child of the autocomplete list as the
                        // currently selected child element
                        jQuery(":first-child", list).addClass("selected");
                    }
                });

    };

    /**
     * Processes one command from the current console queue in case there's at
     * least one command there. The order of execution is first in first out
     * (fifo) and one command is executed then only after the return from the
     * server side is completed the next command is executed.
     */
    var process = function() {
        // tries to retrieve the command queue and checks if it's empty
        // in such case must return immediately
        var commands = jQuery(".console").data("commands") || [];
        if (commands.length == 0) {
            return;
        }

        // retrieves the current command and then retrives the remaining
        // parts of the commands queue
        var value = commands[0];
        var next = commands[1] || "";
        command = jQuery.trim(value);
        commands = commands.slice(1);
        jQuery(".console").data("commands", commands);

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

                // trims the resulting value to avoid any possible extra
                // newline values (typical for some interpreters)
                result = jQuery.trim(result);

                // sets the instance (identifier) value in the console
                // for latter usage of the value
                jQuery(".console").data("instance", instance);

                // resets the element value (virtual value) and clear the
                // console line (to the original value)
                jQuery(".console").data("text", next);
                jQuery(".console .line").html("<span class=\"cursor\">&nbsp;</span>");

                // resets the cursor position to the top right most position
                // of the current line in printing
                jQuery(".console").data("cursor", -1);

                jQuery(".console .previous").append("<div><span class=\"prompt\"># </span><span>"
                        + splitValue(value, true) + "</span></div>");
                var resultLine = jQuery("<span></span>");

                var line = splitValue(result, true);
                jQuery(".console .previous").append("<div>" + line + "</div>");
                jQuery(".console").scrollTop(jQuery(".console")[0].scrollHeight);

                var history = jQuery(".console").data("history") || [];

                // checks if the current value to be inserted
                // into the history is not equal to the one already
                // present at the top of the history only in that
                // situation shall the value be inserted in history
                if (value != history[history.length - 1]) {
                    history.push(value);
                }
                jQuery(".console").data("history", history);
                jQuery(".console").data("history_index", 0);

                // runs the process command again to continue the processing
                // of the current queue
                process();
            }
        });
    };

    // initializes the cursor position at the end
    // of the console line (initial position)
    jQuery(".console").data("cursor", -1);

    // resets the console text to avoid any possible auto
    // complete operation
    jQuery(".console .text").val("");

    // "clicks" in the console so that the focus is started
    // at the console (immediate interaction)
    jQuery(".console").click();
});
