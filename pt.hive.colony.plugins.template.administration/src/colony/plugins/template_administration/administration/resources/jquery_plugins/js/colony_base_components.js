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
// __revision__  = $LastChangedRevision: 684 $
// __date__      = $LastChangedDate: 2008-12-08 15:16:55 +0000 (seg, 08 Dez 2008) $
// __copyright__ = Copyright (c) 2008 Hive Solutions Lda.
// __license__   = GNU General Public License (GPL), Version 3

(function($) {
    /**
     * Creates a new colony text box in the given input element.
     *
     * @param {Map}
     *            options The options for the colony text box creation.
     */
    $.fn.colonyTextBox = function(options) {
        // completes the options appending the defaults and the argument options
        var completeOptions = $.extend({}, $.fn.colonyTextBox.defaults, options);

        // selects the element
        var $this = $(this);

        // adds the colony text box class
        $this.addClass("colony-text-box");

        // in case the size property is defined
        if (completeOptions["size"]) {
            // retrieves the size property
            var colonyTextBoxSize = completeOptions["size"];

            // switches in the size property
            switch (colonyTextBoxsize) {
                // in case the size is small
                case ("small") :
                    $this.addClass("colony-text-box-small");
                    break;
                // in case the size is normal
                case ("normal") :
                    $this.addClass("colony-text-box-normal");
                    break;
                // in case the size is large
                case ("large") :
                    $this.addClass("colony-text-box-large");
                    break;
            }
        }
    };

    /**
     * The default options for the colony text box.
     *
     * @type Map
     */
    $.fn.colonyTextBox.defaults = {
        size : "normal"
    };

    /**
     * Creates a new colony button in the given span element.
     *
     * @param {String}
     *            text The text for the colony button.
     * @param {Map}
     *            options The options for the colony button creation.
     */
    $.fn.colonyButton = function(text, options) {
        // completes the options appending the defaults and the argument options
        var completeOptions = $.extend({}, $.fn.colonyButton.defaults, options);

        // sets the has image flag as false
        var hasImage = false;

        // selects the element
        var $this = $(this);

        // adds the colony text box class
        $this.addClass("colony-button");

        // in case the size property is defined
        if (completeOptions["size"]) {
            // retrieves the size property
            var colonyButtonSize = completeOptions["size"];

            // switches in the size property
            switch (colonyButtonSize) {
                // in case the size is small
                case ("small") :
                    $this.addClass("colony-button-small");
                    break;
                // in case the size is normal
                case ("normal") :
                    $this.addClass("colony-button-normal");
                    break;
                // in case the size is large
                case ("large") :
                    $this.addClass("colony-button-large");
                    break;
            }
        }

        // in case the click property is defined
        if (completeOptions["click"]) {
            // retrieves the click property
            var colonyButtonClick = completeOptions["click"];

            // sets the click handler
            $this.click(colonyButtonClick);
        }

        // in case the image property is defined
        if (completeOptions["image"]) {
            // retrieves the image property
            var colonyButtonImage = completeOptions["image"];

            // creates the button image element
            var buttonImage = $("<img id='buttonImage' src='"
                    + colonyButtonImage + "' />");

            // appends the button image to the colony button
            $this.append(buttonImage);

            // sets the has image flag as true
            hasImage = true;
        }

        if (hasImage)
            // creates the button text image element
            var buttonText = $("<span id='buttonTextImage'>" + text + "</span>");
        else
            // creates the button text element
            var buttonText = $("<span id='buttonText'>" + text + "</span>");

        // appends the button text to the colony button
        $this.append(buttonText);
    };

    /**
     * The default options for the colony button.
     *
     * @type Map
     */
    $.fn.colonyButton.defaults = {
        size : "normal"
    };

    /**
     * Creates a new colony list box in the given div element.
     *
     * @param {ColonyDataStore}
     *            dataStore The colony data store for the colony list box
     *            creation.
     * @param {Map}
     *            options The options for the colony list box creation.
     */
    $.fn.colonyListBox = function(dataStore, options) {
        // completes the options appending the defaults and the argument options
        var completeOptions = $.extend({}, $.fn.colonyListBox.defaults, options);

        // selects the element
        var $this = $(this);

        // adds the colony list box class
        $this.addClass("colony-list-box");

        // retrieves all the data store elements
        var dataStoreAllElements = dataStore.getAllElements();

        // iterates throught all the data store elements
        for (elementKey in dataStoreAllElements) {
            // retrieves the data store element
            var dataStoreElement = dataStoreAllElements[elementKey];

            // creates a new div element using the datastore element
            var divElement = "<div class='colony-list-box-element'>"
                    + dataStoreElement + "</div>";

            // appends the div element to the colony list box
            $this.append(divElement);
        }

        $("#" + $this.attr("id") + " > .colony-list-box-element").live("click",
                function() {
                    // retrieves all the list box elements
                    var listBoxElements = $this.children(".colony-list-box-element");

                    // iterates over all the list box elements
                    listBoxElements.each(function() {
                        // unselects the box element by removing the colony-list-box-element-selected class
                        $(this).removeClass("colony-list-box-element-selected");
                    });

                    // selects the box element by adding the colony-list-box-element-selected class
                    $(this).addClass("colony-list-box-element-selected");

                    // triggers the selected element changed event
                    $this.trigger("selectedElementChanged", [$(this)]);
                });

        dataStore.addElementAddedHandler(function(elementName, elementValue) {
                    // creates a new div element using the element value
                    var divElement = "<div id='" + elementName
                            + "' class='colony-list-box-element'>"
                            + elementValue + "</div>";

                    // appends the div element to the colony list box
                    $this.append(divElement);
                });

        dataStore.addElementRemovedHandler(function(elementName) {
                    // retrieves the child of the parent for the element name
                    elementChild = $this.children("#" + elementName);

                    // removes the element from the the colony list box
                    elementChild.remove();
                });

        // must install an element modified handler
    }

    /**
     * The default options for the colony list box.
     *
     * @type Map
     */
    $.fn.colonyListBox.defaults = {
        size : "normal"
    };

    /**
     * Creates a new colony multi level list box in the given div element.
     *
     * @param {ColonyDataStore}
     *            dataStore The colony data store for the colony multi level
     *            list box creation.
     * @param {Map}
     *            options The options for the colony multi level list box
     *            creation.
     */
    $.fn.colonyMultiLevelListBox = function(dataStore, options) {
        // completes the options appending the defaults and the argument options
        var completeOptions = $.extend({},
                $.fn.colonyMultiLevelListBox.defaults, options);

        // selects the element
        var $this = $(this);

        // retrieves the identifier of the current selected element
        var thisId = $this.attr("id");

        // adds the colony list box class
        $this.addClass("colony-multi-level-list-box");

        // creates the header element
        var headerElement = "<div class='colony-multi-level-list-box-header'>header</div>";

        // preprends the header element
        $this.prepend(headerElement);

        // creates the new main list id
        var newMainListId = "mainList" + thisId;

        // retrieves the main list element
        var mainList = $this.find("#mainList");

        // changes the main list id
        mainList.attr("id", newMainListId);

        // creates a colony list box in the main list element
        mainList.colonyListBox(dataStore);

        mainList.bind("selectedElementChanged", function(event, value) {
                    console.debug(value);
                });

        // retrieves the rest of the list children
        var childrenList = $this.find("div[id^=list]");

        // retrieves the number of available levels
        var numberLevels = childrenList.size;

        // sets the number of levels of the element
        $this.data("numberLevels", numberLevels)

        // sets the number of levels of the element
        $this.data("currentLevel", 0)

        /*
         * childrenList.each(function() { var elementId = $(this).attr("id");
         * var newElementId = elementId + thisId; $(this).attr("id",
         * newElementId); $(this).colonyListBox(dataStore); });
         */
    }

    /**
     * The default options for the colony multi level list box.
     *
     * @type Map
     */
    $.fn.colonyMultiLevelListBox.defaults = {
        size : "normal"
    };
})(jQuery);
