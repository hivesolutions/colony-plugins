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

(function($) {
    jQuery.fn.uxconsole = function(query, callback, options) {
        // the offset in pixels of the autocomplete
        // window relative to the console line
        var AUTOCOMPLETE_OFFSET = 2;

        // the basic commands of the console to be
        // executed at the client side
        var COMMANDS = ["clear", "fullscreen", "window"];

        // the default values for the data query
        var defaults = {};

        // sets the default options value
        var options = options ? options : {};

        // constructs the options
        var options = jQuery.extend(defaults, options);

        // sets the jquery matched object
        var matchedObject = this;

        /**
         * Initializer of the plugin, runs the necessary functions to initialize
         * the structures.
         */
        var initialize = function() {
            _appendHtml();
            _registerHandlers();
        };

        /**
         * Creates the necessary html for the component.
         */
        var _appendHtml = function() {
            // retrievs the text area for the interaction with
            // the console
            var text = jQuery(".text", matchedObject);

            // initializes the cursor position at the end
            // of the console line (initial position)
            matchedObject.data("cursor", -1);

            // resets the console text to avoid any possible auto
            // complete operation
            text.val("");

            // iterates over each of the matched object to start "their"
            // console structures
            matchedObject.each(function(index, element) {
                        // retrieves the current element
                        var _element = jQuery(this);

                        // initializes the console by requesting the initial instace
                        // from the client side (initialization scripts should be
                        // executed at this stage)
                        init(_element);
                    });
        };

        /**
         * Registers the event handlers for the created objects.
         */
        var _registerHandlers = function() {
            // retrieves the reference to the global wide
            // window object
            var __window = jQuery(window);

            // retrieves the text area associated with the
            // matched object (console)
            var text = jQuery(".text", matchedObject);

            // retrieves the reference to the autocomplete
            // component of the console
            var _autocomplete = jQuery(".autocomplete", matchedObject);

            // registers for the click event in the console to
            // propagate the focus event to the text area
            matchedObject.click(function() {
                        // retrieves the current element and the associated
                        // text area (from the console) and the autocomplete
                        // display area
                        var element = jQuery(this);
                        var text = jQuery(".text", element);
                        var autocomplete = jQuery(".autocomplete", element);

                        // focus the activity in the text area of the console
                        // and hides the autocomplete
                        text.focus();
                        autocomplete.hide();
                    });

            matchedObject.bind("dragenter", function(event) {
                        // retrieves the current element and
                        // adds the drag class to it (styling
                        // of the element structure)
                        var element = jQuery(this);
                        element.addClass("drag");
                    });

            matchedObject.bind("dragover", function(event) {
                        // retrieves the current element and
                        // adds the drag class to it (styling
                        // of the element structure)
                        var element = jQuery(this);
                        element.addClass("drag");
                    });

            matchedObject.bind("dragleave", function(event) {
                        // retrieves the current element and
                        // removes the drag class to it (styling
                        // of the element structure)
                        var element = jQuery(this);
                        element.removeClass("drag");
                    });

            matchedObject.bind("drop", function(event) {
                        // retrieves the current element and
                        // removes the drag class to it (styling
                        // of the element structure)
                        var element = jQuery(this);
                        element.removeClass("drag");

                        // prevents the default event (avoids browser showing
                        // the file in raw mode)
                        event.preventDefault();

                        // retrieves the first file and create a new file
                        // reader object to handle the loading of the file
                        var dataTransfer = event.originalEvent.dataTransfer;
                        var file = dataTransfer.files[0];
                        reader = new FileReader();
                        reader.onload = function(event) {
                            // retrieves the provided text value from
                            // the event to be processed by the console
                            // then replaces the windows style newlines
                            // with the basic unix styled ones
                            var value = event.target.result;
                            value = value.replace(/\r\n/g, "\n");

                            // retrieves the current console commands and appends
                            // the complete file value into it (for execution) then
                            // puts the commands value back into the console
                            var _commands = element.data("commands") || [];
                            _commands.push(value);
                            element.data("commands", _commands);

                            // runs the process command on the console and waits for the
                            // response to print the newline with the information regarding
                            // the execution of the file
                            process(element, true, file.name, function(result) {
                                        newline(element, "load " + file.name,
                                                "", result);
                                    });
                        };
                        reader.readAsText(file);

                        // stops the event propagation to avoid any possible
                        // problem with upper handlers
                        event.stopPropagation();
                        event.stopImmediatePropagation();
                    });

            text.keydown(function(event) {
                // retrieves the current element, the parent console
                // element and automplete panel
                var element = jQuery(this);
                var console = element.parents(".console");
                var _autocomplete = jQuery(".autocomplete", console);

                // retrieves the text currently in used for the context
                // of the console (current command)
                var value = console.data("text") || "";

                // retrieves the key value
                var keyValue = event.keyCode ? event.keyCode : event.charCode
                        ? event.charCode
                        : event.which;

                // sets the default value for the canceling operation
                // (no default behavior) as true (most of the times)
                var cancel = true;

                if (event.ctrlKey) {
                    switch (keyValue) {
                        case 32 :
                            autocomplete(console, true);
                            break;

                        default :
                            break;
                    }
                }

                if (event.shiftKey) {
                    switch (keyValue) {
                        case 70 :
                            // checks if the current console is currently displayed
                            // in fullscreen and then checks if the autocomplete box
                            // is visible
                            var isFullscreen = console.hasClass("fullscreen");
                            var isAutocompleteVisible = _autocomplete.is(":visible");

                            // in case the current mode is fullscreen, changes to the
                            // window model otherwise changes to fullscreen, then in
                            // case the autocomplete window is shows runs the layout
                            // update in it using the autocomplete function
                            isFullscreen
                                    ? _window(console)
                                    : fullscreen(console);
                            isAutocompleteVisible
                                    && autocomplete(console, true);

                            // prevents the default event to avoid unwanted behavior
                            event.preventDefault();

                            // breaks the swith
                            break;
                    }
                }

                switch (keyValue) {
                    case 8 :
                        // prevents the default behavior for the backspace
                        // key because it would focus the window on the text area
                        event.preventDefault();

                        var cursor = console.data("cursor");
                        if (cursor == value.length - 1) {
                            break;
                        }

                        var first = value.slice(0, value.length - cursor - 2);
                        var second = value.slice(value.length - cursor - 1,
                                value.length);
                        var value = first + second;
                        console.data("text", value)

                        refresh(console);
                        break;

                    case 9 :
                        // prevents the default behavior for the tab key
                        // to avoid the focus from jumping to a different element
                        event.preventDefault();

                        // checks if the autocomplete window is visible and in case
                        // it is flushes the currently selected autocomplete option
                        // to the console (autocomplete selection)
                        var isVisible = _autocomplete.is(":visible");
                        if (isVisible) {
                            flushAutocomplete(console);
                            break;
                        }

                        // retrieves the console cursor position and adds a sequence
                        // of four spaces between the current parts of the values
                        // then updates the text value of the console
                        var cursor = console.data("cursor");
                        var first = value.slice(0, value.length - cursor - 1);
                        var second = value.slice(value.length - cursor - 1,
                                value.length);
                        var value = first + "    " + second;
                        console.data("text", value)

                        // refreshs the console layout to update the console
                        // text value and other structures
                        refresh(console);
                        break;

                    case 27 :
                        // hides the autocomplete panel, cancelation operation
                        // occurred (should take effect immediately)
                        _autocomplete.hide();
                        break;

                    case 32 :
                        // hides the autocomplete panel, cancelation operation
                        // occurred (should take effect immediately)
                        _autocomplete.hide();
                        cancel = false;
                        break;

                    case 33 :
                        // checks if the autocomplete panel is currently visible
                        // for such situations the currently selected item in it
                        // should be replaced by the first one (page up)
                        var isVisible = _autocomplete.is(":visible");
                        if (isVisible) {
                            // retrieves the currently selected item and removes the
                            // selected class from it
                            var selected = jQuery("ul > li.selected",
                                    _autocomplete);
                            selected.removeClass("selected");

                            // retrieves the target element (first element) and selects
                            // it by adding the selected class and ensuring its visibility
                            // then "selects" the autocomplete to update the tooltip
                            var target = jQuery("ul > li:first-child",
                                    _autocomplete);
                            target.addClass("selected");
                            ensureVisible(target, _autocomplete);
                            selectAutocomplete();

                            // prevernts the default behavior (avoids the top level window
                            // from moving, expected behavior)
                            event.preventDefault();

                            // breaks the switch
                            break;
                        }

                        // breaks the switch
                        break;

                    case 34 :
                        // checks if the autocomplete panel is currently visible
                        // for such situations the currently selected item in it
                        // should be replaced by the last one (page down)
                        var isVisible = _autocomplete.is(":visible");
                        if (isVisible) {
                            // retrieves the currently selected item and removes the
                            // selected class from it
                            var selected = jQuery("ul > li.selected",
                                    _autocomplete);
                            selected.removeClass("selected");

                            // retrieves the target element (last element) and selects
                            // it by adding the selected class and ensuring its visibility
                            // then "selects" the autocomplete to update the tooltip
                            var target = jQuery("ul > li:last-child",
                                    _autocomplete);
                            target.addClass("selected");
                            ensureVisible(target, _autocomplete);
                            selectAutocomplete();

                            // prevernts the default behavior (avoids the top level window
                            // from moving, expected behavior)
                            event.preventDefault();

                            // breaks the switch
                            break;
                        }

                        // breaks the switch
                        break;

                    case 35 :
                        // updates the cursor position to the rightmost position
                        // (end operation) and then refreshs the console layout
                        // to update the console text value and other structures
                        console.data("cursor", -1);
                        refresh(console);
                        break;

                    case 36 :
                        // updates the cursor position to the leftmost position
                        // (end operation) and then refreshs the console layout
                        // to update the console text value and other structures
                        console.data("cursor", value.length - 1);
                        refresh(console);
                        break;

                    case 37 :
                        // retrieves the current cursor position in order
                        // to move it to the left, in case the position is the
                        // last breaks the switch (nothing to be done)
                        var cursor = console.data("cursor");
                        if (cursor == value.length - 1) {
                            break;
                        }

                        // increments the cursor position (moves it to the left)
                        // and updates the value in the console data
                        cursor++;
                        console.data("cursor", cursor);

                        // refreshs the console layout to update the console
                        // text value and other structures
                        refresh(console);
                        break;

                    case 38 :
                        // checks if the autocomplete panel is currently visible
                        // for such situations the currently selected item in it
                        // should be replaced by the previous one (move down)
                        var isVisible = _autocomplete.is(":visible");
                        if (isVisible) {
                            // retrieves the currently selected item and in case
                            // it's the first element returns immediately, can't
                            // move it up from that position
                            var selected = jQuery("ul > li.selected",
                                    _autocomplete);
                            if (selected.is(":first-child")) {
                                return;
                            }

                            // removes the selected class from the selected element
                            // and retrieves its index position
                            selected.removeClass("selected");
                            var selectedIndex = selected.index();

                            // retrieves the target element (previous element) and selects
                            // it by adding the selected class and ensuring its visibility
                            // then "selects" the autocomplete to update the tooltip
                            var target = jQuery("ul > li:nth-child("
                                            + (selectedIndex) + ")",
                                    _autocomplete);
                            target.addClass("selected");
                            ensureVisible(target, _autocomplete);
                            selectAutocomplete();

                            // breaks the switch
                            break;
                        }

                        // retrieves the current history list and the current index
                        // for the history, going to be used to update the text
                        var history = console.data("history") || [];
                        var historyIndex = console.data("history_index") || 0;

                        // retrieves the current (text) value from the history list
                        // and then increments the index (pointer) for the history
                        var value = history[history.length - historyIndex - 1];
                        if (historyIndex != history.length - 1) {
                            historyIndex++;
                        }

                        // updates the console data information for the "new" text
                        // value and for the history index
                        console.data("text", value)
                        console.data("history_index", historyIndex)

                        // refreshs the console layout to update the console
                        // text value and other structures
                        refresh(console);
                        break;

                    case 39 :
                        // retrieves the current cursor position in order
                        // to move it to the right, in case the position is the
                        // last breaks the switch (nothing to be done)
                        var cursor = console.data("cursor");
                        if (cursor == -1) {
                            break;
                        }

                        // decrements the cursor position (moves it to the right)
                        // and updates the value in the console data
                        cursor--;
                        console.data("cursor", cursor);

                        // refreshs the console layout to update the console
                        // text value and other structures
                        refresh(console);
                        break;

                    case 40 :
                        // checks if the autocomplete panel is currently visible
                        // for such situations the currently selected item in it
                        // should be replaced by the next one (move down)
                        var isVisible = _autocomplete.is(":visible");
                        if (isVisible) {
                            // retrieves the currently selected item and in case
                            // it's the last element returns immediately, can't
                            // move it down from that position
                            var selected = jQuery("ul > li.selected",
                                    _autocomplete);
                            if (selected.is(":last-child")) {
                                return;
                            }

                            // removes the selected class from the selected element
                            // and retrieves its index position
                            selected.removeClass("selected");
                            var selectedIndex = selected.index();

                            // retrieves the target element (next element) and selects
                            // it by adding the selected class and ensuring its visibility
                            // then "selects" the autocomplete to update the tooltip
                            var target = jQuery("ul > li:nth-child("
                                            + (selectedIndex + 2) + ")",
                                    _autocomplete);
                            target.addClass("selected");
                            ensureVisible(target, _autocomplete);
                            selectAutocomplete();

                            // breaks the switch
                            break;
                        }

                        // retrieves the current history list and the current index
                        // for the history, going to be used to update the text
                        var history = console.data("history") || [];
                        var historyIndex = console.data("history_index") || 0;

                        // retrieves the current (text) value from the history list
                        // and then decrements the index (pointer) for the history
                        var value = history[history.length - historyIndex];
                        if (historyIndex != 0) {
                            historyIndex--;
                        }

                        // updates the console data information for the "new" text
                        // value and for the history index
                        console.data("text", value)
                        console.data("history_index", historyIndex)

                        // refreshs the console layout to update the console
                        // text value and other structures
                        refresh(console);
                        break;

                    case 46 :
                        // prevents the default behavior for the delete
                        // key because it would focus the window on the text area
                        event.preventDefault();

                        // retrieves the currently set cursor from the console
                        // and in case it's not set breaks immediately
                        var cursor = console.data("cursor");
                        if (cursor == -1) {
                            break;
                        }

                        // retrieves the firt and second part of the current line
                        // and removes a character at the position of the cursor
                        // this should be able to replicate the delete "effect"
                        var first = value.slice(0, value.length - cursor - 1);
                        var second = value.slice(value.length - cursor,
                                value.length);
                        var value = first + second;

                        // updates the text (value) in the console and "moves" the
                        // cursor one position
                        console.data("text", value)
                        console.data("cursor", cursor - 1)

                        // refreshs the console layout to update the console
                        // text value and other structures
                        refresh(console);
                        break;

                    default :
                        cancel = false;
                        break;
                }

                // updates the cancel data attribute in the
                // console to provide information to the hadling
                // of the key pressing in the next event
                console.data("cancel", cancel)

                // stops the event propagation this should be able
                // to avoid possible problems with double handling
                event.stopPropagation();
                event.stopImmediatePropagation();
            });

            text.bind("paste", function(event) {
                // retrieves the element and the parent console
                var element = jQuery(this);
                var console = element.parents(".console");

                // sets a timeout so that the complete paste data
                // is set in the text area (deferred event)
                setTimeout(function() {
                            // retrieves the current value of the element and clears
                            // the contents of the text element to avoid  any duplicate
                            // paste operation (unwanted behavior)
                            var character = element.val();
                            element.val("");

                            // retrieves the current console text to be able to be used
                            // as teh base data for the paste operation
                            var text = console.data("text") || "";

                            // adds the new character into the text buffer
                            // by slicing the value around the current position,
                            // then joins the value back with the character
                            var cursor = console.data("cursor");
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
                                var _commands = console.data("commands") || [];
                                for (var index = 0; index < commands.length; index++) {
                                    _commands.push(commands[index]);
                                }
                                console.data("commands", _commands);
                                process(console);
                            }

                            // updates the text value of the console and refreshes
                            // the visual part of it
                            var value = commands[commands.length - 1];
                            console.data("text", value);
                            refresh(console);
                        }, 0);
            });

            text.keypress(function(event) {
                        // retrieves the element and the parent console
                        var element = jQuery(this);
                        var console = element.parents(".console");
                        var _autocomplete = jQuery(".autocomplete", console);

                        // retrieves the key value
                        var keyValue = event.keyCode
                                ? event.keyCode
                                : event.charCode ? event.charCode : event.which;

                        // retrieves the valid key code and converts it into
                        // a character value, then retrieves the current text
                        // and cancel value from the console
                        var keyCode = event.keyCode || event.which;
                        var character = String.fromCharCode(keyCode);
                        var text = console.data("text") || "";
                        var cancel = console.data("cancel") || false;

                        // in case the cancel flag is set the key press must
                        // be ignored and the call returned immediately
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
                                // checks if the autocomplete window is visible and in case
                                // it is flushes the currently selected autocomplete option
                                // to the console (autocomplete selection)
                                var isVisible = _autocomplete.is(":visible");
                                if (isVisible) {
                                    flushAutocomplete(console);
                                    break;
                                }

                                var value = console.data("text") || "";

                                switch (value) {
                                    case "clear" :
                                        // clears the current console display removing the various
                                        // information contained in it
                                        clear(console, true);
                                        event.preventDefault();

                                        // breaks the switch
                                        break;

                                    case "fullscreen" :
                                        // puts the current console window into the fullscreen mode
                                        // this action should change the current body and window status
                                        // so it should be used carefully to avoid side effects
                                        fullscreen(console);
                                        clear(console, false);
                                        event.preventDefault();

                                        // breaks the switch
                                        break;

                                    case "window" :
                                        // puts the current console window into the window mode
                                        // this action should change the current body and window status
                                        // so it should be used carefully to avoid side effects
                                        _window(console);
                                        clear(console, false);
                                        event.preventDefault();

                                        // breaks the switch
                                        break;

                                    default :
                                        // runs the process of the "remote" command this should trigger
                                        // the execution of the server side execution
                                        var commands = console.data("commands")
                                                || [];
                                        commands.push(value);
                                        console.data("commands", commands)
                                        process(console);

                                        // breaks the switch
                                        break;
                                }

                                // breaks the switch
                                break;

                            default :
                                // adds the new character into the text buffer
                                // by slicing the value around the current position,
                                // then joins the value back with the character
                                var cursor = console.data("cursor");
                                var first = text.slice(0, text.length - cursor
                                                - 1);
                                var second = text.slice(text.length - cursor
                                                - 1, text.length);
                                var value = first + character + second;

                                // updates the text value of the console and refreshes
                                // the visual part of it, note that the autocomplete
                                // is only run in case the character is not a space
                                console.data("text", value);
                                refresh(console);
                                character != " " && autocomplete(console, true);

                                // breaks the switch
                                break;
                        }

                        // stops the event propagation and prevents the default
                        // behavior (no printing in the text area)
                        event.stopPropagation();
                        event.stopImmediatePropagation();
                        event.preventDefault();
                    });

            text.focus(function() {
                        // retrieves the current element and uses it to retrieve
                        // the parent console element
                        var element = jQuery(this);
                        var console = element.parents(".console");

                        // adds the focus class to the console element
                        console.addClass("focus");
                    });

            text.blur(function() {
                        // retrieves the current element and uses it to retrieve
                        // the parent console element, then uses it to retrieve
                        // the reference to the autocomplete panel element
                        var element = jQuery(this);
                        var console = element.parents(".console");
                        var _autocomplete = jQuery(".autocomplete", console);

                        // removes the focus class from the console and hides the
                        // autocomplete panel
                        console.removeClass("focus");
                        _autocomplete.hide();
                    });

            __window.scroll(function() {
                        // hides the autocomplete panel to avoid problems with
                        // outdated positions
                        _autocomplete.hide();
                    });
        };

        var escapeHtml = function(value) {
            return value.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(
                    />/g, "&gt;").replace(/\n/g, "<br/>").replace(/ /g,
                    "&nbsp;");
        };

        var splitValue = function(value, escape, cursor) {
            // in case there is no value defined there is no need
            // to split because there is no definition of it
            if (value == null) {
                return value;
            }

            // starts the list to hold the various character slices and
            // then retrieves the length of the value to be used durring
            // the iteration for value slicing
            var slices = [];
            var length = value.length;

            // iterates over the length of the value (string) to populate
            // the list of slices with all the value characters
            for (var index = 0; index < length; index += 1) {
                var slice = value.slice(index, index + 1);
                slices.push(slice);
            }

            // starts the strings that will hold both the world and
            // the (temporary) slices and then retrieves the size of
            // the slices list to be used in the iteration
            var word = "";
            var slice = "";
            var sliceLength = slices.length;

            // iterates over all the slices to escape their values and
            // set the cursor position (if defined)
            for (var index = 0; index < sliceLength; index++) {
                // escapes the slice value, then adds the cursor tag
                // (in case it's set) and then appends the word break tag
                // into the final value to be appended to the word
                slice = escape ? escapeHtml(slices[index]) : slices[index];
                slice = length - cursor - 1 == index
                        ? "<span class=\"cursor\">" + slice + "</span>"
                        : slice;
                word += slice + "<wbr></wbr>";
            }

            // in case the cursor is not set (invalid) adds the cursor
            // to the end of the word
            if (cursor == -1) {
                word += "<span class=\"cursor\">&nbsp;</span>"
            }

            // returns the final word with all the characters separated
            // with word break tags (for word breaking)
            return word;
        };

        var refresh = function(console) {
            // retrieves the current line element assciated with
            // the console to update its value
            var line = jQuery(".line", console);

            // retrieves the current console text value or default
            // to an empty string then retrieves the current cursor
            // position
            var value = console.data("text") || "";
            var cursor = console.data("cursor");

            // retrieves the scroll height value from the console
            // to be used to scroll the console to the bottom
            var scrollHeight = console[0].scrollHeight;

            // splits the value into the appropriate word representation
            // and used it to set the line html value
            var word = splitValue(value, true, cursor);
            line.html(word);

            // scrolls the current console to the bottom position and
            // runs the autocomplete processing operation, avoiding the
            // processing of data in case no autocomplete is visible
            // (avoids excessive remote calls)
            console.scrollTop(scrollHeight);
            autocomplete(console, false);
        };

        /**
         * Clears the contents of the console, this should include the current
         * line, the previous lines and the text field. At the end of the
         * execution the console is refreshed.
         *
         * @param {Element}
         *            console The reference to the console element to be used as
         *            target for the clear operation.
         * @param {Boolean}
         *            complete If the clearing of the consol should be complete
         *            (previous elements removed) or if only the current line is
         *            to be removed.
         */
        var clear = function(console, complete) {
            // retrieves the various text related elements from
            // the console, to be used to clear their values
            var text = jQuery(".text", console);
            var line = jQuery(".line", console);
            var previous = jQuery(".previous", console);

            // resets the text and cursor value in te console
            // data to the original values
            console.data("text", "");
            console.data("cursor", -1);

            // updates the element values to the original values
            // (visual clear operation)
            text.val("");
            line.empty();
            complete && previous.empty();

            // refreshes the console layout to reflect the
            // changes in the console structure
            refresh(console);
        };

        var joinResult = function(token, result) {
            // iterates over all the commands and tries to find the
            // ones that match the required token string start
            for (var index = 0; index < COMMANDS.length; index++) {
                // retrieves the current command and check if it starts
                // with the provided token in case it does adds it to
                // the result list (set)
                var current = COMMANDS[index];
                var offset = current.indexOf(token);
                if (offset != 0) {
                    continue;
                }
                result.push([current, "command"]);
            }
        };

        var autocomplete = function(console, force) {
            // retrieves the reference to both the text and line
            // elements of the console structure
            var text = jQuery(".text", console);
            var line = jQuery(".line", console);

            // retrieves the reference to the autocomplete panel
            // of the console
            var _autocomplete = jQuery(".autocomplete", console);

            // checks if the autocomplete window is currently visible
            // in case it's not and the force flag is not set avoid
            // the processing of the autocomplete elements
            var isVisible = _autocomplete.is(":visible");
            if (!force && !isVisible) {
                return;
            }

            // retrieves the token structure and uses it to retrieve
            // the currently selected token (selected word)
            var tokenStructure = getToken(console);
            var token = tokenStructure[0];

            // runs the remove query to retrieve the various autcomplete
            // results (this query is meant to be fast 100ms maximum)
            jQuery.ajax({
                type : "post",
                url : "console/autocomplete",
                data : {
                    command : token,
                    instance : console.data("instance")
                },
                success : function(data) {
                    // retrieves the element reference to the global
                    // window object
                    var _window = jQuery(window);

                    // unpacks the resulting json data into the result
                    // and the instance part, so that they may be used
                    // in the processing of the results
                    var result = data["result"];
                    var offset = data["offset"];
                    var instance = data["instance"];

                    // joins the received result set with the local commands
                    // set so that the local commands may also appear in the
                    // autocomplete list
                    joinResult(token, result);

                    // retrieves the autocomplete list item and clears
                    // all of its items (component reset)
                    var list = jQuery("ul", _autocomplete);
                    list.empty();

                    // iterates over all the values to be inserted into
                    // the autocomplete options list
                    for (var index = 0; index < result.length; index++) {
                        // retrieves the current value in iteration to
                        // add it to the options list, then unpacks it into
                        // name and the type part of the "tuple"
                        var value = result[index];
                        var name = value[0];
                        var type = value[1];
                        var options = value[2];

                        // retrieves the highlight and the remainder part
                        // of the name using the command length as base
                        var highlight = name.slice(0, token.length - offset);
                        var remainder = name.slice(token.length - offset);

                        // creates the new item with both the highlight and
                        // the remaind part and adds it to the list of options
                        var item = jQuery("<li class=\"" + type
                                + "\"><span class=\"high\">" + highlight
                                + "</span>" + remainder + "</li>");
                        list.append(item);
                        item.data("options", options);
                    }

                    // sets the instance (identifier) value in the console
                    // for latter usage of the value
                    console.data("instance", instance);

                    // sets the first child of the autocomplete list as the
                    // currently selected child element
                    jQuery(":first-child", list).addClass("selected");

                    // forces the display of the autocomplete in case there
                    // are results available otherwise hides the autocomplete
                    // list (no need to display the result)
                    result.length ? _autocomplete.show() : _autocomplete.hide();

                    // in case there are no results to be displayed no additional
                    // processing should occur (not significant) returns immediately
                    if (!result.length) {
                        return;
                    }

                    // calculates the offset to the top of the screen based
                    // on the current line position and offset to the top,
                    // then scrolls the autocomplete scrolling back the top
                    // (considered to be the original position)
                    var offsetTop = line.offset().top + line.outerHeight();
                    _autocomplete.css("top", offsetTop + "px");
                    _autocomplete.scrollTop(0);

                    // retrieves the current token structure and uses it to
                    // retrieve the start index of the token (for autocomplete
                    // box positioning)
                    var tokenStructure = getToken(console);
                    var startIndex = tokenStructure[1];

                    // retrieves the size of the font currently being used for the
                    // text and converts it into an integer value then uses it to
                    // calculate the offset to be used in the autocomplete
                    var fontSize = text.css("font-size");
                    fontSize = parseInt(fontSize);
                    _autocomplete.css("margin-left",
                            (startIndex * fontSize + 24) + "px");

                    // retrieves the current window scroll top position to be used
                    // as offset for the position of the autocomplete panel
                    var windowScroll = _window.scrollTop();
                    var marginTop = AUTOCOMPLETE_OFFSET - windowScroll;

                    // updates the autocomplete window margin so that the window is
                    // displayed bellow the current line and then checks if it's
                    // visible, in case it's not it must be placed above the line
                    _autocomplete.css("margin-top", marginTop + "px");
                    var isVisible = checkVisible(_autocomplete, _window);

                    // calculates the margin top position to be used to place
                    // the autocomplete window above the current line and then
                    // in case the window is not visible places in such
                    // place (notice the minus sign in the margin)
                    var aboveMargin = _autocomplete.outerHeight()
                            + line.outerHeight() + AUTOCOMPLETE_OFFSET
                            + windowScroll;
                    if (isVisible) {
                        _autocomplete.removeClass("above");
                    } else {
                        _autocomplete.addClass("above");
                        _autocomplete.css("margin-top", (aboveMargin * -1)
                                        + "px");
                    }

                    // selects the autocomplete item, this should trigger the
                    // placement of the tooltip window at the appropriate side
                    selectAutocomplete();
                }
            });

        };

        String.prototype.trim = function() {
            return this.replace(/^\s+|\s+$/g, "");
        }
        String.prototype.ltrim = function() {
            return this.replace(/^\s+/, "");
        }
        String.prototype.rtrim = function() {
            return this.replace(/\s+$/, "");
        }

        /**
         * Processes one command from the current console queue in case there's
         * at least one command there. The order of execution is first in first
         * out (fifo) and one command is executed then only after the return
         * from the server side is completed the next command is executed.
         *
         * @param {Element}
         *            console The refernece to the console element to be used in
         *            the processing of he command.
         * @param {Boolean}
         *            silent Flag that controls if the processing of the command
         *            should generate console output.
         * @param {String}
         *            name The name of the file representing the command to be
         *            executed, this value should null in case the command was
         *            created by a console.
         * @param {Function}
         *            callback The callback function to be called at the end of
         *            each command processed durring this process call.
         */
        var process = function(console, silent, name, callback) {
            // tries to retrieve the command queue and checks if it's empty
            // in such case must return immediately
            var commands = console.data("commands") || [];
            if (commands.length == 0) {
                return;
            }

            // retrieves the currently pending data to be flushed to the
            // server side (important for multiple line commands)
            var _pending = console.data("pending") || "";

            // retrieves the current command and then retrives the remaining
            // parts of the commands queue
            var value = commands[0];
            var next = commands[1] || "";
            var command = value.rtrim();
            commands = commands.slice(1);
            console.data("commands", commands);

            // checks if the current command refers a file oriented value
            // (contains multiple lines) or if it's just a single command line
            // in case the name is defined this the commands are considered
            // to be originated from a file
            var file = name ? 1 : 0;

            // in case there is pendind data to be sent and the command is not
            // empty (end of pending operation) must delay command processing
            if (_pending && command) {
                newline(console, value, next, "", _pending + "\n" + value, true);
                process(console, silent, name, callback);
                return;
            }

            // updates the command value by prepending the pending part
            // of the command to the command itself (this will allow for
            // complete execution of the previous lines)
            command = _pending + "\n" + command;

            jQuery.ajax({
                        type : "post",
                        url : "console/execute",
                        data : {
                            command : command,
                            instance : console.data("instance"),
                            file : file,
                            name : name
                        },
                        success : function(data) {
                            // unpacks the resulting json data into the result
                            // and the instance part, so that they may be used
                            // in the processing and printing of the result
                            var result = data["result"];
                            var pending = data["pending"];
                            var instance = data["instance"];

                            // sets the instance (identifier) value in the console
                            // for latter usage of the value only in case the instance
                            // value is defined (otherwise leave as it is)
                            instance && console.data("instance", instance);

                            // in case the current processing mode is not silent
                            // must create a newline with the current context (verbose)
                            !silent
                                    && newline(console, value, next, result,
                                            command, pending);

                            // in case the callback is defined calls it with
                            // the resulting values from the client side
                            callback && callback(result, pending, instance);

                            // runs the process command again to continue the processing
                            // of the current queue
                            process(console, silent, name, callback);
                        }
                    });
        };

        var flushAutocomplete = function(console) {
            // retrieves the reference to the autocomplete element
            // contained inside the console
            var _autocomplete = jQuery(".autocomplete", console);

            // retrieves the currently selected autocomplete element and
            // then retrieves its value and its options map (in case one
            // is available)
            var selected = jQuery("ul > li.selected", _autocomplete);
            var text = selected.text();
            var options = selected.data("options") || {};

            // retrieves the current's console text and then retrieves
            // the token structure for the currrently selected text
            var _text = console.data("text") || "";
            var tokenStructure = getToken(console);

            // unpacks the token structure into the various components
            // of it, the token and the start and end indexes
            var token = tokenStructure[0];
            var startIndex = tokenStructure[1];
            var endIndex = tokenStructure[2];

            var tokenElements = token.split(".");
            var tokenElements = tokenElements.slice(0, tokenElements.length - 1);
            tokenElements.push(text);
            token = tokenElements.join(".")

            var start = _text.slice(0, startIndex);
            var end = _text.slice(endIndex);

            // in case there is an extra string value to be added to the token
            // adds it (this will appear at the front of the value)
            token += options["extra"] || "";

            call = false;

            // in case the currently selected item is a method or a function
            // extra care must be taken to provide the calling part
            if (selected.hasClass("method") || selected.hasClass("function")) {
                // appends the calling part of the line to the token
                // to provide calling shortcut
                token += "()";
                call = true;
            }

            // creates the final text value to be set in the line using
            // the start part the token and the (final) end part
            text = start + token + end;

            // calculates the new cursor position based on the partial
            // token values and the start string length and takes into
            // account the possible offset for the call situations
            var cursor = text.length
                    - (start.length + token.length + (call ? 0 : 1))

            console.data("text", text);
            console.data("cursor", cursor);
            _autocomplete.hide();
            refresh(console);
        };

        var newline = function(console, value, next, result, command, pending) {
            // retrieves the reference to a series of elements contained
            // inside the console
            var line = jQuery(".line", console);
            var previous = jQuery(".previous", console);
            var prompt = jQuery(".current .prompt", console);
            var _autocomplete = jQuery(".autocomplete", console);

            // recalculates the pending command value using the
            // pending flag as the guide for this operation and
            // then sets the new pending string in the console
            _pending = pending ? command : "";
            console.data("pending", _pending);

            // retrieves the value of the currently displayed prompt
            // as the previous prompt and "calculates" the value for
            // the next primpt string
            var previousPrompt = prompt.html();
            var _prompt = pending ? ". " : "# ";

            // trims the resulting value to avoid any possible extra
            // newline values (typical for some interpreters)
            result = result.rtrim();

            // resets the element value (virtual value) and clear the
            // console line (to the original value) and updates the
            // prompt value with the "calculated" one
            console.data("text", next);
            line.html("<span class=\"cursor\">&nbsp;</span>");
            prompt.html(_prompt);

            // resets the cursor position to the top right most position
            // of the current line in printing
            console.data("cursor", -1);

            // creates a new previous line and adds it to the previous container
            // this line will contain the values of the executed command
            previous.append("<div><span class=\"prompt\">" + previousPrompt
                    + "</span><span>" + splitValue(value, true)
                    + "</span></div>");

            // splits the result value (into the appropriate components) and
            // also adds it to the previous action container, then scrolls
            // the current console area to the lower part
            var line = splitValue(result, true);
            previous.append("<div>" + line + "</div>");
            console.scrollTop(console[0].scrollHeight);

            // retrieves the sequence object that contains the various
            // command strings that compose the history of the console
            var history = console.data("history") || [];

            // checks if the current value to be inserted
            // into the history is not equal to the one already
            // present at the top of the history only in that
            // situation shall the value be inserted in history
            if (value != history[history.length - 1]) {
                history.push(value);
            }
            console.data("history", history);
            console.data("history_index", 0);

            // hides the autocomplete window, no need to display
            // it durring the initial part of the line processing
            _autocomplete.hide();
        };

        var selectAutocomplete = function(console) {
            // retrieves the reference to the global wide window
            // element
            var _window = jQuery(window);

            // retrieves the current line from the console and the
            // reference to the autocomplete element
            var line = jQuery(".line", console);
            var _autocomplete = jQuery(".autocomplete", console);

            // retrieves the tooltip associated with the autocomplete
            // element and the various components of it
            var tooltip = jQuery(".tooltip", _autocomplete);
            var tooltipDoc = jQuery(".doc", tooltip);
            var tooltipParams = jQuery(".params", tooltip);
            var tooltipReturn = jQuery(".return", tooltip);

            // retrieves the currently selected autocomplete item to
            // be used for the selection process
            var selected = jQuery("ul > li.selected", _autocomplete);

            // retrieves the various options from the selected item defaulting
            // to the basic values in case of non existence
            var options = selected.data("options") || {};
            var doc = options["doc"] || "";
            var params = options["params"] || [];
            var _return = options["return"] || null;
            doc = doc.trim();

            // hides the tooltip window (default behavior) and in case there
            // is documentation string available returns immediately (not tooltip
            // will be shown for this case)
            tooltip.hide();
            if (!doc) {
                return;
            }

            // shows the tooltip window back to the screen to ensure visibility
            // of the it (documentation exists)
            tooltip.show();

            // sets the tooltip margin left position to the right of the tooltip
            // and with a small spacing
            var marginLeft = _autocomplete.outerWidth() + 4
            tooltip.css("margin-left", marginLeft);

            // retrieves the documentation element from the tooltip data and in
            // case the current documentation value to be set is different updates
            // the layout value accordingly, then saves the new value in teh data
            // in order to avoid unnecessary updates
            var _doc = tooltip.data("doc") || "";
            if (doc != _doc) {
                tooltipDoc.html(splitValue(doc, true));
            }
            tooltip.data("doc", doc);

            // retrieves the complete set of parameters from the tooltip
            // and only in case the current parameters are different the
            // the tooltip parameters are created (performance decision)
            var _params = tooltip.data("params") || [];
            if (params != _params) {
                // clears the tooltip parameters element in order to place
                // new parameter element in there
                tooltipParams.empty();

                // iterates over all the parameters to create it's strucutre
                // and add them to the tooltip parameters section
                for (var index = 0; index < params.length; index++) {
                    var param = params[index];
                    tooltipParams.append("<div class=\"param\"><span class=\"name\">"
                            + param[0]
                            + "</span>&nbsp;<span class=\"type\">("
                            + param[1]
                            + ")</span><br />&nbsp;&nbsp;<span class=\"description\">"
                            + splitValue(param[2], true) + "</span></div>")
                }
            }

            // updates the parameters list in the tooltip data to avoid
            // unnecessary layout updates
            tooltip.data("params", params);

            // retrieves the complete return value from the tooltip
            // and only in case the current return value is different the
            // the tooltip return value is created (performance decision)
            var __return = tooltip.data("return") || [];
            if (_return != __return) {
                // clears the tooltip return element in order to place
                // new return element in there
                tooltipReturn.empty();

                // in case the return value is valid creates the element
                // and adds it to the tooltip return element
                _return
                        && tooltipReturn.append("<div class=\"param\"><span class=\"name\">"
                                + _return[0]
                                + "</span>&nbsp;<span class=\"type\">("
                                + _return[1]
                                + ")</span><br />&nbsp;&nbsp;<span class=\"description\">"
                                + splitValue(_return[2], true)
                                + "</span></div>")
            }

            // updates the return value in the tooltip data to avoid
            // unnecessary layout updates
            tooltip.data("return", _return);

            // checks if the current autocomplete position is at
            // the above of the current baseline, in order to make
            // decisions about the relative position of the tooltip
            var isAbove = _autocomplete.hasClass("above");

            // retrieves both the autocomplete height, the tooltip
            // height and the autocomplete border botttom and uses
            // them to calculate the delta value for the tooltip
            var autocompleteHeight = _autocomplete.outerHeight();
            var tooltipHeight = tooltip.outerHeight();
            var borderBottom = parseInt(_autocomplete.css("border-bottom"));
            var delta = autocompleteHeight - tooltipHeight - borderBottom;

            // in case the delta value is less than zero it's considered
            // to be a valid delta otherwise set's it as null, then validates
            // again if the position is above the baseline and only in such
            // case the delta value is considered valid
            delta = delta < 0 ? delta : null;
            delta = isAbove ? delta : null;

            // updates the top margin of the tooltip with the "final" delta
            // value resulting from the validations
            tooltip.css("margin-top", delta);
        };

        var getToken = function(console) {
            // retrieves the current console command in execution
            // to retrieve the associated autocomplete value
            var command = console.data("text") || "";

            // retrieves the current cursor position and uses it to
            // try to find the index of the token to be used in the retrieval
            var cursor = console.data("cursor") || -1;
            for (var index = command.length - cursor - 2; index >= 0; index--) {
                if (command[index] != " ") {
                    continue;
                }
                break;
            }

            index++;

            // saves the current index position as the start index position
            // for the command (the reference to the first letter)
            var startIndex = index;

            for (var index = startIndex; index < command.length; index++) {
                if (command[index] != " ") {
                    continue;
                }
                break;
            }

            var endIndex = index;
            var token = command.slice(startIndex, endIndex);

            return [token, startIndex, endIndex];
        };

        var maximize = function(console) {
            // retrieves the window element to retrieve some
            // of its dimensions
            var _window = jQuery(window);

            // retrieves the html and body global elements
            // to be able to operate over them
            var _html = jQuery("html");
            var _body = jQuery("body");

            // removes the current overflow y scroll bar (avoids
            // duplicate scroll bar)
            _html.css("overflow-y", "hidden");

            // removes the complete set of margin and padding values
            // for the body element
            _body.css("margin", "0px 0px 0px 0px");
            _body.css("padding", "0px 0px 0px 0px");

            // retrieves both the window heigh and width dimensions
            // to be used in the console
            var windowHeight = _window.height();
            var windowWidth = _window.width();

            // updates the various console attributes to set it as
            // full occupying area of the window
            console.css("margin", "0px 0px 0px 0px");
            console.css("position", "absolute");
            console.css("top", "0px");
            console.css("left", "0px");
            console.height(windowHeight - 4);
            console.width(windowWidth - 8);

            // retrieves the scroll height from the console
            // and updates the console scroll position to
            // position it at the bottom
            var scrollHeight = console[0].scrollHeight;
            console.scrollTop(scrollHeight);
        };

        var minimize = function(console) {
            // retrieves the html and body global elements
            // to be able to operate over them
            var _html = jQuery("html");
            var _body = jQuery("body");

            // removes the overflow attribute from the html
            // element to restore it (show scroll)
            _html.css("overflow-y", null);

            // removes the margin and padding attributes from
            // the body element
            _body.css("margin", null);
            _body.css("padding", null);

            // removes the complete set of css attributes
            // from the console to restore the original size
            console.css("margin", null);
            console.css("position", null);
            console.css("top", null);
            console.css("left", null);
            console.css("height", null);
            console.css("width", null);

            // retrieves the scroll height from the console
            // and updates the console scroll position to
            // position it at the bottom
            var scrollHeight = console[0].scrollHeight;
            console.scrollTop(scrollHeight);
        };

        var fullscreen = function(console) {
            // retrieves the rerence to the autocomplete panel
            // for the console element
            var _autocomplete = jQuery(".autocomplete", console);

            // adds the fullscrren class to the console element
            // so that the specific style are applied to it
            console.addClass("fullscreen");

            // creates the function that will be used to update the
            // size of the console on a resize of the parent
            var resize = function(event) {
                // hides the autocomplete window so that no visual
                // disturbances are displayed as a result of the new size
                _autocomplete.hide();

                // refreshes the current console window to fill the
                // newly available space
                maximize(console);
            };

            // retrieves the window and registers the resize in
            // the window to update the console size
            var _window = jQuery(window);
            _window.resize(resize);

            // saves the resize function in the console to be latter
            // used in the unbind process of the window resize event
            console.data("resize", resize);

            // maximizes the current window to fill the currently
            // available space (in body)
            maximize(console);
        };

        var _window = function(console) {
            // removes the fullscreen class from the console element
            // to avoid unexpected visuals in the console
            console.removeClass("fullscreen");

            // retrieves the currently used resize function from the
            // console to be used in the unset of the event handler
            var resize = console.data("resize", resize);

            // retrieves the window and uses it to unbind the resize
            // event (currently set) from it
            var _window = jQuery(window);
            _window.unbind("resize", resize)

            // minimizes the console removing all the custom style
            // applied to the current environment
            minimize(console);
        };

        var checkVisible = function(element, parent) {
            // retrieves the various measures of the parent for the
            // partial calculus of the visibility status of the element
            var parentHeight = parent.height();
            var parentTop = parent.scrollTop();
            var parentBottom = parentTop + parentHeight;

            // retrieves the measures for the element in order to be able
            // to calculate its own visibility status
            var elementHeight = element.outerHeight();
            var elementTop = element.offset().top;
            var elementBottom = elementTop + elementHeight;

            // checks if the element is visible in the current context
            // and returns that result to the caller method
            var isVisible = elementBottom <= parentBottom
                    && elementTop >= parentTop;
            return isVisible;
        };

        var ensureVisible = function(element, parent) {
            // retrieves the various measures of the parent for the
            // partial calculus of the visibility status of the element
            var parentHeight = parent.height();
            var parentTop = parent.scrollTop();
            var parentBottom = parentTop + parentHeight;

            // retrieves the measures for the element in order to be able
            // to calculate its own visibility status
            var elementHeight = element.outerHeight();
            var elementTop = element.offset().top
                    - element.parent().offset().top;
            var elementBottom = elementTop + elementHeight;

            // checks if the element is visible in the current context
            // and in case it's retunrs immediately no need to change the
            // parent element to ensure visibility
            var isVisible = elementBottom <= parentBottom
                    && elementTop >= parentTop;
            if (isVisible) {
                return;
            }

            // calculates the signal using the relative position of the
            // element to determine if it should be negative or positive
            var signal = elementTop > parentTop ? 1 : -1;

            // calculates the (new) current scroll position base on the
            // signal (relative position) of the element in relation with
            // the current scroll position
            var current = signal == 1 ? elementTop
                    - (parentHeight - elementHeight) : elementTop;
            parent.scrollTop(current);
        };

        var init = function(console) {
            // retrieves the current and previous lines for the provided
            // console element reference
            var current = jQuery(".current", console);
            var previous = jQuery(".previous", console);

            // hides the current line, no input will be possible durring
            // the initial loading of the console
            current.hide();

            // runs the remove query to retrieve the various autcomplete
            // results (this query is meant to be fast 100ms maximum)
            jQuery.ajax({
                        type : "post",
                        url : "console/init",
                        success : function(data) {
                            // unpacks the resulting json data into the result
                            // and the instance part, so that they may be used
                            // in the processing of the results
                            var result = data["result"];
                            var instance = data["instance"];

                            // splits the result value (into the appropriate components) and
                            // also adds it to the previous action container, then scrolls
                            // the current console area to the lower part
                            var line = splitValue(result, true);
                            previous.append("<div>" + line + "</div>");
                            console.scrollTop(console[0].scrollHeight);

                            // sets the instance (identifier) value in the console
                            // for latter usage of the value
                            console.data("instance", instance);

                            // restores the current line display, because the loading is now
                            // considered complete
                            current.show();
                        }
                    });
        };

        // initializes the plugin
        initialize();

        // returns the object
        return this;
    };
})(jQuery);

jQuery(document).ready(function() {
            // starts the ux console plugin for the selected console
            // component (normal starting) then clicks in it to trigger
            // the immediate selection of the console
            var console = jQuery(".console");
            console.uxconsole();
            console.click();
        });
