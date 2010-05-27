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

// __author__    = Luís Martinho <lmartinho@hive.pt>
// __version__   = 1.0.0
// __revision__  = $LastChangedRevision$
// __date__      = $LastChangedDate$
// __copyright__ = Copyright (c) 2010 Hive Solutions Lda.
// __license__   = Hive Solutions Confidential Usage License (HSCUL)

/**
 * jQuery autocomplete plugin, this plugin provides auto complete functionality
 * to standard text fields.
 *
 * @name jquery-autocomplete.js
 * @author Luís Martinho <lmartinho@hive.pt>
 * @version 1.0
 * @date April 15, 2010
 * @category jQuery plugin
 * @copyright Copyright (c) 2010 Hive Solutions Lda.
 * @license Hive Solutions Confidential Usage License (HSCUL) -
 *          http://www.hive.pt/licenses/
 */
(function($) {
    $.fn.autocomplete = function(options) {
        var LEFT = 37;
        var UP = 38;
        var RIGHT = 39;
        var DOWN = 40;
        var ENTER = 13;

        // the default values for the menu
        var defaults = {
            showEffect : "fadeIn",
            hideEffect : "fadeOut",
            // by default changes to the target contents page
            requestHandler : $.historyLoad,
            requestHandlerScope : $
        };

        // sets the default options value
        var options = options ? options : {};

        // constructs the options
        var options = $.extend(defaults, options);

        // sets the jquery matched object
        var matchedObject = this;

        var inputMatchedObject = $("input", matchedObject);

        var seachButtonMatchedObject = $(".autocomplete-search-button",
                matchedObject);

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
            matchedObject.append("<div class=\"autocomplete-container\">");
        };

        /**
         * Registers the event handlers for the created objects.
         */
        var _registerHandlers = function() {
            inputMatchedObject.keydown(function(event) {
                        var keyCode = event.keyCode;

                        if (keyCode == UP) {
                            // highlights the previous element
                            _highlightPrevious(matchedObject);

                            return false;
                        } else if (keyCode == DOWN) {
                            // highlights the next element
                            _highlightNext(matchedObject);

                            return false;
                        }
                    });

            inputMatchedObject.keypress(function(event) {
                        var keyCode = event.keyCode;

                        if (keyCode == ENTER) {
                            // stops the propagation on the enter keypress event
                            return false;
                        }
                    });

            // registers the handler for the key up event
            inputMatchedObject.keyup(function(event) {
                        var keyCode = event.keyCode;

                        // in case an arrow key was pressed
                        if (keyCode == UP || keyCode == DOWN || keyCode == LEFT
                                || keyCode == RIGHT) {
                            // skips the search
                            return;
                        }

                        if (keyCode == ENTER) {
                            // shows the page for highlighted index
                            _selectHighlighted(options, matchedObject,
                                    inputMatchedObject);

                            // skips the search
                            return false;
                        }

                        // performs the actual search action
                        _search(options, matchedObject, inputMatchedObject);
                    });

            // registers the handler for the key up event
            inputMatchedObject.blur(function() {
                        // hides the auto complete when the input field is blurred
                        _hideAutoComplete(options, matchedObject);
                    });

            $("body").click(function() {
                        _hideAutoComplete(options, matchedObject);
                    });
        };

        var _showAutoComplete = function(options, matchedObject) {
            // retrieves the configured show effect
            var showEffect = options["showEffect"];

            $(".autocomplete-container", matchedObject)[showEffect]();
        }
        var _hideAutoComplete = function(options, matchedObject) {
            // retrieves the configured hide effect
            var hideEffect = options["hideEffect"];

            $(".autocomplete-container", matchedObject)[hideEffect]();
        }

        var _highlightPrevious = function(matchedObject) {
            // retrieves the highlighted element
            var higlightedElement = $(".highlighted", matchedObject);

            // initializes the previous element
            var previousElement = null;

            if (!higlightedElement) {
                return;
            }

            // removes the higlighted class
            higlightedElement.removeClass("highlighted");

            // retrieves the default previous element
            previousElement = higlightedElement.prev(".autocomplete-container li");

            // in case the element was not found
            if (previousElement.length == 0) {
                // does nothing
                return;
            }

            // hightlights the previous element
            previousElement.addClass("highlighted");
        }

        var _highlightNext = function(matchedObject) {
            // retrieves the highlighted element
            var higlightedElement = $(".highlighted", matchedObject);

            // initializes the next element
            var nextElement = null;

            // in case no element is highlighted
            if (higlightedElement.length == 0) {
                // highlights the first element
                nextElement = $(".autocomplete-container li:first",
                        matchedObject);
                console.warn(nextElement);
            } else {
                // retrieves the default next element
                nextElement = higlightedElement.next(".autocomplete-container li");
            }

            // in case there is no next element
            if (nextElement.length == 0) {
                // does nothing
                return;
            }

            // removes the higlighted class
            higlightedElement.removeClass("highlighted");

            // hightlights the next element
            nextElement.addClass("highlighted");
        }

        var _selectHighlighted = function(options, matchedObject, inputMatchedObject) {
            // retrieves the search timeout
            var searchTimeout = options["searchTimeout"];

            // hides the auto complete
            _hideAutoComplete(options, matchedObject);

            // resets the search timeout
            clearTimeout(searchTimeout);

            // retrieves the intended target
            var targetRequest = $(".highlighted", matchedObject).attr("target_request");

            // retrieves the request handler
            var requestHandler = options["requestHandler"];
            var requestHandlerScope = options["requestHandlerScope"];

            // handles the request
            requestHandler.call(requestHandlerScope, targetRequest);

            // clears the search query field
            inputMatchedObject.attr("value", "");
        }

        var _search = function(options, matchedObject, inputMatchedObject) {
            // retrieves the url
            var url = options["url"];

            // retrieves the search timeout
            var searchTimeout = options["searchTimeout"];

            // retrieves the search query
            var searchQuery = inputMatchedObject.attr("value");

            // in case the search query is empty
            if (!searchQuery || searchQuery == "") {
                // hides the auto complete container
                _hideAutoComplete(options, matchedObject);

                // skips the load
                return;
            }

            // defines the request arguments for the previous button
            var formData = "search_query=" + searchQuery;

            // resets the search timeout
            clearTimeout(searchTimeout);

            // creates a new search timeout
            options["searchTimeout"] = setTimeout(function() {
                        $.ajax({
                                    url : url,
                                    type : "POST",
                                    data : formData,
                                    success : function(result) {
                                        _tableContentCallback(options,
                                                matchedObject,
                                                inputMatchedObject, result);
                                    }
                                });
                    }, 500);
        }

        // the table content callback function
        var _tableContentCallback = function(options, matchedObject, inputMatchedObject, result) {
            // unbinds the events on the items
            $(".autocomplete-container > ul > li", matchedObject).unbind();

            // sets the auto complete items
            $(".autocomplete-container", matchedObject).html(result);

            // retrieves the list of autocomplete items
            matchedObjectAutocompleteItems = $(
                    ".autocomplete-container > ul > li", matchedObject);

            // in case no results were retrieved
            if (matchedObjectAutocompleteItems.size() == 0) {
                // hides the autocomplete
                _hideAutoComplete(options, matchedObject);

                // skips the processing
                return;
            }

            // shows the auto complete
            _showAutoComplete(options, matchedObject);

            // register the click handler for items
            matchedObjectAutocompleteItems.click(function(event) {
                        var element = $(this);

                        // hides the auto complete
                        _hideAutoComplete(options, matchedObject);

                        // retrieves the intended target
                        targetRequest = element.attr("target_request");

                        // retrieves the request handler
                        var requestHandler = options["requestHandler"];
                        var requestHandlerScope = options["requestHandlerScope"];

                        // handles the request
                        requestHandler.call(requestHandlerScope, targetRequest);

                        // clears the search query field
                        inputMatchedObject.attr("value", "");
                    });

            matchedObjectAutocompleteItems.mouseover(function(event) {
                        var element = $(this);

                        // skips the update if the element is already highlighted
                        if (element.hasClass("highlighted")) {
                            return;
                        }

                        // removes the highlight from the currently highlighted element
                        $(".highlighted", matchedObject).removeClass("highlighted");

                        // highlights the hovered element
                        element.addClass("highlighted");
                    });

            // highlights the first element
            $(".autocomplete-container > ul > li:first", matchedObject).addClass("highlighted");
        };

        // initializes the plugin
        initialize();

        // returns the object
        return this;
    };
})(jQuery);
