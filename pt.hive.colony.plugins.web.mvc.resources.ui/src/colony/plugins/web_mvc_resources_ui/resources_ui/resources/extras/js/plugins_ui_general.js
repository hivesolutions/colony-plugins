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

(function($) {
    jQuery.resolveurl = function(url, options) {
        // the default values for the resolve url
        var defaults = {};

        // sets the default method value
        var method = method ? method : "default";

        // sets the default options value
        var options = options ? options : {};

        // constructs the options
        var options = jQuery.extend(defaults, options);

        // sets the jquery matched object
        var matchedObject = this;

        // retrieves the base path environment variable
        var basePath = jQuery.environment("base-path");

        // re-creates the url using the base path, in case
        // there is a valid base path
        var url = basePath ? basePath + url : url;

        // returns the "resolved" url
        return url;
    };
})(jQuery);

(function($) {
    jQuery.environment = function(variableName, defaultValue, options) {
        // the default values for the environment
        var defaults = {
            environmentElement : jQuery("#environment-variables")
        };

        // sets the default method value
        var method = method ? method : "default";

        // sets the default options value
        var options = options ? options : {};

        // constructs the options
        var options = jQuery.extend(defaults, options);

        // sets the jquery matched object
        var matchedObject = this;

        // retrieves the environment element
        var environmentElement = options["environmentElement"];

        // retrieves the (environement) variable value
        var variableValue = jQuery("#" + variableName, environmentElement).html();

        // sets the variable value with the default value in case it's necessary
        var variableValue = variableValue === null ? defaultValue : variableValue;

        // returns the (environement) variable value
        return variableValue;
    };
})(jQuery);

(function($) {
    jQuery.fn.page = function(method, options) {
        // the default values for the menu
        var defaults = {
            headerPath : "header"
        };

        // sets the default method value
        var method = method ? method : "default";

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
            // tries to retrieve the history load value
            var historyLoad = options["historyLoad"];

            // tries to retrieve the history handler
            var historyHandler = options["historyHandler"];

            // sets the defaul history load value
            historyLoad = historyLoad != null ? historyLoad : true;

            // resolves the partial url
            var partialUrl = jQuery.resolveurl("search/autocomplete/partial");

            // creates the menu bar in the menu bar component
            jQuery("#menu-bar", matchedObject).menubar();

            // creates the link table in the
            // site menu component
            jQuery("#site-menu", matchedObject).linktable();

            // installs the autocomplete in the menu bar search field
            jQuery("#menu-bar-search-field", matchedObject).autocomplete({
                        url : partialUrl,
                        showEffect : "slideDown",
                        hideEffect : "slideUp"
                    });

            // in case the history load flag is active
            if (historyLoad) {
                // initializes the history
                jQuery.historyInit(historyHandler, "");
            }
        };

        /**
         * Registers the event handlers for the created objects.
         */
        var _registerHandlers = function() {
        };

        var _reloadHeader = function(matchedObject, options) {
            // retrieves the header path
            var headerPath = options["headerPath"];

            // resolves the header path retrieving the
            // "full" target
            var fullTarget = jQuery.resolveurl(headerPath);

            jQuery.ajax({
                        url : fullTarget,
                        success : function(data) {
                            __reloadMenuBar(matchedObject, options, data);
                        },
                        error : function(request, textStatus, errorThrown) {
                        }
                    });
        };

        var __reloadMenuBar = function(matchedObject, options, contents) {
            // retrieves the header element
            var header = jQuery("#header", matchedObject);

            // retrieves the menu bar element active
            var menuBarElementActive = jQuery("#menu-bar > ul > li.active > a",
                    header);

            // removes the menu bar element active id
            var menuBarElementActiveId = menuBarElementActive.attr("id");

            // clears the header element
            header.empty();

            // appends the contents to the header
            header.append(contents);

            // removes the active class from the current active list item
            jQuery("#menu-bar > ul > li.active", header).removeClass("active");

            // adds the active class to the previopus acrive list item
            jQuery("#menu-bar > ul > li > #" + menuBarElementActiveId).parent().addClass("active");

            // creates the menu bar in the menu bar component
            jQuery("#menu-bar", matchedObject).menubar();
        };

        // switches over the method
        switch (method) {
            case "reloadHeader" :
                // reloads the header
                _reloadHeader(matchedObject, options);

                // breaks the switch
                break;

            case "default" :
                // initializes the plugin
                initialize();

                // breaks the swtich
                break;
        }

        // returns the object
        return this;
    };
})(jQuery);

