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

// __author__    = Jo?o Magalh?es <joamag@hive.pt>
// __version__   = 1.0.0
// __revision__  = $LastChangedRevision$
// __date__      = $LastChangedDate$
// __copyright__ = Copyright (c) 2010 Hive Solutions Lda.
// __license__   = Hive Solutions Confidential Usage License (HSCUL)

jQuery.extend({
    historyCurrentHash : undefined,
    historyCallback : undefined,
    historyIframeSrc : undefined,
    historyNeedIframe : jQuery.browser.msie
            && (jQuery.browser.version < 8 || document.documentMode < 8),

    historyInit : function(callback, src) {
        jQuery.historyCallback = callback;
        if (src)
            jQuery.historyIframeSrc = src;
        var current_hash = location.hash.replace(/\?.*$/, "");

        jQuery.historyCurrentHash = current_hash;
        if (jQuery.historyNeedIframe) {
            // stops the callback firing twice during initilization
            // if no hash present
            if (jQuery.historyCurrentHash == "") {
                jQuery.historyCurrentHash = "#";
            }

            // adds the hidden iframe for internet explorer
            jQuery("body").prepend("<iframe id=\"jQuery_history\" style=\"display: none;\""
                    + " src=\"javascript:false;\"></iframe>");
            var ihistory = jQuery("#jQuery_history")[0];
            var iframe = ihistory.contentWindow.document;
            iframe.open();
            iframe.close();
            iframe.location.hash = current_hash;
        } else if (jQuery.browser.safari) {
            // etablish back/forward stacks
            jQuery.historyBackStack = [];
            jQuery.historyBackStack.length = history.length;
            jQuery.historyForwardStack = [];
            jQuery.lastHistoryLength = history.length;

            jQuery.isFirst = true;
        }
        if (current_hash)
            jQuery.historyCallback(current_hash.replace(/^#/, ""));
        setInterval(jQuery.historyCheck, 100);
    },

    historyAddHistory : function(hash) {
        // This makes the looping function do something
        jQuery.historyBackStack.push(hash);

        jQuery.historyForwardStack.length = 0; // clear forwardStack (true click occured)
        this.isFirst = true;
    },

    historyCheck : function() {
        if (jQuery.historyNeedIframe) {
            // On IE, check for location.hash of iframe
            var ihistory = jQuery("#jQuery_history")[0];
            var iframe = ihistory.contentDocument
                    || ihistory.contentWindow.document;
            var current_hash = iframe.location.hash.replace(/\?.*$/, "");
            if (current_hash != jQuery.historyCurrentHash) {

                location.hash = current_hash;
                jQuery.historyCurrentHash = current_hash;
                jQuery.historyCallback(current_hash.replace(/^#/, ""));

            }
        } else if (jQuery.browser.safari) {
            if (jQuery.lastHistoryLength == history.length
                    && jQuery.historyBackStack.length > jQuery.lastHistoryLength) {
                jQuery.historyBackStack.shift();
            }
            if (!jQuery.dontCheck) {
                var historyDelta = history.length
                        - jQuery.historyBackStack.length;
                jQuery.lastHistoryLength = history.length;

                if (historyDelta) { // back or forward button has been pushed
                    jQuery.isFirst = false;
                    if (historyDelta < 0) { // back button has been pushed
                        // move items to forward stack
                        for (var i = 0; i < Math.abs(historyDelta); i++)
                            jQuery.historyForwardStack.unshift(jQuery.historyBackStack.pop());
                    } else { // forward button has been pushed
                        // move items to back stack
                        for (var i = 0; i < historyDelta; i++)
                            jQuery.historyBackStack.push(jQuery.historyForwardStack.shift());
                    }
                    var cachedHash = jQuery.historyBackStack[jQuery.historyBackStack.length
                            - 1];
                    if (cachedHash != undefined) {
                        jQuery.historyCurrentHash = location.hash.replace(
                                /\?.*$/, "");
                        jQuery.historyCallback(cachedHash);
                    }
                } else if (jQuery.historyBackStack[jQuery.historyBackStack.length
                        - 1] == undefined
                        && !jQuery.isFirst) {
                    // back button has been pushed to beginning and URL already pointed to hash (e.g. a bookmark)
                    // document.URL doesn't change in Safari
                    if (location.hash) {
                        var current_hash = location.hash;
                        jQuery.historyCallback(location.hash.replace(/^#/, ""));
                    } else {
                        var current_hash = "";
                        jQuery.historyCallback("");
                    }
                    jQuery.isFirst = true;
                }
            }
        } else {
            // otherwise, check for location.hash
            var current_hash = location.hash.replace(/\?.*$/, "");
            if (current_hash != jQuery.historyCurrentHash) {
                jQuery.historyCurrentHash = current_hash;
                jQuery.historyCallback(current_hash.replace(/^#/, ""));
            }
        }
    },
    historyLoad : function(hash) {
        var newhash;
        hash = decodeURIComponent(hash.replace(/\?.*$/, ""));

        if (jQuery.browser.safari) {
            newhash = hash;
        } else {
            newhash = "#" + hash;
            location.hash = newhash;
        }
        jQuery.historyCurrentHash = newhash;

        if (jQuery.historyNeedIframe) {
            var ihistory = jQuery("#jQuery_history")[0];
            var iframe = ihistory.contentWindow.document;
            iframe.open();
            iframe.close();
            iframe.location.hash = newhash;
            jQuery.lastHistoryLength = history.length;
            jQuery.historyCallback(hash);
        } else if (jQuery.browser.safari) {
            jQuery.dontCheck = true;
            // Manually keep track of the history values for Safari
            this.historyAddHistory(hash);

            // Wait a while before allowing checking so that Safari has time to update the "history" object
            // correctly (otherwise the check loop would detect a false change in hash).
            var fn = function() {
                jQuery.dontCheck = false;
            };
            window.setTimeout(fn, 200);
            jQuery.historyCallback(hash);
            // N.B. "location.hash=" must be the last line of code for Safari as execution stops afterwards.
            //      By explicitly using the "location.hash" command (instead of using a variable set to "location.hash") the
            //      URL in the browser and the "history" object are both updated correctly.
            location.hash = newhash;
        } else {
            jQuery.historyCallback(hash);
        }
    }
});
