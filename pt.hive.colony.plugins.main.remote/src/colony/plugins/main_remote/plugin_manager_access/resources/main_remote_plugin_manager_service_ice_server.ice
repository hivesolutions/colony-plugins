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
// __revision__  = $LastChangedRevision$
// __date__      = $LastChangedDate$
// __copyright__ = Copyright (c) 2008 Hive Solutions Lda.
// __license__   = GNU General Public License (GPL), Version 3

#ifndef MAIN_REMOTE_PLUGIN_MANAGER
#define MAIN_REMOTE_PLUGIN_MANAGER

module pt {
	module hive {
		module colony {
			module plugins {
				module main {
					module remote {
						module pluginmanagericeservice {
							struct Capability {
								string capabilityName;
							};
							["java:type:java.util.LinkedList<Capability>"]
							sequence<Capability> Capabilities;
							struct Dependency {
								string dependencyName;
							};
							["java:type:java.util.LinkedList<Dependency>"]
							sequence<Dependency> Dependencies;
							struct Event {
								string eventName;
							};
							sequence<Event> Events;
							struct PluginDescriptor {
								int id;
								string name;
								string shortName;
								string description;
								string version;
								Capabilities capabilitiesList;
								Capabilities capabilitiesAllowedList;
								Dependencies dependenciesList;
								Events eventsHandledList;
								Events eventsRegistrableList;
								bool valid;
								bool loaded;
							};
							["java:type:java.util.LinkedList<PluginDescriptor>"]
							sequence<PluginDescriptor> PluginDescriptors;
							interface PluginManagerOp {
								idempotent int registerPluginManager(string id);
								idempotent PluginDescriptors getPluginDescriptorById(string pluginId);
							};
						};
					};
				};
			};
		};
	};
};

#endif
