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

// __author__    = {author} <{email}>
// __version__   = 1.0.0
// __revision__  = $LastChangedRevision: 1714 $
// __date__      = $LastChangedDate: 2008-08-17 00:37:51 +0100 (Dom, 17 Ago 2008) $
// __copyright__ = Copyright (c) 2008 Hive Solutions Lda.
// __license__   = GNU General Public License (GPL), Version 3

pt.hive.prototype.gui.web.plugins.{module_name}Plugin = Class.create(
		pt.hive.prototype.gui.web.framework.Plugin, {
			initialize : function($super, manager) {
				$super(manager);

				// the plugin properties
				this.id = "pt.hive.prototype.gui.web.plugins.{namespace}.{id}";
				this.name = "{name}";
				this.shortName = "{short_name}";
				this.description = "{description}";
				this.version = "{version}";
				this.author = "{author}";
				this.capabilities = [];
				this.capabilitiesAllowed = [];
				this.dependencies = [new pt.hive.prototype.gui.web.framework.PluginDependency(
								"pt.hive.prototype.gui.web.plugins.main.logic.mvc",
								"1.0.0", true)];
				this.eventsHandled = [];
				this.eventsRegistrable = [];

				this.jsImports = [
				new pt.hive.prototype.gui.web.framework.JsImport("plugins/{path}/{id}_model.js"),
				new pt.hive.prototype.gui.web.framework.JsImport("plugins/{path}/{id}_view.js"),
				new pt.hive.prototype.gui.web.framework.JsImport("plugins/{path}/{id}_controller.js"),
				new pt.hive.prototype.gui.web.framework.JsImport("plugins/{path}/{id}_presentation_model.js"),
				new pt.hive.prototype.gui.web.framework.JsImport("plugins/{path}/{id}_module.js")
				];
			},
			loadPlugin : function($super) {
				$super();
			},
			endLoadPlugin : function($super) {
				$super();
				this.mvcModule = new pt.hive.prototype.gui.web.plugins.{namespace}.{module_name}(
						this, mvcManager, {id}, "panel");
			},
			dependencyInjected : function($super, plugin) {
				$super(plugin);
			},
			getPanelModule : function(){
				return this.mvcModule;
			}
		});

plugins.push(pt.hive.prototype.gui.web.plugins.{module_name}Plugin);
loaded("plugins/{id}_plugin.js");
