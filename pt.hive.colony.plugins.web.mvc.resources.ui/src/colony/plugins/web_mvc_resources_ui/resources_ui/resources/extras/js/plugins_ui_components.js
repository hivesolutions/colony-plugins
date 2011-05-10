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
    jQuery.fn.textarea = function(options) {
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
        };

        /**
         * Registers the event handlers for the created objects.
         */
        var _registerHandlers = function() {
            matchedObject.focus(function(event) {
                        jQuery(this).addClass("active");
                    });

            matchedObject.blur(function(event) {
                        jQuery(this).removeClass("active");
                    });
        };

        // initializes the plugin
        initialize();

        // returns the object
        return this;
    };
})(jQuery);

(function($) {
    jQuery.fn.button = function(options) {
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
        };

        /**
         * Registers the event handlers for the created objects.
         */
        var _registerHandlers = function() {
            matchedObject.mousedown(function(event) {
                        // adds the click class
                        jQuery(this).addClass("click");
                    });

            matchedObject.mouseup(function(event) {
                        // removes the click class
                        jQuery(this).removeClass("click");
                    });
        };

        // initializes the plugin
        initialize();

        // returns the object
        return this;
    };
})(jQuery);

(function($) {
    jQuery.fn.switchbutton = function(options) {
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
            // creates the string with the html code
            var htmlCode = "<div class=\"switch-button-cursor\"></div>"
                    + "<div class=\"clear\"></div>"

            // appends the html code to the matched object
            matchedObject.append(htmlCode);
        };

        /**
         * Registers the event handlers for the created objects.
         */
        var _registerHandlers = function() {
            jQuery(matchedObject).click(function(event) {
                // retrieves the switch button
                var switchButton = jQuery(this);

                // in case the swirch button contains the
                // on class
                if (switchButton.hasClass("on")) {
                    // removes the on class from the switch button
                    switchButton.removeClass("on");

                    // adds the off class to the switch button
                    switchButton.addClass("off");

                    // triggers the status change event
                    switchButton.trigger("status_change", [switchButton, "off"]);
                } else {
                    // removes the off class from the switch button
                    switchButton.removeClass("off");

                    // adds the on class to the switch button
                    switchButton.addClass("on");

                    // triggers the status change event
                    switchButton.trigger("status_change", [switchButton, "on"]);
                }
            });
        };

        // initializes the plugin
        initialize();

        // returns the object
        return this;
    };
})(jQuery);

