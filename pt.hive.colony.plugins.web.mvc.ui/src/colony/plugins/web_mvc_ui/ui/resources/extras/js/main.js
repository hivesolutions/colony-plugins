// Take The Bill Service
// Copyright (C) 2010 Hive Solutions Lda.
//
// This file is part of Take The Bill Service.
//
// Take The Bill Service is confidential and property of Hive Solutions Lda,
// its usage is constrained by the terms of the Hive Solutions
// Confidential Usage License.
//
// Take The Bill Service should not be distributed under any circumstances,
// violation of this may imply legal action.
//
// If you have any questions regarding the terms of this license please
// refer to <http://www.hive.pt/licenses/>.

// __author__    = João Magalhães <joamag@hive.pt>
// __version__   = 1.0.0
// __revision__  = $LastChangedRevision$
// __date__      = $LastChangedDate$
// __copyright__ = Copyright (c) 2010 Hive Solutions Lda.
// __license__   = Hive Solutions Confidential Usage License (HSCUL)

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
