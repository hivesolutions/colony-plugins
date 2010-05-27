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
    $("#account-description").click(function() {
                if (!$("#account-float-panel").is(":visible")) {
                    $("#account-float-panel").fadeIn(200, function() {
                                $("#account-float-panel").click(
                                        function(event) {
                                            event.stopPropagation();

                                        });
                                $(document).click(function(event) {
                                            $("#account-float-panel").hide();
                                            $(document).unbind("click");
                                        });
                            });
                }
            });

    // loads the contents
    contentsLoad();
});

/**
 * Loads the initial contents, modifing the internal DOM structure if necessary.
 */
function contentsLoad() {
    // sets the page in the body
    $("body").page();

    // sets the main container
    $("#main-container").maincontainer();

    // reloads the contents page
    $("#main-container").maincontainer("reload");
}

/**
 * Loads the page for the given hahs value.
 *
 * @param {String}
 *            hash The hash value to be reloaded.
 */
function pageLoad(hash) {
    changeContents(hash);
}

/**
 * Changes the contents of the main container.
 *
 * @param {String}
 *            target The target to be used in the update of the main container.
 */
function changeContents(target) {
    $("#main-container").maincontainer("changeMenu", {
                target : target
            });

    $("#main-container").maincontainer("change", {
                target : target
            });
}

/**
 * Retrieves the base path based on a component placed in the dom.
 *
 * @return {String} The base path.
 */
function getBasePath() {
    // returns the base path, based on the
    // component in the dom
    return $("#environment-variables > #base-path").html();
}

/**
 * Retrieves the ajax submit value based on a component placed in the dom.
 *
 * @return {String} The ajax submit.
 */
function getAjaxSubmit() {
    // returns the ajax submit value, based on the
    // component in the dom
    return $("#environment-variables > #ajax-submit").html();
}