(function($) {
    jQuery.fn.datefield = function(options) {
        // the default values for the menu
        var defaults = {
            monthsMap : {
                0 : "January",
                1 : "February",
                2 : "March",
                3 : "April",
                4 : "May",
                5 : "June",
                6 : "July",
                7 : "August",
                8 : "September",
                9 : "October",
                10 : "November",
                11 : "December"
            }
        };

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
            // creates the string with the html code
            var htmlCode = "<div class=\"date-text-field\">"
                    + "<div class=\"date-field-input-container\">"
                    + "<input type=\"text\" class=\"date-field-input\" />"
                    + "<input type=\"hidden\" class=\"date-field-input-hidden\" />"
                    + "</div>"
                    + "<div class=\"date-field-button\"></div>"
                    + "</div>"
                    + "<div class=\"date-field-contents\">"
                    + "<div class=\"date-field-contents-header\">"
                    + "<div class=\"button-previous\"></div>"
                    + "<div class=\"button-next\"></div>"
                    + "<h1></h1>"
                    + "<div class=\"clear\"></div>"
                    + "</div>"
                    + "<div class=\"date-field-contents-body\">"
                    + "<table cellspacing=\"0\" cellpadding=\"0\">"
                    + "<thead>"
                    + "<tr>"
                    + "<th>D</th>"
                    + "<th>S</th>"
                    + "<th>T</th>"
                    + "<th>Q</th>"
                    + "<th>Q</th>"
                    + "<th>S</th>"
                    + "<th>S</th>"
                    + "</tr>"
                    + "</thead>"
                    + "<tbody>"
                    + "</tbody>"
                    + "</table>"
                    + "</div>"
                    + "<div class=\"date-field-contents-footer\">"
                    + "<div class=\"button-previous\"></div>"
                    + "<div class=\"button-next\"></div>"
                    + "<h1><span class=\"button-today active\">Today</span></h1>"
                    + "<div class=\"clear\"></div>" + "</div>";

            // appends the html code to the matched object
            matchedObject.append(htmlCode);

            // iterates over each of the matched objects
            matchedObject.each(function(index, element) {
                        // retrieves the element reference
                        var elementReference = jQuery(element);

                        // retrieves the date field input
                        var dateFieldInput = jQuery(".date-field-input",
                                elementReference);

                        // retrieves the date field input hidden
                        var dateFieldInputHidden = jQuery(
                                ".date-field-input-hidden", elementReference);

                        // tries to retrieve the timestamp value
                        var timestamp = elementReference.attr("timestamp");

                        // in case the timestamp element is set to true
                        if (timestamp == "true") {
                            // sets the timestamp value in the element
                            elementReference.data("timestamp", true)
                        } else {
                            // unsets the timestamp value in the element
                            elementReference.data("timestamp", false)
                        }

                        // tries to retrieve the current date
                        var date = elementReference.attr("date");

                        // in case the date is valid
                        if (date) {
                            // tries to create a date element
                            var dateElement = new Date(date);

                        } else {
                            // creates a new date object with the current date
                            var dateElement = new Date();
                        }

                        // sets the new date element
                        elementReference.data("date", dateElement);

                        // retrieves the element name and tab index
                        var name = elementReference.attr("name");
                        var tabIndex = elementReference.attr("tabindex");

                        // sets both the name and the tab index in the date field
                        // input field, in order to enable form interaction
                        dateFieldInputHidden.attr("name", name);
                        dateFieldInput.attr("tabindex", tabIndex);

                        // removes the element name and tab index
                        elementReference.removeAttr("name");
                        elementReference.removeAttr("tabindex");

                        // updates the date value in the component
                        __updateDate(elementReference);
                    });
        };

        /**
         * Registers the event handlers for the created objects.
         */
        var _registerHandlers = function() {
            // retrieves the date field input
            var dateFieldInput = jQuery(".date-field-input", matchedObject);

            // retrieves the date field button
            var dateFieldButton = jQuery(".date-field-button", matchedObject);

            // retrieves the date field header button next
            var dateFieldHeaderButtonNext = jQuery(
                    ".date-field-contents-header > .button-next", matchedObject);

            // retrieves the date field header button previous
            var dateFieldHeaderButtonPrevious = jQuery(
                    ".date-field-contents-header > .button-previous",
                    matchedObject);

            // retrieves the date field footer button today
            var dateFieldFooterButtonToday = jQuery(
                    ".date-field-contents-footer .button-today", matchedObject);

            dateFieldInput.focus(function(event) {
                        jQuery(this).addClass("active");
                    });

            dateFieldInput.blur(function(event) {
                        jQuery(this).removeClass("active");
                    });

            dateFieldButton.click(function(event) {
                        // retrieves the parent date field
                        var dateField = jQuery(this).parents(".date-field");

                        // retrieves the current date
                        var currentDate = dateField.data("date");

                        // creates a copy of the current date to serve
                        // as the view date
                        var viewDate = new Date(currentDate);

                        // sets the current view date
                        dateField.data("view_date", viewDate);

                        // updates the calendar with the current date
                        __updateCalendar(options, dateField, currentDate);

                        // toggles the date field visibility
                        __toggle(dateField);
                    });

            dateFieldButton.mousedown(function() {
                        // adds the click class
                        jQuery(this).addClass("click");
                    });

            dateFieldButton.mouseup(function() {
                        // removes the click class
                        jQuery(this).removeClass("click");
                    });

            dateFieldHeaderButtonNext.click(function(event) {
                        // retrieves the parent date field
                        var dateField = jQuery(this).parents(".date-field");

                        // retrieves the current date
                        var currentDate = dateField.data("view_date");

                        // retrieves the current month
                        var currentMonth = currentDate.getMonth();

                        // in case the current month is the last one
                        if (currentMonth == 11) {
                            // retrieves the current year
                            var currentYear = currentDate.getFullYear();

                            // increments the current year
                            currentDate.setFullYear(currentYear + 1);

                            // sets the initial month
                            currentDate.setMonth(0);
                        } else {
                            // increments the current month
                            currentDate.setMonth(currentMonth + 1);
                        }

                        // updates the calendar
                        __updateCalendar(options, dateField, currentDate);
                    });

            dateFieldHeaderButtonPrevious.click(function(event) {
                        // retrieves the parent date field
                        var dateField = jQuery(this).parents(".date-field");

                        // retrieves the current date
                        var currentDate = dateField.data("view_date");

                        // retrieves the current month
                        var currentMonth = currentDate.getMonth();

                        // in case the current month is the last one
                        if (currentMonth == 0) {
                            // retrieves the current year
                            var currentYear = currentDate.getFullYear();

                            // increments the current year
                            currentDate.setFullYear(currentYear - 1);

                            // sets the initial month
                            currentDate.setMonth(11);
                        } else {
                            // increments the current month
                            currentDate.setMonth(currentMonth - 1);
                        }

                        // updates the calendar
                        __updateCalendar(options, dateField, currentDate);
                    });

            dateFieldFooterButtonToday.click(function(event) {
                        // retrieves the parent date field
                        var dateField = jQuery(this).parents(".date-field");

                        // retrieves the current date
                        var currentDate = new Date();

                        // updates the calendar
                        __updateCalendar(options, dateField, currentDate);
                    });
        };

        var __toggle = function(dateField) {
            // retrieves the date field contents
            var dateFieldContents = jQuery(".date-field-contents", dateField);

            // toggles the date field contents visibility
            if (dateFieldContents.is(":visible")) {
                // hides the date field
                __hide(dateField);
            } else {
                // shows the date field
                __show(dateField);
            }
        };

        var __show = function(dateField) {
            // retrieves the date field contents
            var dateFieldContents = jQuery(".date-field-contents", dateField);

            // fades the date field contents in
            dateFieldContents.fadeIn(250);
        };

        var __hide = function(dateField) {
            // retrieves the date field contents
            var dateFieldContents = jQuery(".date-field-contents", dateField);

            // fades the date field contents out
            dateFieldContents.fadeOut(150);
        };

        var __updateDate = function(element) {
            // retrieves the date element from the element
            var dateElement = element.data("date");

            // converts the date to string value
            var dateStringValue = __toStringValue(dateElement);

            // converts the date string value to target string value
            var dateTargetStringValue = __toTargetStringValue(element,
                    dateStringValue);

            // updates the date field input with the date string value
            jQuery(".date-field-input", element).attr("value", dateStringValue);

            // updates the date field input hidden with the date target string value
            jQuery(".date-field-input-hidden", element).attr("value",
                    dateTargetStringValue);
        };

        var __updateCalendar = function(options, dateField, date) {
            // retrieves the monts map
            var monthsMap = options["monthsMap"];

            // retrieves the current selected date
            var selectedDate = dateField.data("date");

            // retrieves the current selected year
            var selectedYear = selectedDate.getFullYear();

            // retrieves the current selected month
            var selectedMonth = selectedDate.getMonth();

            // retrieves the year from the date
            var year = date.getFullYear();

            // retrieves the month from the date
            var month = date.getMonth();

            // checks if the current view month is the currently
            // selected one
            if (selectedYear == year && selectedMonth == month) {
                // sets the current month flag
                var currentMonth = true;
            } else {
                // unsets the current month flag
                var currentMonth = false;
            }

            // retrieves the day from the date
            var day = date.getDate();

            // creates the date representing the first day of the month
            var firstDayDate = new Date(year, month, 1);

            // creates the date representing the last day of the month
            var lastDayDate = new Date(year, month + 1, 0);

            // creates the date representing the last day of the previous month
            var lastDayPreviousMonthDate = new Date(year, month, 0);

            // retrieves the index of the last day of the current month
            var lastIndex = lastDayDate.getDate() + 1;

            // retrieves the first day of the mont (week day)
            var firstDay = firstDayDate.getDay();

            // retrieves the index of the last day of the previous month
            var lastPreviousIndex = lastDayPreviousMonthDate.getDate() + 1;

            // starts the string buffer
            var stringBuffer = new StringBuffer();

            // sets the initial week day
            var weekDay = 0;

            // sets the initial week count
            var weekCount = 0;

            // adds the initial table row to the string buffer
            stringBuffer.append("<tr class=\"first\">");

            // iterates over all the days in the "first" week
            // until it reaches the initial day
            for (var index = 0; index < firstDay; index++) {
                // calculates the delta initial index, the previous
                // month day value
                var deltaInitialIndex = lastPreviousIndex - (firstDay - index);

                // adds the table item
                stringBuffer.append("<td>" + deltaInitialIndex + "</td>");

                // increments the current week day
                weekDay++;
            }

            // iterates over all the days of the current month
            for (var index = 1; weekCount < 5; index++) {
                // in case it's the last week day (saturday)
                if (weekDay == 7) {
                    // closes the table row
                    stringBuffer.append("</tr>");

                    // in case it's the final week
                    if (weekCount == 4) {
                        // adds the last table row
                        stringBuffer.append("<tr class=\"last\">");
                    } else {
                        // adds a new table row
                        stringBuffer.append("<tr>");
                    }

                    // resets the week day
                    weekDay = 0;

                    // increments the week count
                    weekCount++;
                }

                // increments the week day
                weekDay++;

                // in case the index exceeded the number
                // of days for the current month
                if (index >= lastIndex) {
                    // calculates the delta final index, the next
                    // month day value
                    var deltaFinalIndex = index - lastIndex + 1;

                    // adds the empty table item
                    stringBuffer.append("<td>" + deltaFinalIndex + "</td>");

                    // continues the loop
                    continue;
                }

                // creates the date value for the current element
                var dateValue = year + "/" + (month + 1) + "/" + index;

                // in case it's the current selected
                if (currentMonth && index == day) {
                    stringBuffer.append("<td class=\"today\">");
                } else {
                    stringBuffer.append("<td>");
                }

                // adds the table item
                stringBuffer.append("<span class=\"active\" date=\""
                        + dateValue + "\">" + index + "</span></td>");
            }

            // starts the delta final index value
            var deltaFinalIndex = deltaFinalIndex ? deltaFinalIndex + 1 : 1;

            // iterates over all the remaining week days
            for (var index = weekDay; index < 7; index++) {
                // adds the table item
                stringBuffer.append("<td>" + deltaFinalIndex + "</td>");

                // increments the
                deltaFinalIndex++;
            }

            // closes the last table row
            stringBuffer.append("</tr>");

            // retrieves the string value from the string buffer
            var stringValue = stringBuffer.toString();

            // retrieves the date fiel table body
            var dateFieldTableBody = jQuery(
                    ".date-field-contents-body > table > tbody", dateField);

            // retrieves the date field title
            var dateFieldTitle = jQuery(".date-field-contents-header > h1",
                    dateField);

            // clears the current date field table body
            dateFieldTableBody.empty();

            // adds the string value to the date field table body
            dateFieldTableBody.append(stringValue);

            // retrieves the month name
            var monthName = monthsMap[month];

            // creates the top label, using the month name
            // and the year value
            var topLabel = monthName + " " + year;

            // sets the top label in the date field title
            dateFieldTitle.html(topLabel);

            var dateFieldTableBodyActiveElements = jQuery(
                    ".date-field-contents-body > table > tbody span.active",
                    dateField);

            dateFieldTableBodyActiveElements.click(function() {
                        // retrieves the date value from the element
                        var elementDate = jQuery(this).attr("date");

                        // sets the new date element
                        dateField.data("date", new Date(elementDate));

                        // updates the date value in the component
                        __updateDate(dateField);

                        // hides the date field
                        __hide(dateField);
                    });
        };

        var __toTargetStringValue = function(element, dateStringValue) {
            // tries to retrieve the timestamp value
            var timestamp = element.data("timestamp")

            // in case the timestamp flag is active
            if (timestamp) {
                // creates the date timestamp from the date string value
                var dateTimestamp = Date.parse(dateStringValue) / 1000;

                // returns the date timestamp
                return dateTimestamp;
            }

            // returns the (default) date stirng value
            return dateStringValue;
        };

        var __toStringValue = function(dateValue) {
            // retrieves the year
            var year = dateValue.getFullYear();

            // retrieves the month
            var month = dateValue.getMonth() + 1;

            // retrieves the day
            var day = dateValue.getDate();

            // creates the month string
            var monthString = String(month);

            // creates the day string
            var dayString = String(day);

            if (monthString.length == 1) {
                monthString = "0" + monthString;
            }

            if (dayString.length == 1) {
                dayString = "0" + dayString;
            }

            return year + "/" + monthString + "/" + dayString
        };

        // initializes the plugin
        initialize();

        // returns the object
        return this;
    };
})(jQuery);

