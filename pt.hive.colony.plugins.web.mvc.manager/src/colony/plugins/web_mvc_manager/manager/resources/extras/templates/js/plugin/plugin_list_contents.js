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

$(document).ready(function() {
            // sets the logic loaded data
            var logicLoaded = $("#contents").data("logicLoaded");

            // in case the logic is already loaded
            if (logicLoaded) {
                // returns immediately
                return
            }

            var _registerExtraHandlers = function(targetElement) {
                // retrieves the switch buttons from the target element
                var switchButtons = $(".switch-button", targetElement);

                // creates the switch buttons
                switchButtons.switchbutton();

                // registers the callback for the status change event
                switchButtons.bind("status_change",
                        function(event, element, status) {
                            // retrieves the switch button
                            var switchButton = $(this);

                            // retrieves the plugin id from the switch button
                            var pluginId = switchButton.attr("plugin");

                            // retrieves the plugin status, from the stauts of the switch button
                            var pluginStatus = status == "on"
                                    ? "load"
                                    : "unload";

                            // retrieves the oposite status
                            var opositeStatus = status == "on" ? "off" : "on";

                            // removes the status class, and adds
                            // the oposite class (changing status)
                            switchButton.removeClass(status);
                            switchButton.addClass(opositeStatus);

                            $.ajax({
                                        url : "plugins/" + pluginId + "/change_status.json",
                                        type : "post",
                                        data : {
                                            plugin_status : pluginStatus
                                        }
                                    });
                        });
            };

            // retrieves the plugin table
            var pluginTable = $("#plugin-table");

            // registers the extra handlers for the plugin table
            _registerExtraHandlers(pluginTable);

            // register the callback to the content change event
            pluginTable.bind("content_change", function(event, targetElements) {
                        _registerExtraHandlers(targetElements);
                    });

            // sets the logic loaded data
            $("#contents").data("logicLoaded", true);
        });
