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

// the data proxy name value
DATA_PROXY_NAME_VALUE = "dataProxyName";

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
		var dataStoreInformation = new ColonyDataStore($this);

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
					if (completeOptions[DATA_PROXY_NAME_VALUE])
						// retrieves the dataProxyName property
						colonyMemoryDataProxyOptions["name"] = completeOptions[DATA_PROXY_NAME_VALUE];

					// creates a new memory data proxy
					var memoryDataProxy = $this.colonyMemoryDataProxy(colonyMemoryDataProxyOptions);

					dataStoreInformation.dataProxy = memoryDataProxy;
					dataStoreInformation.dataProxyName = memoryDataProxy["name"];
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
		dataStoreInformation.name = dataStoreName;

		// sets the data in the parent element
		$this.data(dataStoreName, dataStoreInformation);

		// returns the data store information map (data store)
		return dataStoreInformation;
	}

	ColonyDataStore = function(element) {
		// sets the data store element in the data store
		this.element = element;

		// starts the list of element added handlers
		this.elementAddedHandlers = [];

		// starts the list of element removed handlers
		this.elementRemovedHandlers = [];
	}

	ColonyDataStore.prototype.setDataProxy = function(dataProxy) {
	}

	ColonyDataStore.prototype.addElementAddedHandler = function(handler) {
		// retrieves the element added handlers
		var elementAddedHandlers = this.elementAddedHandlers;

		// adds the new handler to the list of element added handlers
		elementAddedHandlers.push(handler);
	}

	ColonyDataStore.prototype.removeElementAddedHandler = function(handler) {
	}

	ColonyDataStore.prototype.addElementRemovedHandler = function(handler) {
		// retrieves the element removed handlers
		var elementRemovedHandlers = this.elementRemovedHandlers;

		// adds the new handler to the list of element removed handlers
		elementRemovedHandlers.push(handler);
	}

	ColonyDataStore.prototype.removeElementRemovedHandler = function(handler) {
	}

	ColonyDataStore.prototype.addElement = function(elementName, elementValue) {
		// retrieves the data proxy
		var dataProxy = this.dataProxy;

		// adds the element to the data proxy
		dataProxy.addElement(elementName, elementValue);

		// retrieves the element added handlers
		var elementAddedHandlers = this.elementAddedHandlers;

		// iterates over all the element added handlers
		for (var i = 0; i < elementAddedHandlers.length; i++) {
			// retrieves the element added handler
			elementAddedHandler = elementAddedHandlers[i];

			// calls the element added handler
			elementAddedHandler(elementName, elementValue);
		}
	}

	ColonyDataStore.prototype.removeElement = function(elementName) {
		// retrieves the data proxy
		var dataProxy = this.dataProxy;

		// removes the element from the data proxy
		dataProxy.removeElement(elementName);

		// retrieves the element removed handlers
		var elementRemovedHandlers = this.elementRemovedHandlers;

		// iterates over all the element removed handlers
		for (var i = 0; i < elementRemovedHandlers.length; i++) {
			// retrieves the element removed handler
			elementRemovedHandler = elementRemovedHandlers[i];

			// calls the element removed handler
			elementRemovedHandler(elementName);
		}
	}

	ColonyDataStore.prototype.getElement = function(elementName) {
		// retrieves the data proxy
		var dataProxy = this.dataProxy;

		// retrieves the element from the data proxy
		var elementValue = dataProxy.getElement(elementName);

		return elementValue;
	}

	ColonyDataStore.prototype.getAllElements = function() {
		// retrieves the data proxy
		var dataProxy = this.dataProxy;

		// retrieves all the elements from the data proxy
		var allElements = dataProxy.getAllElements();

		return allElements;
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
		var memoryDataProxyInformation = new ColonyMemoryDataProxy($this);

		// in case the name property is defined
		if (completeOptions["name"])
			// retrieves the name property
			var memoryDataProxyName = completeOptions["name"];
		else
			// sets the default name in the name property
			var memoryDataProxyName = $.fn.colonyMemoryDataProxy.DEFAULT_NAME;

		// sets the memory data proxy name in the memory data proxy
		memoryDataProxyInformation.name = memoryDataProxyName;

		// sets the data in the parent element
		$this.data(memoryDataProxyName, memoryDataProxyInformation);

		// returns the memory data proxy information map (memory data proxy)
		return memoryDataProxyInformation;
	}

	ColonyMemoryDataProxy = function(element) {
		// sets the memory data proxy element in the memory data proxy
		this.element = element;

		// sets the memory data proxy elements map as empty
		this.elements = {};

		// sets the memory data proxy elements index map as empty
		this.elementsLevelIndexMap = {}

		// sets the memory data proxy element levels as a new list of lists
		this.elementLevels = [[]];

		// sets the memory data proxy current level index
		this.currentLevelIndex = 0;

		// sets the memory data proxy current level
		this.currentLevel = this.elementLevels[this.currentLevelIndex];
	}

	ColonyMemoryDataProxy.prototype.addElement = function(elementName, elementValue) {
		// retrieves the elements map
		var memoryDataProxyInformationElements = this.elements;

		// retrieves the current level list
		var memoryDataProxyInformationCurrentLevel = this.currentLevel;

		// retrieves the elements index map
		var memoryDataProxyInformationElementsLevelIndexMap = this.elementsLevelIndexMap;
		
		// retrieves the current level list
		var memoryDataProxyInformationCurrentLevelIndex = this.currentLevelIndex;

		// sets the element value in the elements map
		memoryDataProxyInformationElements[elementName] = elementValue;

		// adds the element name to the current level list
		memoryDataProxyInformationCurrentLevel.push(elementName);

		// sets the elements level index map value
		memoryDataProxyInformationElementsLevelIndexMap[elementName] = memoryDataProxyInformationCurrentLevelIndex;
	}

	ColonyMemoryDataProxy.prototype.removeElement = function(elementName) {
		// retrieves the elements map
		var memoryDataProxyInformationElements = this.elements;

		// deletes the element value in the elements map
		delete memoryDataProxyInformationElements[elementName]
	}

	ColonyMemoryDataProxy.prototype.getElement = function(elementName) {
		// retrieves the elements map
		var memoryDataProxyInformationElements = this.elements;

		// retrieves the element value in the elements map
		var elementValue = memoryDataProxyInformationElements[elementName];

		// returns the element value
		return elementValue;
	}

	ColonyMemoryDataProxy.prototype.addChildElement = function(elementName, elementValue, parentElementName) {
		// retrieves the elements map
		var memoryDataProxyInformationElements = this.elements;

		// sets the element value in the elements map
		memoryDataProxyInformationElements[elementName] = elementValue
	}

	ColonyMemoryDataProxy.prototype.getAllElements = function() {
		// retrieves the elements map
		var memoryDataProxyInformationElements = this.elements;

		// returns the elements map
		return memoryDataProxyInformationElements;
	}

	ColonyMemoryDataProxyElement = function(elementName, elementValue) {
		this.name = elementName;
		this.value = elementValue;
		this.parents = [];
		this.childs = [];
	}

	ColonyMemoryDataProxyElement.prototype.getName = function() {
		// returns the element name
		return this.name;
	}

	ColonyMemoryDataProxyElement.prototype.getValue = function() {
		// returns the element value
		return this.value;
	}

	ColonyMemoryDataProxyElement.prototype.addParent = function(parentElement) {
		// adds the parent element to the list of parents
		this.parents.push(parentElement);
	}

	ColonyMemoryDataProxyElement.prototype.removeParent = function(parentElement) {
		// retrieves the parent element index from the list of parent elements
		var parentIndex = this.parents.indexOf(parentElement);

		// in case the parent element exists
		if(parentIndex != -1)
			// removes the parent element from the list of parent elements
			this.parents.splice(parentIndex, parentIndex);
	}

	ColonyMemoryDataProxyElement.prototype.addChild = function(childElement) {
		// adds the child element to the list of childs
		this.childs.push(childElement);
	}

	ColonyMemoryDataProxyElement.prototype.removeChild = function(childElement) {
		// retrieves the child element index from the list of child elements
		var childIndex = this.childs.indexOf(childElement);

		// in case the child element exists
		if(childIndex != -1)
			// removes the child element from the list of child elements
			this.childs.splice(childIndex, childIndex);
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