(function($) {
    jQuery.fn.maincontainer = function(method, options) {
        // the default values for the menu
        var defaults = {
            minimumContentsHeight : 600,
            smallWidth : 684,
            largeWidth : 884
        };

        // sets the default method value
        var method = method ? method : "default";

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
            // retrieves the left column
            var leftColumn = jQuery("#left-column", matchedObject);

            // sets the initial attribute value
            leftColumn.data("visible", true);

            // adds the loading animation to all
            // the items in the side bar
            jQuery("#left-column > ul > li", matchedObject).loadinganimation();
        };

        /**
         * Registers the event handlers for the created objects.
         */
        var _registerHandlers = function() {
            jQuery("#content-icon", matchedObject).click(function() {
                        _toggleSidePanel(matchedObject, options);
                    });

            jQuery("#left-column > ul > li", matchedObject).click(
                    function(event, element) {
                        // retrieves the event target element
                        var targetElement = jQuery(event.target);

                        // in case the target element is not a list item
                        // the parent should be the target element
                        if (!targetElement.is("li")) {
                            // sets the target element parent as the
                            // target element
                            targetElement = targetElement.parent();
                        }

                        // retrieves the target request fromt the target element
                        var targetRequest = targetElement.attr("data-target_request");

                        // updates the history with the new value
                        jQuery.historyLoad(targetRequest);
                    });
        };

        /**
         * Togles the state of the side panel, changing the visibility of it.
         *
         * @param {Element}
         *            matchedObject The matched object.
         * @param {Map}
         *            options The options of the plugin instance.
         */
        var _toggleSidePanel = function(matchedObject, options) {
            // retrieves the left column
            var leftColumn = jQuery("#left-column", matchedObject);

            // retrieves and inverts the current visible value
            var visible = !leftColumn.data("visible");

            // sets the initial attribute value
            leftColumn.data("visible", visible);

            // in case the left column is visible, the update
            // is required to be before the transition
            // in order to avoid overflow problems
            if (visible) {
                _updateContentsWidth(matchedObject, options);
            }

            // animates the left column
            leftColumn.animate({
                        width : "toggle"
                    }, function() {
                        // in case the left column is not visible
                        if (!visible) {
                            _updateContentsWidth(matchedObject, options);
                        }
                    });
        };

        /**
         * Reloads the main contents page. Setting all the ui components and
         * registering all the event handlers for the page.
         *
         * @param {Element}
         *            matchedObject The matched object.
         * @param {Map}
         *            options The options of the plugin instance.
         */
        var _reloadContents = function(matchedObject, options) {
            // starts the overlay component
            jQuery("#overlay").overlay();

            // starts the notification area
            jQuery("#notification-area").notificationarea();

            // creates the text area components
            jQuery("input, textarea", matchedObject).textarea();

            // creates the button components
            jQuery("div.button", matchedObject).button();

            // creates the switch button components
            jQuery("div.switch-button", matchedObject).switchbutton();

            // creates the date field components
            jQuery("div.date-field", matchedObject).datefield();

            // creates the progress indicator components
            jQuery("div.progress-indicator", matchedObject).progressindicator();

            // creates the dropbox components
            jQuery("div.dropbox", matchedObject).dropbox();

            // creates the message components
            jQuery("div.message", matchedObject).message();

            // creates the search table components
            jQuery("div.search-table", matchedObject).searchtable();

            // adds the mandatory dot code to the labels that
            // contain the mandatory option
            jQuery("label.mandatory", matchedObject).append("<span style=\"color: red;margin-left: 4px;\">&bull;</span>");

            // binss the form keypress to the form submit action
            jQuery("form", matchedObject).bind("keypress", function(event) {
                        // retrieves the event code
                        var code = (event.keyCode ? event.keyCode : event.which);

                        // in case it's the enter key
                        if (code == 13) {
                            // submits the form
                            __formSubmit(event);
                        }
                    });

            // binds the click event of the submit button to
            // the form submit function
            jQuery("form div.submit", matchedObject).bind("click", __formSubmit);

            // binds the click event of the reset button to
            // the form reset function
            jQuery("form div.cancel", matchedObject).bind("click", __formReset);

            // retrieves the value of the ajax submit environment variable
            var ajaxSubmit = jQuery.environment("ajax-submit", "false");

            // in case ajax submission is enabled
            if (ajaxSubmit != "false") {
                // binds the submit event of the forms to the form
                // submit function
                jQuery("form", matchedObject).bind("submit", function(event) {
                            __formSubmit(event);
                            return false;
                        });

                // iterates over all the forms to
                // set the "dynamic" action
                jQuery("form", matchedObject).each(function() {
                            // retrieves the form value
                            var formValue = jQuery(this);

                            // retrieves the action target value
                            // from the form
                            var actionTarget = formValue.attr("data-action_target");

                            // in case there is no action target defined
                            // (not dynamic) form
                            if (actionTarget == null) {
                                // returns immediately
                                return;
                            }

                            // resolves the action path
                            var action = jQuery.resolveurl(actionTarget
                                    + ".ajx");

                            // sets the action in the form
                            formValue.attr("action", action);
                        });
            }

            // iterates over all the links of "type" (class) dynamic
            // to set the "dynamic" href (action)
            jQuery("a.dynamic", matchedObject).each(function() {
                        // retrieves the link value
                        var linkValue = jQuery(this);

                        // retrieves the action target value
                        // from the link
                        var actionTarget = linkValue.attr("data-action_target");

                        // in case there is no action target defined
                        // (not dynamic) link
                        if (actionTarget == null) {
                            // returns immediately
                            return;
                        }

                        // creates the href (action) path
                        var href = jQuery.resolveurl(actionTarget);

                        // sets the href (action) in the link
                        linkValue.attr("href", href);
                    });

            // updates the contents size
            jQuery("#main-container").maincontainer("update");

            // register the forms
            _registerForms(matchedObject, options);
        };

        /**
         * Registers the forms of the main container.
         *
         * @param {Element}
         *            matchedObject The matched object.
         * @param {Map}
         *            options The options of the plugin instance.
         */
        var _registerForms = function(matchedObject, options) {
            jQuery("form", matchedObject).bind("submit_start", function(event) {
                        // shows the filter
                        jQuery(this).filter("show");
                    });

            jQuery("form", matchedObject).bind(
                    "success",
                    function(event, responseText, status, xmlHttpRequest, form) {
                        // hides the filter
                        jQuery(this).filter("hide");

                        // updates the contents page with the response text
                        __updateContentsPage(matchedObject, options,
                                responseText);

                        // shows the message (if necessary)
                        jQuery(".message", matchedObject).message("show", {
                                    timeout : 7500
                                });
                    });

            jQuery("form", matchedObject).bind("error", function() {
                // hides the filter
                jQuery(this).filter("hide");

                // updates the contents page with an error message
                __updateContentsPage(matchedObject, options,
                        "There was an error submiting the form");

                // shows the message (if necessary)
                jQuery(".message", matchedObject).message("show", {
                            timeout : 15000
                        });
            });
        };

        /**
         * Updates the contents area size, according to the available space.
         * This update method should be called whenever the area is changed.
         *
         * @param {Element}
         *            matchedObject The matched object.
         * @param {Map}
         *            options The options of the plugin instance.
         */
        var _updateContentsSize = function(matchedObject, options) {
            // retrieves the contents
            var contents = jQuery("#contents", matchedObject);

            // sets the content size as set
            contents.data("size_set", true)

            // waits until the contents is ready
            contents.ready(function() {
                        // updates the contents height
                        _updateContentsHeight(matchedObject, options);

                        // updates the contents width
                        _updateContentsWidth(matchedObject, options);
                    });
        };

        /**
         * Updates the current contents height.
         *
         * @param {Element}
         *            matchedObject The matched object.
         * @param {Map}
         *            options The options of the plugin instance.
         */
        var _updateContentsHeight = function(matchedObject, options) {
            // retrieves the minimum contents height
            var minimumContentsHeight = options["minimumContentsHeight"];

            // retrieves the contents
            var contents = jQuery("#contents", matchedObject);

            // retrieves the content body
            var contentBody = jQuery("#content-body", matchedObject);

            // retrieves the contents height
            var contentsHeight = contents.height();

            // retrieves the contents margin top
            var contentsMarginTop = parseInt(contents.css("margin-top"));

            // retrieves the contents margin bottom
            var contentsMarginBottom = parseInt(contents.css("margin-bottom"));

            // sets the content height as the minimum between the
            // minimum contents height and the current contents height
            var contentsHeight = contentsHeight > minimumContentsHeight
                    ? contentsHeight
                    : minimumContentsHeight;

            // calculates the full contents height, including the
            // top and bottom margins
            var contentsHeight = contentsHeight + contentsMarginTop
                    + contentsMarginBottom;

            // sets the content body with the contents height
            contentBody.height(contentsHeight);
        };

        /**
         * Updates the current contents width.
         *
         * @param {Element}
         *            matchedObject The matched object.
         * @param {Map}
         *            options The options of the plugin instance.
         */
        var _updateContentsWidth = function(matchedObject, options) {
            // retrieves the large width value
            var largeWidth = options["largeWidth"];

            // retrieves the small width value
            var smallWidth = options["smallWidth"];

            // retrieves the left column
            var leftColumn = jQuery("#left-column", matchedObject);

            // retrieves the contents
            var contents = jQuery("#contents", matchedObject);

            // retrieves the visible value
            var visible = leftColumn.data("visible");

            // in case the menu is visible
            if (visible) {
                // updates the width to large
                contents.width(smallWidth);
            }
            // otherwise the menu is not visible
            else {
                // updates the width to large
                contents.width(largeWidth);
            }
        };

        var _hideMenuLoading = function(matchedObject, options) {
            // removes the loading class from loading list items
            jQuery("#left-column > ul > li.loading", matchedObject).removeClass("loading");
        };

        var _changeAll = function(matchedObject, options) {
            // changes the contents
            _changeContents(matchedObject, optiosn);

            // changes the contents menu
            _changeContentsMenu(matchedObject, optiosn);
        }

        var _changeContents = function(matchedObject, options) {
            // retrieves the target
            var target = options["target"];

            // retrieves the minimum contents height
            var minimumContentsHeight = options["minimumContentsHeight"];

            // retrieves the contents
            var contents = jQuery("#contents", matchedObject);

            // retrieves the content size set value
            var contentsSizeSet = contents.data("size_set");

            // retrieves the contents position
            var contentsPosition = contents.position();

            // retrieves the contents width
            var contentsWidth = contents.width();

            // retrieves the contents height
            var contentsHeight = contents.height();

            // retrieves the contents margin top
            var contentsMarginTop = parseInt(contents.css("margin-top"));

            // retrieves the contents margin bottom
            var contentsMarginBottom = parseInt(contents.css("margin-bottom"));

            // retrieves the contents margin left
            var contentsMarginLeft = parseInt(contents.css("margin-left"));

            // retrieves the contents margin right
            var contentsMarginRight = parseInt(contents.css("margin-right"));

            // retrieves the contents height based on the maximum of the
            // height between the contents height and the minimum contents height
            var contentsHeight = contentsHeight > minimumContentsHeight
                    ? contentsHeight
                    : minimumContentsHeight;

            // creates the contents size map
            var contentsSize = {
                width : contentsWidth,
                height : contentsHeight
            };

            // creates the contents margins map
            var contentsMargins = {
                horizontal : contentsMarginLeft + contentsMarginRight,
                vertical : contentsMarginTop + contentsMarginBottom
            };

            // creates the filter options map
            var filterOptions = {
                size : contentsSize,
                position : contentsPosition,
                margins : contentsMargins
            };

            // creates the message options map
            var messageOptions = {
                size : contentsSize,
                position : contentsPosition,
                margins : contentsMargins,
                textMessage : "Loading"
            };

            // in case the contents size is set, the filter
            // and the loading message may be shown (it's possible
            // to measure the width of the contents)
            if (contentsSizeSet) {
                // shows both the filter and the loading message
                jQuery("#filter").mainfilter("show", filterOptions);
                jQuery("#loading-message").loadingmessage("show",
                        messageOptions);
            }

            // retrieves the real target
            var realTarget = target.split("&", 1)[0];

            // determines the first separator index
            var separatorIndex = target.indexOf("&");

            // retrieves the arguments from the target
            var arguments = target.slice(separatorIndex + 1);

            // creates the full target by resolving the address
            // resulting from appending the arguments to the real target
            var fullTarget = jQuery.resolveurl(realTarget + ".ajx?" + arguments);

            jQuery.ajax({
                url : fullTarget,
                success : function(data) {
                    // creates the success callback function
                    var successCallback = function() {
                        // updates the contents page with the retrieved data
                        __updateContentsPage(matchedObject, options, data);
                    };

                    // creates the filter options
                    var filterOptions = {
                        callback : successCallback
                    };

                    // hides the filter and calls the callback
                    jQuery("#filter").mainfilter("hide", filterOptions);

                    // unsets the loading
                    __unsetLoading(matchedObject, options);
                },
                error : function(request, textStatus, errorThrown) {
                    var errorCallback = function() {
                        jQuery("body").dialogwindow("default", {
                            title : "Warning",
                            subTitle : "Problem Loading Resources",
                            message : "There was a problem loading resources, this indicates an erroneous behaviour communicating with the server.",
                            buttonMessage : "Do you want to continue ?",
                            errorCallbackFunctions : [function() {
                                    }]
                        });

                        // updates the contents page with the error message
                        __updateContentsPage(matchedObject, options,
                                "<div id=\"contents\">There was an error retrieving the resource</div>");
                    };

                    var filterOptions = {
                        callback : errorCallback
                    };

                    // hides the filter and calls the callback
                    jQuery("#filter").mainfilter("hide", filterOptions);

                    // unsets the loading
                    __unsetLoading(matchedObject, options);
                }
            });
        };

        var _changeContentsMenu = function(matchedObject, options) {
            // retrieves the target
            var target = options["target"];

            // sets the current menu in the matched object
            matchedObject.data("menu", target);

            // removes the active class fomr all the header items
            jQuery("#left-column > h1", matchedObject).removeClass("active");

            // removes the active class fomr all the list items
            jQuery("#left-column > ul > li", matchedObject).removeClass("active");

            // retrieves the target element to be changed
            var targetElement = jQuery(
                    "#left-column > ul > li[data-target_request=" + target
                            + "]", matchedObject);

            // adds the active class to the target element
            // the refered list item
            targetElement.addClass("active");

            // adds the loading class to the target element
            // the refered list item
            targetElement.addClass("loading");

            // retrieves the identifier from the parent element
            var idValue = targetElement.parent().attr("id")

            // adds the active class to the parents value
            targetElement.parent().parent().children("h1#" + idValue).addClass("active");
        };

        var __unsetLoading = function(matchedObject, options) {
            // hides the loading message element
            jQuery("#loading-message").loadingmessage("hide");

            // hides the menu loading
            _hideMenuLoading(matchedObject, options);
        };

        var __formSubmit = function(event) {
            // retrieves the event target
            var eventTarget = event.target;

            // retrieves the event target element
            var eventTargetElement = jQuery(eventTarget);

            if (eventTargetElement.is("form")) {
                // retrieves the parent form
                var parentForm = eventTargetElement;
            } else {
                // retrieves the parent form
                var parentForm = eventTargetElement.parents("form");
            }

            // calls the form submit start function
            // to trigger the submit start event
            __formSubmitStart(parentForm);

            // retrieves the value of the ajax submit environment variable
            var ajaxSubmit = jQuery.environment("ajax-submit", "false");

            // in case ajax submission is disabled
            if (ajaxSubmit == "false") {
                // submits the form normally
                parentForm.submit();
            } else {
                // submits the parent form using ajax
                parentForm.ajaxSubmit({
                            success : __formSuccess,
                            error : __formError
                        });
            }
        };

        /**
         * Resets a form reseting all the values to the original values.
         *
         * @param {Event}
         *            event The event object sent from the form submit event.
         */
        var __formReset = function(event) {
            // retrieves the event target
            var eventTarget = event.target;

            // retrieves the event target element
            var eventTargetElement = jQuery(eventTarget);

            if (eventTargetElement.is("form")) {
                // retrieves the parent form
                var parentForm = eventTargetElement;
            } else {
                // retrieves the parent form
                var parentForm = eventTargetElement.parents("form");
            }

            // iterates over all the parent form
            // elements to reset them
            parentForm.each(function() {
                        // resets the element
                        this.reset();
                    });
        };

        /**
         * Method called uppon for submission start.
         *
         * @param {Element}
         *            form The called form element.
         */
        var __formSubmitStart = function(form) {
            // triggers the submit start event
            form.trigger("submit_start", [form]);
        };

        /**
         * Method called uppon for submission error.
         *
         * @param {String}
         *            responseText The response text.
         * @param {String}
         *            status The status of the error.
         * @param {XmlHttpRequest}
         *            xmlHttpRequest The associated xml http request.
         * @param {Element}
         *            form The called form element.
         */
        var __formError = function(responseText, status, xmlHttpRequest, form) {
            // triggers the error event
            form.trigger("error", [responseText, status, xmlHttpRequest, form]);
        };

        /**
         * Method called uppon for submission success.
         *
         * @param {String}
         *            responseText The response text.
         * @param {String}
         *            status The status of the success.
         * @param {XmlHttpRequest}
         *            xmlHttpRequest The associated xml http request.
         * @param {Element}
         *            form The called form element.
         */
        var __formSuccess = function(responseText, status, xmlHttpRequest, form) {
            // triggers the success event
            form.trigger("success",
                    [responseText, status, xmlHttpRequest, form]);
        };

        /**
         * Updates the contents page with the data in the given string.
         *
         * @param {String}
         *            data The data to be set in the contents page.
         */
        var __updateContentsPage = function(matchedObject, options, data) {
            // removes the current includes, meta data and contents from the
            // contents body element
            jQuery("#content-body > #includes, #content-body > #meta-data, #content-body > #contents").remove();

            // removes all the css temporary elements
            jQuery("head > #css-removal").remove();

            // adds the data to the contents body
            jQuery("#content-body").append(data);

            // reloads the contents page
            jQuery("#main-container").maincontainer("reload");

            // loads the includes
            __loadIncludes(matchedObject, options);

            // loads the meta data
            __loadMetaData(matchedObject, options);
        };

        var __loadIncludes = function(matchedObject, options) {
            // retrieves the content body
            var contentBody = jQuery("#content-body")

            // retreives the includes from the content body
            var includes = jQuery("#includes", contentBody);

            // retrieves the javascript file references from the includes
            var javascriptFiles = jQuery(".javascript", includes);

            // retrieves the css file references from the includes
            var cssFiles = jQuery(".css", includes);

            // retrieves the head element
            var head = jQuery("head");

            // iterates over all the javascript file references
            javascriptFiles.each(function(index, element) {
                // retrieves the target from the javascript element
                var target = jQuery(element).html();

                // resolves the full target
                var fullTarget = jQuery.resolveurl(target);

                jQuery.ajax({
                    url : fullTarget,
                    success : function(data) {
                        eval(data);
                    },
                    error : function(request, textStatus, errorThrown) {
                        jQuery("body").dialogwindow("default", {
                            title : "Warning",
                            subTitle : "Problem Loading Javascript Files",
                            message : "There was a problem loading javascript files, this indicates an erroneous behaviour communicating with the server.",
                            buttonMessage : "Do you want to continue ?",
                            errorCallbackFunctions : [function() {
                                    }]
                        });
                    }
                });
            });

            // iterates over all the css file references
            cssFiles.each(function(index, element) {
                        // retrieves the target from the javascript element
                        var target = jQuery(element).html();

                        // creates the html to import the css element
                        var cssHtml = "<link type=\"text/css\" href=\""
                                + target
                                + "\" rel=\"stylesheet\" id=\"css-removal\">";

                        // appends the css element to the head
                        head.append(cssHtml);
                    });
        };

        var __loadMetaData = function(matchedObject, options) {
            // retrieves the force reload option
            var forceReload = options["forceReload"];

            // retrieves the content body
            var contentBody = jQuery("#content-body")

            // retreives the meta data from the
            var metaData = jQuery("#meta-data", contentBody);

            // retrieves the area references from the meta data
            var areas = jQuery(".area", metaData);

            // retrieves the side panel file references from the meta data
            var sidePanels = jQuery(".side-panel", metaData);

            // iterates over all area references
            areas.each(function(index, element) {
                        // retrieves the area name from the element
                        var areaName = jQuery(element).html();

                        // change the current active menu
                        jQuery("#menu-bar").menubar("change", {
                                    area : areaName
                                });
                    });

            // iterates over all the side panel file references
            sidePanels.each(function(index, element) {
                // sets the current side panel in the matched object
                var sidePanel = matchedObject.data("side_panel");

                // retrieves the target from the javascript element
                var target = jQuery(element).html();

                // in case the target side panel
                // is the current one and the force reload
                // flag is not set
                if (target == sidePanel && !forceReload) {
                    // returns immediatly
                    return;
                }

                // sets the side panel in the current object
                matchedObject.data("side_panel", target);

                // resolves the full target (url)
                var fullTarget = jQuery.resolveurl(target);

                jQuery.ajax({
                    url : fullTarget,
                    success : function(data) {
                        // retrieves the left column
                        var leftColumn = jQuery("#left-column", contentBody);

                        // retrieves the icon bar
                        var iconBar = jQuery("#icon-bar", contentBody);

                        // retrieves the visible value
                        var visible = leftColumn.data("visible");

                        // removes the current icon bar from the content body
                        iconBar.remove();

                        // removes the left column from the content body
                        leftColumn.remove();

                        // replacess the left column data
                        contentBody.prepend(data);

                        // reloads the side panel
                        __reloadSidePanel(matchedObject, options, visible);

                        // changes the contents menu
                        _changeContentsMenu(matchedObject, options);
                    },
                    error : function(request, textStatus, errorThrown) {
                        jQuery("body").dialogwindow("default", {
                            title : "Warning",
                            subTitle : "Problem Loading Side Panel",
                            message : "There was a problem loading side panel, this indicates an erroneous behaviour communicating with the server.",
                            buttonMessage : "Do you want to continue ?",
                            errorCallbackFunctions : [function() {
                                    }]
                        });
                    }
                });
            });
        };

        var __reloadSidePanel = function(matchedObject, options, visible) {
            // retrieves the left column
            var leftColumn = jQuery("#left-column", matchedObject);

            // in case the left column is not visible
            if (!visible) {
                // hides the left column
                leftColumn.hide();
            }

            // sets the new visible value
            leftColumn.data("visible", visible);

            jQuery("#content-icon", matchedObject).click(function() {
                        _toggleSidePanel(matchedObject, options);
                    });

            jQuery("#left-column > ul > li", matchedObject).click(
                    function(event, element) {
                        // retrieves the event target element
                        var targetElement = jQuery(event.target);

                        // in case the target element is not a list item
                        // the parent should be the target element
                        if (!targetElement.is("li")) {
                            // sets the target element parent as the
                            // target element
                            targetElement = targetElement.parent();
                        }

                        // retrieves the target request from the target element
                        var targetRequest = targetElement.attr("data-target_request");

                        // updates the history with the new value
                        jQuery.historyLoad(targetRequest);
                    });
        };

        // switches over the method
        switch (method) {
            case "reload" :
                // reloads the contents
                _reloadContents(matchedObject, options);

                // breaks the switch
                break;

            case "update" :
                // updats the contents size
                _updateContentsSize(matchedObject, options);

                // breaks the switch
                break;

            case "hideLoading" :
                // hides the menu loading
                _hideMenuLoading(matchedObject, options);

                // breaks the switch
                break;

            case "changeAll" :
                // changes all
                _changeAll(matchedObject, options);

                // breaks the switch
                break;

            case "change" :
                // changes the contents
                _changeContents(matchedObject, options);

                // breaks the switch
                break;

            case "changeMenu" :
                // changes the content menu
                _changeContentsMenu(matchedObject, options);

                // breaks the switch
                break;

            case "loadMetadata" :
                // loads the meta data
                __loadMetaData(matchedObject, options);

                // breaks the switch
                break;

            case "default" :
                // initializes the plugin
                initialize();

                // breaks the switch
                break;
        }

        // returns the object
        return this;
    };
})(jQuery);

