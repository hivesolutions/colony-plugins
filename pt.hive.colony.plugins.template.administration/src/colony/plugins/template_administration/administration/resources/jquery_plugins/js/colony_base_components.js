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
	 * @param {Dicitonary}
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
	 * @param {Dicitonary}
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
	 * @param {Dicitonary}
	 *            options The options for the colony list box creation.
	 */
	$.fn.colonyListBox = function(dataStore, options) {
		// completes the options appending the defaults and the argument options
		var completeOptions = $.extend({}, $.fn.colonyListBox.defaults, options);

		// selects the element
		var $this = $(this);

		// adds the colony list box class
		$this.addClass("colony-list-box");

		// must iterate throught all the elements in the data store
		// and add them to the list box

		// elements should be like this
		// <div class="listBoxElement">Type</div>

		$this.append("<div class='colony-list-box-element'>Type</div>");

		// must install a new element handler

		// must install an element removed handler

		// must install an element modified handler
	}

	/**
	 * The default options for the colony list box.
	 * 
	 * @type Map
	 */
	$.fn.colonyButton.defaults = {
		size : "normal"
	};
})(jQuery);
