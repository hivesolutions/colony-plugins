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
    jQuery.fn.installfile = function(options) {
        // the post value
        var POST_VALUE = "post";

        // the content type value
        var CONTENT_TYPE_VALUE = "Content-Type";

        // the application octet stream value
        var APPLICATION_OCTET_STREAM_VALUE = "application/octet-stream";

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
            // retrieves the file
            var file = options["file"];

            // retrieves the target url
            var targetUrl = options["targetUrl"];

            // in case the file is invalid
            // or is not available
            if (!file) {
                // returns immediately
                return;
            }

            // creates a new file reader, to read
            // the file contents (ad binary data)
            var fileReader = new FileReader();
            fileReader.readAsBinaryString(file);

            // sets the file reader in the options
            options["fileReader"] = fileReader;
        };

        /**
         * Registers the event handlers for the created objects.
         */
        var _registerHandlers = function() {
            // retrieves the file reader from the optiokns
            var fileReader = options["fileReader"];

            // in case the file reader is invalid
            // or is not available
            if (!fileReader) {
                // returns immediately
                return;
            }

            // registets the file reader for the on load
            // event
            fileReader.onload = function(event) {
                // calls the file reader load
                __fileReaderLoad(matchedObject, options);
            };
        };

        var __fileReaderLoad = function(matchedObject, options) {
            // retrieves the file reader from the options
            var fileReader = options["fileReader"];

            // retrieves the target url from the options
            var targetUrl = options["targetUrl"];

            // retrieves the file contents from
            // the file reader
            var fileContents = fileReader.result;

            // encodes the file contents into base64
            var fileContentsBase64 = Base64.encode(fileContents);

            // creates a new cml http request
            var xmlHttpRequest = new XMLHttpRequest();

            // retrieves the upload element
            var uploadElement = jQuery(xmlHttpRequest.upload);

            // registers the upload element to the progress event
            uploadElement.bind("progress", function(event) {
                // in case the length is not
                // computable
                if (!event.lengthComputable) {
                    return
                }

                // calculates the percentage of loading
                var percentage = Math.round((event.loaded * 100) / event.total);

                // triggers the file progress change event
                matchedObject.trigger("file_progress_change", [percentage]);
            });

            // registers the upload element to the load event
            uploadElement.bind("load", function(event) {
                        // retrieves the response text
                        var responseText = xmlHttpRequest.responseText;

                        // retrieves the response status
                        var responseStatus = xmlHttpRequest.status;

                        // triggers the file loaded event
                        matchedObject.trigger("file_loaded", [responseText,
                                        responseStatus, xmlHttpRequest]);
                    });

            // opens the xml http request to the target url
            xmlHttpRequest.open(POST_VALUE, targetUrl);

            // sets the content type header
            xmlHttpRequest.setRequestHeader(CONTENT_TYPE_VALUE,
                    APPLICATION_OCTET_STREAM_VALUE)

            // sends the file contents (in base64)
            xmlHttpRequest.send(fileContentsBase64);

            // triggers the file loading event
            matchedObject.trigger("file_loading", []);
        }

        // initializes the plugin
        initialize();

        // returns the object
        return this;
    };
})(jQuery);

(function($) {
    jQuery.fn.installpackagefile = function(options) {
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
            // retrieves the file
            var file = options["file"];

            // retrieves the file name
            var fileName = file.name;

            // splits the file name to retrieve
            // the file extension
            var fileNameSplit = fileName.split(".");
            var fileNameSplitLength = fileNameSplit.length;
            var fileExtension = fileNameSplit[fileNameSplitLength - 1];

            // switches over the file extension
            switch (fileExtension) {
                // in case it's a bundle extension
                case "cbx" :
                    // sets the bundles json url
                    var url = "bundles.json";

                    // breaks the switch
                    break;

                // in case it's a plugin extension
                case "cpx" :
                    // sets the plugins json url
                    var url = "plugins.json";

                    // breaks the switch
                    break;
            }

            // sets the target url in the options
            options["targetUrl"] = url;

            // sets the file extension in the options
            options["fileExtension"] = fileExtension;

            // installs the file
            matchedObject.installfile(options);
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
    jQuery.fn.filedrop = function(options) {
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
            // registers the matched object for the drag enter event
            matchedObject.bind("dragenter", function(event) {
                        // stops the event propagation and prevents
                        // the default event operation
                        event.stopPropagation();
                        event.preventDefault();

                        // triggers the file enter event
                        matchedObject.trigger("file_enter", [])
                    });

            // registers the matched object for the drag leave event
            matchedObject.bind("dragleave", function(event) {
                        // stops the event propagation and prevents
                        // the default event operation
                        event.stopPropagation();
                        event.preventDefault();

                        // triggers the file leave event
                        matchedObject.trigger("file_leave", [])
                    });

            // registers the matched object for the drag over event
            matchedObject.bind("dragover", function(event) {
                        // stops the event propagation and prevents
                        // the default event operation
                        event.stopPropagation();
                        event.preventDefault();
                    });

            // registers the matched object for the drop event
            matchedObject.bind("drop", function(event) {
                        // stops the event propagation and prevents
                        // the default event operation
                        event.stopPropagation();
                        event.preventDefault();

                        // retrieves the data tranfer and the files
                        // rom the original event
                        var dataTransfer = event.originalEvent.dataTransfer;
                        var files = dataTransfer.files;

                        // triggers the file drop event
                        matchedObject.trigger("file_drop", [files])
                    });
        };

        // initializes the plugin
        initialize();

        // returns the object
        return this;
    };
})(jQuery);