(function($) {
    jQuery.fn.loadinganimation = function(options) {
        // the default values for the menu
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
            // adds the loading animation div to the matched object
            matchedObject.append("<div class=\"loading-animation\"></div>");
        };

        /**
         * Registers the event handlers for the created objects.
         */
        var _registerHandlers = function() {
        };

        // initializes the plugin
        initialize();

        // returns the object
        return this;
    };
})(jQuery);

(function($) {
    jQuery.fn.mainfilter = function(method, options) {
        // the default values for the menu
        var defaults = {
            margins : {
                top : 0,
                left : 0
            }
        };

        // sets the default method value
        var method = method ? method : "default";

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
        };

        /**
         * Registers the event handlers for the created objects.
         */
        var _registerHandlers = function() {
        };

        var _show = function(matchedObject, options) {
            // retrieves the size
            var size = options["size"];

            // retrieves the position
            var position = options["position"];

            // retrieves the margins
            var margins = options["margins"];

            // retrieves the callback
            var callback = options["callback"];

            // sets the left position of the filter
            matchedObject.css("left", position.left);

            // sets the top position of the filter
            matchedObject.css("top", position.top)

            // sets the width of the filter
            matchedObject.width(size.width + margins.horizontal);

            // sets the height of the filter
            matchedObject.height(size.height + margins.vertical);

            // shows the filter
            matchedObject.fadeIn(300, callback);
        }

        var _hide = function(matchedObject, options) {
            // retrieves the callback
            var callback = options["callback"];

            // fades out the filter and calls the
            // callback (on end)
            matchedObject.fadeOut(0, callback);
        }

        // switches over the method
        switch (method) {
            case "show" :
                _show(matchedObject, options);
                break;

            case "hide" :
                _hide(matchedObject, options);
                break;

            case "default" :
                // initializes the plugin
                initialize();
                break;
        }

        // returns the object
        return this;
    };
})(jQuery);

