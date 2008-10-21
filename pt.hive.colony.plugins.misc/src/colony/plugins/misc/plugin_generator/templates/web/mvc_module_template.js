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
// __revision__  = $LastChangedRevision: 1805 $
// __date__      = $LastChangedDate: 2008-09-11 11:42:26 +0100 (Qui, 11 Set 2008) $
// __copyright__ = Copyright (c) 2008 Hive Solutions Lda.
// __license__   = GNU General Public License (GPL), Version 3

"pt.hive.prototype.gui.web.plugins.{namespace}.{id}".namespace();

pt.hive.prototype.gui.web.plugins.{namespace}.{id}.{module_name} = Class.create(
		pt.hive.prototype.gui.web.plugins.main_logic.mvc.Module, {
			initialize : function($super, ownerPlugin, mvcManager, moduleId, moduleType) {
				$super(mvcManager, moduleId, moduleType);

				var mvcNamespace = pt.hive.prototype.gui.web.plugins.{namespace}.{id};
				this.generateModel(mvcNamespace.{module_name}Model);
				this.generateView(mvcNamespace.{module_name}View);
				this.generateController(mvcNamespace.{module_name}Controller);
				this.generatePresentationModel(mvcNamespace.{module_name}PresentationModel);
			}
		});

loaded("plugins/{path}/{id}_module.js");
