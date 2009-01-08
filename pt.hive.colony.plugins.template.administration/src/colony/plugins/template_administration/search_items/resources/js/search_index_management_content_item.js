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

// __author__    = Jo�o Magalh�es <joamag@hive.pt>
// __version__   = 1.0.0
// __revision__  = $LastChangedRevision: 684 $
// __date__      = $LastChangedDate: 2008-12-08 15:16:55 +0000 (seg, 08 Dez 2008) $
// __copyright__ = Copyright (c) 2008 Hive Solutions Lda.
// __license__   = GNU General Public License (GPL), Version 3

// called uppon search index management content item loading complete
$("#searchIndexManagementContentItem").ready(function() {
			// hides the new search index window
			$("#newSearchIndexWindow").hide();

			$("#searchIndexListRefresh").click(function() {
						// refreshes the index manager table
						refreshIndexManagerTable();
					});

			$("#searchIndexListNew").click(function() {
						$("#newSearchIndexWindow").show();
						$("#newSearchIndexWindow").dialog({
									"width" : 420,
									"height" : 380,
									"show" : "drop",
									"hide" : "drop"
								});
					});

			$(".listBox > div").click(function() {
						var divParent = $(this).parent();
						var selectedElements = divParent.children(".listBoxElementSelected");
						selectedElements.each(function() {
							$(this).removeClass("listBoxElementSelected");
						});
						$(this).addClass("listBoxElementSelected");
					});
		});

function refreshIndexManagerTable() {
	$.post("actions/search_index_information_retrieval.ctp", {
				"queryValue" : "getIndexIdentifiers"
			}, refreshIndexManagerTableHandler);
}

function refreshIndexManagerTableHandler(responseText, textStatus) {

}