(function($) {
    jQuery.fn.loadingmessage = function(method, options) {
        // the default values for the menu
        var defaults = {
            margins : {
                top : 0,
                left : 0
            }
        };

        // sets the default method value
        var method = method ? method : "default";

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
         * Registers the event handlers for the created objects.
         */
        var _registerHandlers = function() {
        };

        /**
         * Creates the necessary html for the component.
         */
        var _appendHtml = function() {
        };

        var _show = function(matchedObject, options) {
            // retrieves the size
            var size = options["size"];

            // retrieves the position
            var position = options["position"];

            // retrieves the margins
            var margins = options["margins"];

            // retrieves the text message
            var textMessage = options["textMessage"];

            // retrieves the callback
            var callback = options["callback"];

            // sets the message as the html contents
            matchedObject.html(textMessage);

            // retrieves the message width
            var messageWidth = matchedObject.width();

            // sets the left position of the message
            matchedObject.css("left", position.left + (size.width / 2)
                            - (messageWidth / 2));

            // sets the top position of the message
            matchedObject.css("top", position.top)

            // shows the message
            matchedObject.fadeIn(300, callback);
        }

        var _hide = function(matchedObject, options) {
            // retrieves the callback
            var callback = options["callback"];

            // fades out the message
            matchedObject.fadeOut(0, callback);
        }

        // switches over the method
        switch (method) {
            case "show" :
                _show(matchedObject, options);
                break;

            case "hide" :
                _hide(matchedObject, options);
                break;

            case "default" :
                // initializes the plugin
                initialize();
                break;
        }

        // returns the object
        return this;
    };
})(jQuery);

