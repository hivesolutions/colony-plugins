// Hive Colony Framework
// Copyright (C) 2008 Hive Solutions Lda.
//
// This file is part of Hive Colony Web Framework.
//
// Hive Colony Web Framework is free software: you can redistribute it and/or modify
// it under the terms of the GNU General Public License as published by
// the Free Software Foundation, either version 3 of the License, or
// (at your option) any later version.
//
// Hive Colony Web Framework is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
// GNU General Public License for more details.
//
// You should have received a copy of the GNU General Public License
// along with Hive Colony Web Framework. If not, see <http://www.gnu.org/licenses/>.

// __author__    = João Magalhães <joamag@hive.pt>
// __version__   = 1.0.0
// __revision__  = $LastChangedRevision: 684 $
// __date__      = $LastChangedDate: 2008-12-08 15:16:55 +0000 (seg, 08 Dez 2008) $
// __copyright__ = Copyright (c) 2008 Hive Solutions Lda.
// __license__   = GNU General Public License (GPL), Version 3

(function($) {
	/**
	 * Creates a new colony data store in the given element.
	 * 
	 * @param {Dicitonary}
	 *            options The options for the colony data store creation.
	 */
	$.fn.colonyDataStore = function(options) {
		// completes the options appending the defaults and the argument options
		var completeOptions = $.extend({}, $.fn.colonyDataStore.defaults,
				options);

		// selects the element
		var $this = $(this);

		// creates the data store information map
		var dataStoreInformation = {};

		// starts the list of element added handlers
		dataStoreInformation["elementAddedHandlers"] = [];

		// starts the list of element removed handlers
		dataStoreInformation["elementRemovedHandlers"] = [];

		// in case the dataProxy property is defined
		if (completeOptions["dataProxy"]) {
			// retrieves the dataProxy property
			var colontDataStoreDataProxy = completeOptions["dataProxy"];

			// switches in the dataProxy property
			switch (colontDataStoreDataProxy) {
				// in case the dataProxy is of type memory
				case ("memory") :
					// creates the colony memory data proxy options map
					var colonyMemoryDataProxyOptions = {};

					// in case the dataProxyName property is defined
					if (completeOptions["dataProxyName"])
						// retrieves the dataProxyName property
						colonyMemoryDataProxyOptions["name"] = completeOptions["dataProxyName"];

					// creates a new memory data proxy
					var memoryDataProxy = $this.colonyMemoryDataProxy(colonyMemoryDataProxyOptions);

					dataStoreInformation["dataProxy"] = memoryDataProxy;
					dataStoreInformation["dataProxyName"] = memoryDataProxy["name"];
					break;
			}
		}

		// in case the name property is defined
		if (completeOptions["elementAdded"]) {
			// retrieves the elementAdded property
			var colonyDataStoreElementAdded = completeOptions["elementAdded"];

			// adds the element added handler to the list of element added handlers
			dataStoreInformation["elementAddedHandlers"].push(colonyDataStoreElementAdded)
		}

		// in case the name property is defined
		if (completeOptions["name"])
			// retrieves the name property
			var dataStoreName = completeOptions["name"];
		else
			// sets the default name in the name property
			var dataStoreName = $.fn.colonyDataStore.DEFAULT_NAME;

		// sets the data store name in the data store
		dataStoreInformation["name"] = dataStoreName;

		// sets the data in the parent element
		$this.data(dataStoreName, dataStoreInformation);

		// returns the data store information map (data store)
		return dataStoreInformation;
	}

	$.fn.colonyDataStoreSetDataProxy = function(elementName, elementValue, options) {
	}

	$.fn.colonyDataStoreAddElement = function(elementName, elementValue, options) {
		// selects the element
		var $this = $(this);

		// gets the data store information from the parent element
		var dataStoreInformation = getDataStoreInformation($this, options);

		// retrieves the data proxy name
		var dataProxyName = dataStoreInformation["dataProxyName"];

		// adds the element to the data proxy
		$this.colonyMemoryDataProxyAddElement(elementName, elementValue, {
					"name" : dataProxyName
				});

		// retrieves the element added handlers
		var elementAddedHandlers = dataStoreInformation["elementAddedHandlers"];

		// iterates over all the element added handlers
		for (var i = 0; i < elementAddedHandlers.length; i++) {
			// retrieves the element added handler
			elementAddedHandler = elementAddedHandlers[i];

			// calls the element added handler
			elementAddedHandler();
		}
	}

	$.fn.colonyDataStoreRemoveElement = function(elementName, options) {
	}

	$.fn.colonyDataStoreGetElement = function(elementName, options) {
	}

	function getDataStoreInformation($object, options) {
		// in case the name property is defined
		if (options != undefined && options["name"])
			// retrieves the name property
			var dataStoreName = options["name"];
		else
			// sets the default name in the name property
			var dataStoreName = $.fn.colonyDataStore.DEFAULT_NAME;

		// retrieves the data store information map (data store)
		var dataStoreInformation = $object.data("DataStore");

		// returns the data store information map (data store)
		return dataStoreInformation;
	}

	/**
	 * The default options for the colony data store.
	 * 
	 * @type Map
	 */
	$.fn.colonyDataStore.defaults = {
		"dataProxy" : "memory"
	};

	/**
	 * The default colony data store name.
	 * 
	 * @type String
	 */
	$.fn.colonyDataStore.DEFAULT_NAME = "DataStore";

	/**
	 * Creates a new colony memory data proxy in the given element.
	 * 
	 * @param {Dicitonary}
	 *            options The options for the colony memory data proxy creation.
	 */
	$.fn.colonyMemoryDataProxy = function(options) {
		// completes the options appending the defaults and the argument options
		var completeOptions = $.extend({}, $.fn.colonyMemoryDataProxy.defaults,
				options);

		// selects the element
		var $this = $(this);

		// creates the memory data proxy information map
		var memoryDataProxyInformation = {};

		// in case the name property is defined
		if (completeOptions["name"])
			// retrieves the name property
			var memoryDataProxyName = completeOptions["name"];
		else
			// sets the default name in the name property
			var memoryDataProxyName = $.fn.colonyMemoryDataProxy.DEFAULT_NAME;

		// sets the memory data proxy elements map as empty
		memoryDataProxyInformation["elements"] = {};

		// sets the memory data proxy name in the memory data proxy
		memoryDataProxyInformation["name"] = memoryDataProxyName;

		// sets the data in the parent element
		$this.data(memoryDataProxyName, memoryDataProxyInformation);

		// returns the memory data proxy information map (memory data proxy)
		return memoryDataProxyInformation;
	}

	$.fn.colonyMemoryDataProxyAddElement = function(elementName, elementValue, options) {
		// selects the element
		var $this = $(this);

		// gets the memory data proxy information from the parent element
		var memoryDataProxyInformation = getMemoryDataProxyInformation($this,
				options);

		// retrieves the elements map
		memoryDataProxyInformationElements = memoryDataProxyInformation["elements"];

		// sets the element value in the elements map
		memoryDataProxyInformationElements[elementName] = elementValue
	}

	function getMemoryDataProxyInformation($object, options) {
		// in case the name property is defined
		if (options != undefined && options["name"])
			// retrieves the name property
			var memoryDataProxyName = options["name"];
		else
			// sets the default name in the name property
			var memoryDataProxyName = $.fn.colonyMemoryDataProxy.DEFAULT_NAME;

		// retrieves the memory data proxy information map (memory data proxy)
		var memoryDataProxyInformation = $object.data(memoryDataProxyName);

		// returns the memory data proxy information map (memory data proxy)
		return memoryDataProxyInformation;
	}

	/**
	 * The default options for the colony memory data proxy.
	 * 
	 * @type Map
	 */
	$.fn.colonyMemoryDataProxy.defaults = {};

	/**
	 * The default colony memory data proxy name.
	 * 
	 * @type String
	 */
	$.fn.colonyMemoryDataProxy.DEFAULT_NAME = "MemoryDataProxy";

})(jQuery);
