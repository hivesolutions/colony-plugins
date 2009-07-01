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

// called uppon search index management content item loading complete
$("#searchIndexManagementContentItem").ready(function() {
    $("#searchIndexListRefresh").click(function() {
                // refreshes the index manager table
                refreshIndexManagerTable();
            });

    $("#searchIndexListNew").colonyButton("new", {
        size : "normal",
        click : function() {
            $("#newSearchIndexWindow").dialog({
                        width : 620,
                        height : 410,
                        autoOpen : false,
                        show : "drop",
                        hide : "drop",
                        resizeStop : function() {
                            alert("tobias");
                        }
                    });
            $("#newSearchIndexWindow").dialog("open");
            $("#newSearchIndexWindow #propertiesEditor").children().each(
                    function() {
                        $(this).hide();
                    });
            $("#newSearchIndexWindow #propertiesVisualizer").children().each(
                    function() {
                        $(this).hide();
                    });
        },
        image : "pics/add.png"
    });

    $("#newSearchIndexWindow #propertiesSelector > .listBoxElement").click(
            function() {
                // retirves the selected html value
                var selectedValue = $(this).html();

                // retrieves the properties editor
                var propertiesEditor = $("#newSearchIndexWindow #propertiesEditor")

                // retrieves the properties editor children
                var propertiesEditorChildren = propertiesEditor.children();

                propertiesEditorChildren.each(function() {
                            $(this).slideUp("normal");
                        });

                // in case the selected value is type
                if (selectedValue == "Type") {
                    // retrieves the properties type div
                    var propertiesDiv = $("#newSearchIndexWindowPropertiesType");
                } else if (selectedValue == "Metrics") {
                    // retrieves the properties metrics div
                    var propertiesDiv = $("#newSearchIndexWindowPropertiesMetrics");
                } else if (selectedValue == "File Extensions") {
                    // retrieves the properties metrics div
                    var propertiesDiv = $("#newSearchIndexWindowPropertiesFileExtensions");
                }

                propertiesDiv.slideDown("normal");
            });

    $("#newSearchIndexWindow #propertiesEditor .listBoxElement").click(
            function() {
                // retrieves the properties visualizer
                var propertiesVisualizer = $("#newSearchIndexWindow #propertiesVisualizer");

                // retrieves the properties visualizer children
                var propertiesVisualizerChildren = propertiesVisualizer.children();

                propertiesVisualizerChildren.each(function() {
                            $(this).slideUp("normal");
                        });

                var parentValue = $("#newSearchIndexWindow #propertiesSelector .listBoxElementSelected").html();
                var value = $(this).html();
                var noSpacesParentValue = parentValue.replace(" ", "");
                var noSpacesValue = value.replace(" ", "");
                var realId = "newSearchIndexWindowProperties"
                        + noSpacesParentValue + noSpacesValue;
                var realValue = $("#" + realId);
                realValue.slideDown("normal");
            });
});

function refreshIndexManagerTable() {
    $.post("actions/search_index_information_retrieval.ctp", {
                queryValue : "getIndexIdentifiers"
            }, refreshIndexManagerTableHandler);
}

function refreshIndexManagerTableHandler(responseText, textStatus) {

}