(function($) {
    jQuery.fn.filter = function(method, options) {
        // the default values for the menu
        var defaults = {};

        // sets the default method value
        var method = method ? method : "default";

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
        };

        /**
         * Registers the event handlers for the created objects.
         */
        var _registerHandlers = function() {
        };

        var _getValues = function(matchedObject) {
            // retrieves the matched object position
            var matchedObjectPosition = matchedObject.position();

            // retrieves the matched object width
            var matchedObjectWidth = matchedObject.width();

            // retrieves the matched object height
            var matchedObjectHeight = matchedObject.height();

            // retrieves the matched object margin top
            var matchedObjectMarginTop = parseInt(matchedObject.css("margin-top"));

            // retrieves the matched object margin bottom
            var matchedObjectMarginBottom = parseInt(matchedObject.css("margin-bottom"));

            // retrieves the matched object margin left
            var matchedObjectMarginLeft = parseInt(matchedObject.css("margin-left"));

            // retrieves the matched object margin right
            var matchedObjectMarginRight = parseInt(matchedObject.css("margin-right"));

            var matchedObjectSize = {
                width : matchedObjectWidth,
                height : matchedObjectHeight
            };

            var matchedObjectMargins = {
                horizontal : matchedObjectMarginLeft + matchedObjectMarginRight,
                vertical : matchedObjectMarginTop + matchedObjectMarginBottom
            };

            return [matchedObjectSize, matchedObjectPosition,
                    matchedObjectMargins];
        };

        var _show = function(matchedObject, options) {
            // retrieves the values list from
            var valuesList = _getValues(matchedObject)

            // retrieves size, position and margins
            // from the values list
            var size = valuesList[0];
            var position = valuesList[1];
            var margins = valuesList[2];

            // sets the filter margins and may use
            // the default ones
            var margins = margins ? margins : {
                top : 0,
                left : 0
            };

            // retrieves the callback (in case it exists)
            var callback = options["callback"];

            // retrieves the filter object
            var filter = jQuery("#filter");

            // sets the filter left position
            filter.css("left", position.left);

            // sets the filter top position
            filter.css("top", position.top)

            // sets the filter width
            filter.width(size.width + margins.horizontal);

            // sets the filter height
            filter.height(size.height + margins.vertical);

            // fades in the filter, and calls the
            // callback on the end
            filter.fadeIn(300, callback);
        };

        var _hide = function(matchedObject, options) {
            // retrieves the callback (in case it exists)
            var callback = options["callback"];

            // retrieves the filter
            var filter = jQuery("#filter");

            // fades out the filter and calls the
            // callback (on end)
            filter.fadeOut(0, callback);
        };

        // switches over the method
        switch (method) {
            case "default" :
            case "show" :
                _show(matchedObject, options);
                break;

            case "hide" :
                _hide(matchedObject, options);
                break;
        }

        // returns the object
        return this;
    };
})(jQuery);