(function($) {
    jQuery.fn.dropbox = function(options) {
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
            // creates the string with the html code
            var htmlCode = "<input class=\"dropbox-text-input\" />"
                    + "<div class=\"dropbox-container\">"
                    + "<div class=\"dropbox-text-field\">"
                    + "<span class=\"dropbox-value\"></span>"
                    + "<div class=\"dropbox-button\"></div>" + "</div>"
                    + "</div>";

            // prepends the html code to the matched object
            matchedObject.prepend(htmlCode);

            matchedObject.each(function(index, element) {
                        // retrieves the element reference from the element
                        var elementReference = jQuery(element);

                        // retrieves the dropbox text input
                        var dropboxTextInput = jQuery(".dropbox-text-input",
                                elementReference);

                        // retrieves the value from the element reference
                        var value = elementReference.attr("value");

                        // retrieves the element name and tab index
                        var name = elementReference.attr("name");
                        var tabIndex = elementReference.attr("tabindex");

                        // sets both the name and the tab index in the dropbox
                        // text input field, in order to enable form interaction
                        dropboxTextInput.attr("name", name);
                        dropboxTextInput.attr("tabindex", tabIndex);

                        // removes the element name and tab index
                        elementReference.removeAttr("name");
                        elementReference.removeAttr("tabindex");

                        if (value) {
                            // retrieves the list element
                            var listElement = jQuery("li[name=" + value + "]",
                                    elementReference)

                            // changes the selection
                            __changeSelection(listElement);
                        }
                    });
        };

        /**
         * Registers the event handlers for the created objects.
         */
        var _registerHandlers = function() {
            matchedObject.keydown(function(event) {
                // retrieves the dropbox
                var dropbox = jQuery(this);

                // retrieves the dropbox contents selected list element
                var dropboxContentsListSelectedElement = jQuery(
                        ".dropbox-contents li.selected", dropbox);

                // in case it's the down arrow or the left arrow
                if (event.keyCode == 37 || event.keyCode == 38) {
                    __changeSelection(dropboxContentsListSelectedElement.prev());
                }
                // in case it's the up arrow or the right arrow
                else if (event.keyCode == 39 || event.keyCode == 40) {
                    __changeSelection(dropboxContentsListSelectedElement.next());
                }
                // in case it's the page up or home
                else if (event.keyCode == 33 || event.keyCode == 36) {
                    __changeSelection(jQuery(":first",
                            dropboxContentsListSelectedElement.parent()));
                }
                // in case it's the page down or end
                else if (event.keyCode == 34 || event.keyCode == 35) {
                    __changeSelection(jQuery(":last",
                            dropboxContentsListSelectedElement.parent()));
                }

                // retrieves the char value from the key code, and converts it
                // to upper case
                var charValue = String.fromCharCode(event.keyCode);
                var upperCharValue = charValue.toUpperCase();

                // retrieves all the list element for the current char key
                var dropboxContentsListSelectedElement = jQuery(
                        ".dropbox-contents li[name^=" + charValue
                                + "], .dropbox-contents li[name^="
                                + upperCharValue + "]", dropbox);

                // in case there are valid element selected
                if (dropboxContentsListSelectedElement.size() > 0) {
                    // changes the selection to the first (best) list element
                    __changeSelection(jQuery(dropboxContentsListSelectedElement.get(0)));
                }
            });

            jQuery(".dropbox-text-input", matchedObject).focus(function() {
                        // retrieves the parent dropbox
                        var dropbox = jQuery(this).parents(".dropbox");

                        // adds the active class from the dropbox
                        dropbox.addClass("active");
                    });

            jQuery(".dropbox-text-input", matchedObject).blur(function() {
                        // retrieves the parent dropbox
                        var dropbox = jQuery(this).parents(".dropbox");

                        // removes the active class from the dropbox
                        dropbox.removeClass("active");
                    });

            jQuery(".dropbox-text-field", matchedObject).click(function() {
                        // retrieves the parent dropbox
                        var dropbox = jQuery(this).parents(".dropbox");

                        // retrieves the dropbox contents
                        var dropboxContents = jQuery(".dropbox-contents",
                                dropbox);

                        // retrieves the current dropbox contents height
                        var dropboxContentsHeight = dropboxContents.height();

                        // creates the margin bottom value
                        var maginBottomValue = (dropboxContentsHeight + 2) * -1
                                + "px";

                        // sets the margin bottom in the dropbox contents
                        dropboxContents.css("margin-bottom", maginBottomValue);

                        // togles the dropbox visibility
                        __toggle(dropbox);
                    });

            jQuery("li", matchedObject).click(function() {
                        // retrieves the list element
                        var listElement = jQuery(this);

                        // retrieves the parent dropbox
                        var dropbox = listElement.parents(".dropbox");

                        // changes the selection to the given list element
                        __changeSelection(listElement);

                        // hides the dropbox
                        __hide(dropbox);
                    });

            jQuery(".dropbox-button", matchedObject).mousedown(function() {
                        // adds the click class
                        jQuery(this).addClass("click");
                    });

            jQuery(".dropbox-button", matchedObject).mouseup(function() {
                        // removes the click class
                        jQuery(this).removeClass("click");
                    });
        };

        var __changeSelection = function(listElement) {
            // retrieves the current value
            var currentValue = listElement.html();

            // retrieves the current name
            var currentName = listElement.attr("name");

            // retrieves the current offset
            var currentOffset = listElement.offset();

            // retrieves the parent dropbox
            var dropbox = listElement.parents(".dropbox");

            // retrieves the dropbox contents
            var dropboxContents = jQuery(".dropbox-contents", dropbox);

            // retrieves the dropbox value
            var dropboxValue = jQuery(".dropbox-value", dropbox);

            // retrieves the dropbox text input
            var dropboxTextInput = jQuery(".dropbox-text-input", dropbox);

            // retrieves the dropbox contents selected list elements
            var dropboxContentsListSelectedElements = jQuery("li.selected",
                    dropboxContents);

            // retrieves the current scroll top
            var dropboxContentsScrollTop = dropboxContents.scrollTop();

            // sets the current value in the dropbox value
            dropboxValue.html(currentValue);

            // sets the current name in the dropbox value
            dropboxValue.attr("name", currentName);

            // sets the current name in the dropbbox text input
            dropboxTextInput.attr("value", currentName);

            // sets the current scroll top in the dropbox contents
            dropboxContents.data("scroll_top", dropboxContentsScrollTop);

            // removes the selected class from all selected list elements
            dropboxContentsListSelectedElements.removeClass("selected");

            // adds the selected class to the list element
            listElement.addClass("selected");
        };

        var __toggle = function(dropbox) {
            // retrieves the dropbox contents
            var dropboxContents = jQuery(".dropbox-contents", dropbox);

            // toggles the dropbox contents visibility
            if (dropboxContents.is(":visible")) {
                // hides the dropbox
                __hide(dropbox);
            } else {
                // shows the dropbox
                __show(dropbox);
            }
        };

        var __show = function(dropbox) {
            // retrieves the dropbox contents
            var dropboxContents = jQuery(".dropbox-contents", dropbox);

            // retrieves the dropbox contents scrolll top
            var dropboxContentsScrollTop = dropboxContents.data("scroll_top");

            // shows the dropbox contents
            dropboxContents.show();

            // in case the dropbox contents scroll top is defined
            if (dropboxContentsScrollTop) {
                // scroll the dropx box contents
                dropboxContents.scrollTop(dropboxContentsScrollTop);
            }
        };

        var __hide = function(dropbox) {
            // retrieves the dropbox contents
            var dropboxContents = jQuery(".dropbox-contents", dropbox);

            // fades the dropbox contents in
            dropboxContents.fadeOut(150);
        };

        // initializes the plugin
        initialize();

        // returns the object
        return this;
    };
})(jQuery);

