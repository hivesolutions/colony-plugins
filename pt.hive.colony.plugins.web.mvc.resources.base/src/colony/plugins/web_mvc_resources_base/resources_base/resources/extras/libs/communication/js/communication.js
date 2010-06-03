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

// __author__    = João Magalhães <joamag@hive.pt> & Luís Martinho <lmartinho@hive.pt>
// __version__   = 1.0.0
// __revision__  = $LastChangedRevision: 7693 $
// __date__      = $LastChangedDate: 2010-03-25 08:40:31 +0000 (qui, 25 Mar 2010) $
// __copyright__ = Copyright (c) 2008 Hive Solutions Lda.
// __license__   = GNU General Public License (GPL), Version 3

(function($) {
    $.fn.communication = function(method, options) {
        // the default values for the menu
        var defaults = {};

        // sets the default method value
        var method = method ? method : "default";

        // sets the default options value
        var options = options ? options : {};

        // constructs the options
        var options = $.extend(defaults, options);

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
            // retrieves the url from the options
            var url = options["url"];

            // retrieves the timeout from the options
            var timeout = options["timeout"];

            // retrieves the data callback functions from the options
            var dataCallbackFunctions = options["dataCallbackFunctions"];

            // sets the default timeout value
            timeout = timeout ? timeout : 1000;

            // sets the matched object url data
            matchedObject.data("url", url);

            // sets the matched object timeout data
            matchedObject.data("timeout", timeout);

            // sets the matched object data callback functions data
            matchedObject.data("dataCallbackFunctions", dataCallbackFunctions);

            $.ajax({
                        type : "post",
                        url : url,
                        data : {
                            command : "connect"
                        },
                        success : function(data) {
                            __onConnectSuccess(matchedObject, options, data);
                        },
                        error : function(request, textStatus, errorThrown) {
                            __onConnectError(matchedObject, options, request,
                                    textStatus, errorThrown);
                        }
                    });
        };

        var __update = function(matchedObject, options) {
            // retrieves the url data
            var url = matchedObject.data("url");

            // retrieves the connection data
            var connectionId = matchedObject.data("id");

            $.ajax({
                        type : "post",
                        url : url,
                        data : {
                            id : connectionId,
                            command : "update"
                        },
                        success : function(data) {
                            __onUpdateSuccess(matchedObject, options, data);
                        },
                        error : function(request, textStatus, errorThrown) {
                            __onUpdateError(matchedObject, options, request,
                                    textStatus, errorThrown);
                        }
                    });
        };

        var __onConnectSuccess = function(matchedObject, options, data) {
            // parses the data generating the json data
            var jsonData = $.parseJSON(data);

            // retrieves the result message
            var resultMessage = jsonData["result"];

            // in case there was success
            if (resultMessage == "success") {
                // retrieves the connection id
                var connectionId = jsonData["id"];

                // sets the connection id in the matched object
                matchedObject.data("id", connectionId);

                // retrieves the timeout data
                var timeout = matchedObject.data("timeout");

                // sets the interval for contents retrieval, and
                // retrieves the interval handler
                var intervalHandler = setInterval(function() {
                            __update(matchedObject, options);
                        }, timeout);

                // sets the matched object interval handler
                matchedObject.data("intervalHandler", intervalHandler);
            }
        };

        var __onConnectError = function(matchedObject, options, request, textStatus, errorThrown) {
        };

        var __onUpdateSuccess = function(matchedObject, options, data) {
            // parses the data generating the json data
            var jsonData = $.parseJSON(data);

            // retrieves the result message
            var resultMessage = jsonData["result"];

            $(resultMessage).each(function(index, element) {
                        // calls the data callbacks
                        __callDataCallbacks(matchedObject, options, element);
                    });
        };

        var __onUpdateError = function(matchedObject, options, request, textStatus, errorThrown) {
        };

        var __callDataCallbacks = function(matchedObject, options, data) {
            // retrieves the data callback functions data
            var dataCallbackFunctions = matchedObject.data("dataCallbackFunctions");

            // sets the default data callback functions
            dataCallbackFunctions = dataCallbackFunctions
                    ? dataCallbackFunctions
                    : [];

            // iterates over all the data callback functions
            $(dataCallbackFunctions).each(function(index, element) {
                        // calls the callback function
                        element(data);
                    });
        };

        // switches over the method
        switch (method) {
            case "disconnect" :
                _disconnect(matchedObject, options);
                break;

            case "data" :
                _data(matchedObject, options);
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