(function($) {
    jQuery.fn.linktable = function(options) {
        // the default values for the menu
        var defaults = {};

        // sets the default options value
        var options = options ? options : {};

        // constructs the options
        var options = jQuery.extend(defaults, options);

        // sets the jquery matched object
        var matchedObject = this;

        // retrieves the matched object children
        var matchedObjectChildren = jQuery("li", matchedObject);

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
            matchedObjectChildren.addClass("menu-item");
        };

        /**
         * Registers the event handlers for the created objects.
         */
        var _registerHandlers = function() {
            matchedObjectChildren.bind("click", function() {
                        // retrieves the link address
                        var linkAddress = jQuery(this).attr("data-link");

                        // replaces the url and redirects the page
                        window.location.replace(linkAddress);
                    });
        };

        // initializes the plugin
        initialize();

        // returns the object
        return this;
    };
})(jQuery);

(function($) {
    jQuery.fn.menubar = function(method, options) {
        // the default values for the menu
        var defaults = {};

        // sets the default method value
        var method = method ? method : "default";

        // sets the default options value
        var options = options ? options : {};

        // constructs the options
        var options = jQuery.extend(defaults, options);

        // sets the jquery matched object
        var matchedObject = this;

        // retrieves the matched object children
        var matchedObjectChildren = jQuery("ul > li > a", matchedObject);

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
            matchedObjectChildren.each(function(index, element) {
                        jQuery(element).menu();
                    });
        };

        /**
         * Registers the event handlers for the created objects.
         */
        var _registerHandlers = function() {
            matchedObjectChildren.bind("menushow", function() {
                        _listenActive(matchedObjectChildren);
                    });

            matchedObjectChildren.bind("menuhide", function() {
                        _listenInactive(matchedObjectChildren);
                    });
        };

        var _listenActive = function(matchedObjectChildren) {
            matchedObjectChildren.each(function(index, element) {
                        // retrieves the element reference
                        var elementReference = jQuery(element)

                        elementReference.mouseenter(function(event) {
                                    matchedObjectChildren.each(
                                            function(index, element) {
                                                jQuery(element).menu("hide", {
                                                            noEvent : true
                                                        });
                                            });

                                    // shows the menu for the element
                                    jQuery(element).menu("show", {
                                                noEffects : true,
                                                noEvent : true
                                            });
                                });
                    });
        };

        var _listenInactive = function(matchedObjectChildren) {
            matchedObjectChildren.unbind("mouseenter");
        };

        var _changeMenu = function(matchedObject, options) {
            // retrieves the area name from the options
            var areaName = options["area"];

            // removes the active class from the currently active item
            jQuery("#menu-bar > ul > li.active").removeClass("active");

            // adds the active class to the target item
            jQuery("#menu-bar > ul > li > #" + areaName).parent().addClass("active");
        };

        // switches over the method
        switch (method) {
            case "change" :
                _changeMenu(matchedObject, options);
                break;

            case "default" :
                // initializes the plugin
                initialize();
                break;
        }

        // returns the object
        return this;
    };
})(jQuery);