(function($) {
    jQuery.fn.message = function(method, options) {
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
            // creates the string with the html code
            var htmlCode = "<div class=\"message-container\">"
                    + "<div class=\"message-icon\"></div>"
                    + "<div class=\"message-contents\"></div>"
                    + "<div class=\"message-button\"></div>"
                    + "<div class=\"clear\"></div>" + "</div>";

            // iterates over all the matched objects
            matchedObject.each(function(index, element) {
                        // retrives the element reference
                        var elementReference = jQuery(element);

                        // retrieves the contents code from the element
                        var contentsCode = elementReference.html();

                        // clears the element
                        elementReference.empty();

                        // appends the html code to the element
                        elementReference.append(htmlCode);

                        // retrieves the message contents
                        var messageContents = jQuery(".message-contents",
                                elementReference);

                        // sets the message contents code
                        messageContents.html(contentsCode);
                    });
        };

        /**
         * Registers the event handlers for the created objects.
         */
        var _registerHandlers = function() {
            jQuery(".message-button", matchedObject).click(function(event) {
                        // retrieves the parent message
                        var message = jQuery(this).parents(".message");

                        // toggles the message
                        __toggle(message);
                    });
        };

        var _show = function(matchedObject, options) {
            // tries to retrieve the timeout from the options
            var timeout = options["timeout"];

            // shows the message
            __show(matchedObject);

            // in case a timeout is set
            if (timeout) {
                // sets a timeout to hide the message
                setTimeout(function() {
                            // hides the message
                            __hide(matchedObject);
                        }, timeout);
            }
        };

        var _hide = function(matchedObject, options) {
            __hide(matchedObject);
        };

        var __toggle = function(message) {
            // toggles the message visibility
            if (message.is(":visible")) {
                // hides the message
                __hide(message);
            } else {
                // shows the message
                __show(message);
            }
        };

        var __show = function(message) {
            // fades the message in
            message.fadeIn(350);
        };

        var __hide = function(message) {
            // fades the message in
            message.fadeOut(250);
        };

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
    jQuery.fn.window = function(method, options) {
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

        var _show = function(matchedObject, options) {
            // tries to retrieve the timeout from the options
            var timeout = options["timeout"];

            // shows the window
            __show(matchedObject);

            // in case a timeout is set
            if (timeout) {
                setTimeout(function() {
                            __hide(matchedObject);
                        }, timeout);
            }
        };

        var _hide = function(matchedObject, options) {
            __hide(matchedObject);
        };

        var __toggle = function(message) {
            // toggles the message visibility
            if (message.is(":visible")) {
                // hides the message
                __hide(message);
            } else {
                // shows the message
                __show(message);
            }
        };

        var __show = function(message) {
            // fades the message in
            message.fadeIn(350);
        };

        var __hide = function(message) {
            // fades the message in
            message.fadeOut(250);
        };

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
    jQuery.fn.notificationarea = function(options) {
        // the default values for the plugin
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
        };

        /**
         * Registers the event handlers for the created objects.
         */
        var _registerHandlers = function() {
            // retrieves the window
            var _window = jQuery(window);

            // registers for the scroll event
            _window.scroll(function(event) {
                        // scrolls the notification area
                        _scrollNotificationArea(matchedObject, options);
                    });
        };

        /**
         * Scrolls the notification area according to the current window
         * position.
         *
         * @param {Element}
         *            matchedObject The mathched object.
         * @param {Map}
         *            options The options of the plugin instance.
         */
        var _scrollNotificationArea = function(matchedObject, options) {
            // retrieves the window
            var _window = jQuery(window);

            // retrieves the window scroll top
            var windowScrollTop = _window.scrollTop();

            // sets the notification area top position
            matchedObject.css("top", windowScrollTop);
        };

        // initializes the plugin
        initialize();

        // returns the object
        return this;
    };
})(jQuery);