(function($) {
    jQuery.fn.menu = function(method, options) {
        // the default values for the menu
        var defaults = {};

        // sets the default method value
        var method = method ? method : "default";

        // sets the default options value
        var options = options ? options : {};

        // retrieves the menu object id
        var menuObjectId = "#" + this.attr("id") + "-menu";

        // retrieves the menu object
        var menuObject = jQuery(menuObjectId);

        // sets the menu in the options
        options["menu"] = menuObject;

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
        };

        /**
         * Registers the event handlers for the created objects.
         */
        var _registerHandlers = function() {
            matchedObject.click(function(event) {
                        // shows the menu
                        _showMenu(matchedObject, options);
                    });
        };

        var _showMenu = function(matchedObject, options) {
            // retrieves the menu object
            var menuObject = options["menu"];

            // retrieves the no effects option
            var noEffects = options["noEffects"];

            // retrieves the no event option
            var noEvent = options["noEvent"];

            // unsets the no effects flag
            options["noEffects"] = false;

            // unsets the no event flag
            options["noEvent"] = false;

            // retrieves the matched object offset
            var matchedObjectOffset = matchedObject.offset();

            // sets the left position of the menu object
            menuObject.css("left", matchedObjectOffset.left);

            matchedObject.parent().addClass("selected");

            // sets the animation properties
            var animationProperties = {
                opacity : "show"
            };

            // sets the animation duration time
            var animationDuration = noEffects ? 0 : 150;

            menuObject.animate(animationProperties, animationDuration,
                    function() {
                        jQuery(document).click(function() {
                                    _hideMenu(matchedObject, options);
                                });
                    });

            // in case the no event flag is inactive
            if (!noEvent) {
                // triggers the menu show event
                matchedObject.trigger("menushow");
            }
        };

        var _hideMenu = function(matchedObject, options) {
            // retrieves the menu object
            var menuObject = options["menu"];

            // retrieves the no event option
            var noEvent = options["noEvent"];

            // in case the menu object is not visible
            if (!menuObject.is(":visible")) {
                // returns immediately
                return
            }

            // hides the menu object
            menuObject.hide();
            matchedObject.parent().removeClass("selected");

            // unbinds the click event from the document
            jQuery(document).unbind("click");

            // in case the no event flag is inactive
            if (!noEvent) {
                // triggers the menu hide event
                matchedObject.trigger("menuhide");
            }
        };

        // switches over the method
        switch (method) {
            case "show" :
                _showMenu(matchedObject, options);
                break;

            case "hide" :
                _hideMenu(matchedObject, options);
                break;

            case "default" :
                // initializes the plugin
                initialize();
                break;
        }

        // returns the object
        return this;
    };
})(jQuery);