(function($) {
    jQuery.fn.notificationwindow = function(method, options) {
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
            // retrieves the title
            var title = options["title"];

            // retrieves the sub title
            var subTitle = options["subTitle"];

            // retrieves the message
            var message = options["message"];

            // retrieves the icon
            var icon = options["icon"];

            // tries to retrieve the timeout from the options
            var timeout = options["timeout"];

            // retrieves the success callback functions
            var successCallbackFunctions = options["successCallbackFunctions"];

            // retrieves the error callback functions
            var errorCallbackFunctions = options["errorCallbackFunctions"];

            // creates the string with the html code
            var htmlCode = "<div class=\"window notification-message\">"
                    + "<div class=\"window-header\">"
                    + "<div class=\"window-button-close\"></div>";

            // in case an icon is defined
            if (icon) {
                htmlCode += "<div class=\"window-header-icon\">" + ""
                        + "<img src=\"" + icon
                        + "\" height=\"48\" width=\"48\" alt=\"Receipt\" />"
                        + "</div>";
            }

            // adds the last part of the html code
            htmlCode += "<div class=\"window-header-content\">" + "<h1>"
                    + title + "</h1>" + "<h2>" + subTitle + "</h2>" + "</div>"
                    + "<div class=\"clear\"></div>" + "</div>"
                    + "<div class=\"panel-container\">"
                    + "<div class=\"panel-content\">"
                    + "<div class=\"panel-message\">" + message + "</div>"
                    + "</div>" + "<div class=\"clear\"></div>" + "</div>"
                    + "</div>";

            // adds the code to the matched object
            matchedObject.append(htmlCode);

            // retrieves the notification window
            var notificationMessage = jQuery(".notification-message:last",
                    matchedObject);

            // sets the callbacks in the notification message
            notificationMessage.data("success_callback_functions",
                    successCallbackFunctions);
            notificationMessage.data("error_callback_functions",
                    errorCallbackFunctions);

            // fades in the notification message
            notificationMessage.fadeIn(500);

            // in case a timeout is set
            if (timeout) {
                // sets a timeout to hide the notification window
                setTimeout(function() {
                            // closes the notification window
                            _close(notificationMessage, options);
                        }, timeout);
            }
        };

        /**
         * Registers the event handlers for the created objects.
         */
        var _registerHandlers = function() {
            // retrieves the notification window
            var notificationMessage = jQuery(".notification-message",
                    matchedObject);

            jQuery(".button-green", notificationMessage).click(function(event) {
                // retrieves the notification message
                var notificationMessage = jQuery(this).parents(".notification-message");

                // closes the notification message and calls the success callbacks
                _close(notificationMessage, options);
                __callSuccessCallbacks(notificationMessage, options);
            });

            jQuery(".window-button-close, .button-blue", notificationMessage).click(
                    function(event) {
                        // retrieves the notification message
                        var notificationMessage = jQuery(this).parents(".notification-message");

                        // closes the notification message and calls the error callbacks
                        _close(notificationMessage, options);
                        __callErrorCallbacks(notificationMessage, options);
                    });
        };

        var _close = function(notificationMessage, options) {
            // fades out the notification window
            notificationMessage.fadeOut(400, function() {
                        // removes the notification window
                        notificationMessage.remove();
                    });
        };

        var __callSuccessCallbacks = function(notificationMessage, options) {
            // retrieves the success callback functions
            var successCallbackFunctions = notificationMessage.data("success_callback_functions");

            // sets the default success callback functions
            successCallbackFunctions = successCallbackFunctions
                    ? successCallbackFunctions
                    : [];

            // iterates over all the success callback functions
            jQuery(successCallbackFunctions).each(function(index, element) {
                        // calls the callback function
                        element();
                    });
        };

        var __callErrorCallbacks = function(notificationMessage, options) {
            // retrieves the error callback functions
            var errorCallbackFunctions = notificationMessage.data("error_callback_functions");

            // sets the default error callback functions
            errorCallbackFunctions = errorCallbackFunctions
                    ? errorCallbackFunctions
                    : [];

            // iterates over all the error callback functions
            jQuery(errorCallbackFunctions).each(function(index, element) {
                        // calls the callback function
                        element();
                    });
        };

        // switches over the method
        switch (method) {
            case "close" :
                _close(matchedObject, options);
                __callErrorCallbacks(matchedObject, options);
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
    jQuery.fn.messagewindow = function(method, options) {
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
            // retrieves the title
            var title = options["title"];

            // retrieves the sub title
            var subTitle = options["subTitle"];

            // retrieves the message
            var message = options["message"];

            // retrieves the centered
            var centered = options["centered"];

            // retrieves the icon
            var icon = options["icon"];

            // creates the string with the html code
            var htmlCode = "<div class=\"absolute window message-message\">"
                    + "<div class=\"window-header\">";

            // in case an icon is defined
            if (icon) {
                htmlCode += "<div class=\"window-header-icon\">" + ""
                        + "<img src=\"" + icon
                        + "\" height=\"48\" width=\"48\" alt=\"Receipt\" />"
                        + "</div>";
            }

            // adds the last part of the html code
            htmlCode += "<div class=\"window-header-content\">" + "<h1>"
                    + title + "</h1>" + "<h2>" + subTitle + "</h2>" + "</div>"
                    + "<div class=\"clear\"></div>" + "</div>"
                    + "<div class=\"panel-container\">"
                    + "<div class=\"panel-content\">"
                    + "<div class=\"panel-message\">" + message + "</div>"
                    + "</div>" + "<div class=\"clear\"></div>" + "</div>"
                    + "</div>";

            // adds the code to the matched object
            matchedObject.append(htmlCode);

            // retrieves the message window
            var messageMessage = jQuery(".message-message:last", matchedObject);

            // retrieves the matched object dimensions
            var matchedObjectHeight = matchedObject.height();
            var matchedObjectWidth = matchedObject.width();

            // retrieves the message window dimensions
            var messageMessageHeight = messageMessage.height();
            var messageMessageWidth = messageMessage.width();

            // sets the message window position, according to the
            // matched object height and width
            messageMessage.css("top", 180);
            messageMessage.css("left", (matchedObjectWidth / 2)
                            - (messageMessageWidth / 2));

            // fades in the message message
            messageMessage.fadeIn(500);

            // sets the overlay to be shown
            jQuery("#overlay").overlay("show");

            // scrolls to the message window
            jQuery.scrollTo(messageMessage, 800, {
                        offset : {
                            top : -250,
                            left : 0
                        }
                    });
        };

        /**
         * Registers the event handlers for the created objects.
         */
        var _registerHandlers = function() {
        };

        var _close = function(matchedObject, options) {
            // retrieves the message window
            var messageMessage = jQuery(".message-message", matchedObject);

            // sets the overlay to be hidden
            jQuery("#overlay").overlay("hide");

            // fades out the message window
            messageMessage.fadeOut(400, function() {
                        // removes the message window
                        messageMessage.remove();
                    });
        };

        // switches over the method
        switch (method) {
            case "close" :
                _close(matchedObject, options);
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
    jQuery.fn.dialogwindow = function(method, options) {
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
            // retrieves the title
            var title = options["title"];

            // retrieves the sub title
            var subTitle = options["subTitle"];

            // retrieves the message
            var message = options["message"];

            // retrieves the button message
            var buttonMessage = options["buttonMessage"];

            // retrieves the centered
            var centered = options["centered"];

            // retrieves the icon
            var icon = options["icon"];

            // retrieves the success callback functions
            var successCallbackFunctions = options["successCallbackFunctions"];

            // retrieves the error callback functions
            var errorCallbackFunctions = options["errorCallbackFunctions"];

            // creates the string with the html code
            var htmlCode = "<div class=\"absolute window dialog-message\">"
                    + "<div class=\"window-header\">"
                    + "<div class=\"window-button-close\"></div>";

            // in case an icon is defined
            if (icon) {
                htmlCode += "<div class=\"window-header-icon\">" + ""
                        + "<img src=\"" + icon
                        + "\" height=\"48\" width=\"48\" alt=\"Receipt\" />"
                        + "</div>";
            }

            // adds the last part of the html code
            htmlCode += "<div class=\"window-header-content\">" + "<h1>"
                    + title + "</h1>" + "<h2>" + subTitle + "</h2>" + "</div>"
                    + "<div class=\"clear\"></div>" + "</div>"
                    + "<div class=\"panel-container\">"
                    + "<div class=\"panel-content\">"
                    + "<div class=\"panel-message\">" + message + "</div>"
                    + "</div>" + "<div class=\"window-button-area\">"
                    + "<div class=\"button-message\" >" + buttonMessage
                    + "</div>"
                    + "<div class=\"button button-blue\" >Cancel</div>"
                    + "<div class=\"button button-green\" >Confirm</div>"
                    + "</div>" + "<div class=\"clear\"></div>" + "</div>"
                    + "</div>";

            // adds the code to the matched object
            matchedObject.append(htmlCode);

            // retrieves the dialog window
            var dialogMessage = jQuery(".dialog-message:last", matchedObject);

            // sets the callbacks in the dialog message
            dialogMessage.data("success_callback_functions",
                    successCallbackFunctions);
            dialogMessage.data("error_callback_functions", errorCallbackFunctions);

            // retrieves the matched object dimensions
            var matchedObjectHeight = matchedObject.height();
            var matchedObjectWidth = matchedObject.width();

            // retrieves the dialog window dimensions
            var dialogMessageHeight = dialogMessage.height();
            var dialogMessageWidth = dialogMessage.width();

            // sets the dialog window position, according to the
            // matched object height and width
            dialogMessage.css("top", 180);
            dialogMessage.css("left", (matchedObjectWidth / 2)
                            - (dialogMessageWidth / 2));

            // fades in the dialog message
            dialogMessage.fadeIn(500);

            // sets the overlay to be shown
            jQuery("#overlay").overlay("show");

            // scrolls to the dialog window
            jQuery.scrollTo(dialogMessage, 800, {
                        offset : {
                            top : -250,
                            left : 0
                        }
                    });
        };

        /**
         * Registers the event handlers for the created objects.
         */
        var _registerHandlers = function() {
            // retrieves the dialog window
            var dialogMessage = jQuery(".dialog-message", matchedObject);

            // registers the dialog message buttons
            jQuery(".button", dialogMessage).button();

            jQuery(".button-green", dialogMessage).click(function(event) {
                        _close(matchedObject, options);
                        __callSuccessCallbacks(matchedObject, options);
                    });

            jQuery(".window-button-close, .button-blue", dialogMessage).click(
                    function(event) {
                        _close(matchedObject, options);
                        __callErrorCallbacks(matchedObject, options);
                    });
        };

        var _close = function(matchedObject, options) {
            // retrieves the dialog window
            var dialogMessage = jQuery(".dialog-message", matchedObject);

            // sets the overlay to be hidden
            jQuery("#overlay").overlay("hide");

            // fades out the dialog window
            dialogMessage.fadeOut(400, function() {
                        // removes the dialog window
                        dialogMessage.remove();
                    });
        };

        var __callSuccessCallbacks = function(matchedObject, options) {
            // retrieves the dialog message
            var dialogMessage = jQuery(".dialog-message", matchedObject);

            // retrieves the success callback functions
            var successCallbackFunctions = dialogMessage.data("success_callback_functions");

            // sets the default success callback functions
            successCallbackFunctions = successCallbackFunctions
                    ? successCallbackFunctions
                    : [];

            // iterates over all the success callback functions
            jQuery(successCallbackFunctions).each(function(index, element) {
                        // calls the callback function
                        element();
                    });
        };

        var __callErrorCallbacks = function(matchedObject, options) {
            // retrieves the dialog message
            var dialogMessage = jQuery(".dialog-message", matchedObject);

            // retrieves the error callback functions
            var errorCallbackFunctions = dialogMessage.data("error_callback_functions");

            // sets the default error callback functions
            errorCallbackFunctions = errorCallbackFunctions
                    ? errorCallbackFunctions
                    : [];

            // iterates over all the error callback functions
            jQuery(errorCallbackFunctions).each(function(index, element) {
                        // calls the callback function
                        element();
                    });
        };

        // switches over the method
        switch (method) {
            case "close" :
                _close(matchedObject, options);
                __callErrorCallbacks(matchedObject, options);
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
    jQuery.fn.progressindicator = function(method, options) {
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
            // creates the string with the html code
            var htmlCode = "<div class=\"progress-indicator-bar\"></div>"
                    + "<div class=\"progress-indicator-value\">0%</div>";

            // appends the html code to the matched object
            matchedObject.append(htmlCode);
        };

        /**
         * Registers the event handlers for the created objects.
         */
        var _registerHandlers = function() {
        };

        var __changePercentage = function(matchedObject, options) {
            // retrieves the percentage value
            var percentage = options["percentage"];

            // sets the percentage in the progress indicator bar
            jQuery(".progress-indicator-bar", matchedObject).css("width",
                    percentage + "%");

            // sets the percentage value in the indicator
            jQuery(".progress-indicator-value", matchedObject).html(percentage
                    + "%");

            // in case the percentage is bigger than the minimum
            if (percentage > 55) {
                jQuery(".progress-indicator-value", matchedObject).addClass("white");
            }
        };

        // switches over the method
        switch (method) {
            case "change" :
                __changePercentage(matchedObject, options);
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
    jQuery.fn.overlay = function(method, options) {
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
            // adds the overlay class to the matched object
            matchedObject.addClass("overlay");
        };

        /**
         * Registers the event handlers for the created objects.
         */
        var _registerHandlers = function() {
        };

        var _toggle = function(matchedObject, options) {
            // in case the matched object is not visible
            if (matchedObject.is(":visible")) {
                // hides the overlay
                _hide(matchedObject, options);
            } else {
                // shows the overlay
                _show(matchedObject, options);
            }
        };

        var _show = function(matchedObject, options) {
            // sets the document height and widht in
            // the matched object
            matchedObject.height(jQuery(document).height());
            matchedObject.width(jQuery(document).width());

            // shows the matched options object
            matchedObject.fadeIn(250);
        };

        var _hide = function(matchedObject, options) {
            // hides the matched object
            matchedObject.fadeOut(100);
        };

        // switches over the method
        switch (method) {
            case "toggle" :
                _toggle(matchedObject, options);
                break;

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
    jQuery.fn.searchtable = function(options) {
        // the enter key code
        var ENTER = 13;

        // the default values for the menu
        var defaults = {
            numberRecords : 15
        };

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
            _startSearch();
        };

        /**
         * Creates the necessary html for the component.
         */
        var _appendHtml = function() {
            // creates the html code
            var htmlCode = "<div class=\"search-field\" id=\"search-list-field\">"
                    + "<input class=\"text\" name=\"search_query\" id=\"search-query\" type=\"text\" />"
                    + "<div class=\"search-button\"></div>" + "</div>";

            // prepends the html to the matched object
            matchedObject.prepend(htmlCode);

            // retrieves the search query element
            var searchQuery = jQuery("#search-query", matchedObject);

            // creates the text area
            searchQuery.textarea();

            // resets the table search
            __resetTableSearch(matchedObject);
        };

        /**
         * Registers the event handlers for the created objects.
         */
        var _registerHandlers = function() {
            // registers the handler for the next button
            jQuery("#search-query", matchedObject).keydown(function(event) {
                        var keyCode = event.keyCode;

                        if (keyCode == ENTER) {
                            // retrieves the searcg table field
                            var searchTable = jQuery(this).parents(".search-table");

                            // resets the table search
                            __resetTableSearch(searchTable);

                            // performs the search
                            _search(searchTable, options, false);
                        }
                    });

            // registers the handler for the key event in the search query field
            jQuery("#search-query", matchedObject).keyup(function(event) {
                        // retrieves the searcg table field
                        var searchTable = jQuery(this).parents(".search-table");

                        // resets the table search
                        __resetTableSearch(searchTable);

                        // performs the search
                        _search(searchTable, options, false);
                    });
        };

        /**
         * Performs the first and initial search.
         */
        var _startSearch = function() {
            // iterates over all the element in the matched object
            matchedObject.each(function(index, element) {
                        _search(jQuery(element), options, false);
                    });
        };

        var _search = function(searchTable, options, update) {
            // retrueves the search query
            var searchQuery = jQuery("#search-query", searchTable);

            // retrueves the table
            var table = jQuery("table", searchTable);

            // retrieves the provider url
            var providerUrl = searchTable.attr("provider_url");

            // retrieves the number of records
            var numberRecords = options["numberRecords"];

            // retrieves the current search query value
            var searchQueryValue = searchQuery.attr("value");

            // retrieves the current final record
            var currentFinalRecord = table.data("current_final_record",
                    currentFinalRecord);

            // assembles the form data to submit with the search button click event
            var searchButtonData = {
                search_query : searchQueryValue,
                start_record : currentFinalRecord,
                number_records : numberRecords
            };

            // processes the ajax request
            jQuery.ajax({
                        url : providerUrl,
                        type : "get",
                        data : searchButtonData,
                        success : function(data) {
                            _partialCallback(searchTable, options, data, update);
                        }
                    });
        };

        var _partialCallback = function(searchTable, options, data, update) {
            // retrieves the data element
            var dataElement = jQuery(data);

            // retrieves the table body data
            var tableBody = jQuery("#table-body", dataElement);

            // retrieves the table metadata data
            var tableMetadata = jQuery("#meta-data", dataElement);

            // triggers the content change event
            searchTable.trigger("content_change", [tableBody])

            if (update) {
                jQuery("tbody", searchTable).append(jQuery("tr", tableBody));
            } else {
                // replaces the table body contents
                jQuery("tbody", searchTable).replaceWith(tableBody);
            }

            // retrieves the number of records retrieves
            var numberRecords = parseInt(jQuery("#number-records",
                    tableMetadata).html());
            var totalNumberRecords = parseInt(jQuery("#total-number-records",
                    tableMetadata).html());

            // sets the initial table data
            var currentFinalRecord = jQuery("table", searchTable).data("current_final_record");
            currentFinalRecord += numberRecords;

            // removes the more button
            jQuery("#more-button", searchTable).remove();

            // in case the current final record is smaller
            // than the total number of records
            if (currentFinalRecord < totalNumberRecords) {
                // creates the button html code
                var htmlCode = "<div id=\"more-button\" class=\"button button-green center\">More</div>";

                // appends the button html code
                jQuery(searchTable).append(htmlCode);

                // retrieves the more button
                var moreButton = jQuery("#more-button", searchTable);

                // creates the more button
                moreButton.button();

                // register the click callback for the more button
                moreButton.click(function() {
                            // performs the search
                            _search(searchTable, options, true);
                        });
            }

            // sets the new table values
            jQuery("table", searchTable).data("current_final_record",
                    currentFinalRecord);
            jQuery("table", searchTable).data("total_number_records",
                    totalNumberRecords);

            // updates the main container (size)
            jQuery("#main-container").maincontainer("update");

            // in case the update flag is set
            if (update) {
                // retrieves the table footer
                var tableFooter = jQuery("table > tfoot", searchTable);

                // retrieves the current window (viewport) height
                var windowHeight = jQuery(window).height();

                // calculates the offset to the top to be used
                var offsetTop = (windowHeight - 46) * -1;

                // scrolls to the table footer
                jQuery.scrollTo(tableFooter, 400, {
                            offset : {
                                top : offsetTop,
                                left : 0
                            }
                        });
            }
        };

        var __resetTableSearch = function(targetElement) {
            // sets the initial table data
            jQuery("table", targetElement).data("current_final_record", 0);
            jQuery("table", targetElement).data("total_number_records", 0);
        };

        var __baseTableHandlers = function(targetElement) {

        };

        // initializes the plugin
        initialize();

        // returns the object
        return this;
    };
})(jQuery);
