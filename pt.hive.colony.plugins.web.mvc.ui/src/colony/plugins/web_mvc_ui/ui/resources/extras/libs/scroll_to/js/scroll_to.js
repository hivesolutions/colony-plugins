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

/**
 * jQuery scroll to plugin, this jQuery plugin is a simple scroll to
 * implementation meant to be used in http://hive.pt website.
 *
 * @name jquery-slideshow.js
 * @author João Magalhães <joamag@hive.pt>
 * @version 1.0
 * @date March 10, 2010
 * @category jQuery plugin
 * @copyright Copyright (c) 2010 Hive Solutions Lda.
 * @license Hive Solutions Confidential Usage License (HSCUL) -
 *          http://www.hive.pt/licenses/
 * @credits Ariel Flesler <aflesler@gmail.com>
 */
(function($) {
    var $scrollTo = $.scrollTo = function(target, duration, settings) {
        $(window).scrollTo(target, duration, settings);
    };

    $scrollTo.defaults = {
        axis : "xy",
        duration : parseFloat($.fn.jquery) >= 1.3 ? 0 : 1
    };

    /**
     * Returns the element that needs to be animated to scroll the window.
     *
     * @param {Object}
     *            scope The current scope to be used.
     * @return {Element} The input element.
     */
    $scrollTo.window = function(scope) {
        return $(window)._scrollable();
    };

    /**
     * Returns the real elements to scroll (supports window/iframes, documents
     * and regular nodes).
     *
     * @return {Element} The input element.
     */
    $.fn._scrollable = function() {
        return this.map(function() {
                    var element = this, isWin = !element.nodeName
                            || $.inArray(element.nodeName.toLowerCase(), [
                                            "iframe", "#document", "html",
                                            "body"]) != -1;

                    if (!isWin)
                        return element;

                    var doc = (element.contentWindow || element).document
                            || element.ownerDocument || element;

                    return $.browser.safari || doc.compatMode == "BackCompat"
                            ? doc.body
                            : doc.documentElement;
                });
    };

    $.fn.scrollTo = function(target, duration, settings) {
        if (typeof duration == "object") {
            settings = duration;
            duration = 0;
        }

        if (typeof settings == "function") {
            settings = {
                onAfter : settings
            };
        }

        if (target == "max") {
            target = 9e9;
        }

        settings = $.extend({}, $scrollTo.defaults, settings);

        // speed is still recognized for backwards compatibility
        duration = duration || settings.speed || settings.duration;

        // make sure the settings are given right
        settings.queue = settings.queue && settings.axis.length > 1;

        if (settings.queue) {
            // let's keep the overall duration
            duration /= 2;
        }

        settings.offset = both(settings.offset);
        settings.over = both(settings.over);

        return this._scrollable().each(function() {
            var element = this, $element = $(element), targ = target, toff, attr = {}, win = $element.is('html,body');

            switch (typeof targ) {
                // in case it's a number or string
                // will pass the regex
                case "number" :
                case "string" :
                    if (/^([+-]=)?\d+(\.\d+)?(px|%)?$/.test(targ)) {
                        targ = both(targ);
                        break;
                    }
                    // relative selector, avoids break
                    targ = $(targ, this);
                case "object" :
                    // in case it's a dom element or jquery element
                    if (targ.is || targ.style) {
                        // retrieves the real position of the target
                        toff = (targ = $(targ)).offset();
                    }
            }

            $.each(settings.axis.split(""), function(i, axis) {
                var Pos = axis == "x" ? "Left" : "Top", pos = Pos.toLowerCase(), key = "scroll"
                        + Pos, old = element[key], max = $scrollTo.max(element,
                        axis);

                if (toff) {
                    attr[key] = toff[pos]
                            + (win ? 0 : old - $element.offset()[pos]);

                    // in case it's a dom element, reduces the margin
                    if (settings.margin) {
                        attr[key] -= parseInt(targ.css("margin" + Pos)) || 0;
                        attr[key] -= parseInt(targ.css("border" + Pos + "Width"))
                                || 0;
                    }

                    attr[key] += settings.offset[pos] || 0;

                    if (settings.over[pos])
                        // scrolls to a fraction of its width/height
                        attr[key] += targ[axis == "x" ? "width" : "height"]()
                                * settings.over[pos];
                } else {
                    var val = targ[pos];
                    // handles the percentage values
                    attr[key] = val.slice && val.slice(-1) == "%"
                            ? parseFloat(val) / 100 * max
                            : val;
                }

                // in case it's umber or "number"
                if (/^\d+$/.test(attr[key])) {
                    // checks the limits
                    attr[key] = attr[key] <= 0 ? 0 : Math.min(attr[key], max);
                }

                // in case it's queueing axes
                if (!i && settings.queue) {
                    // avoids wasting time animating, if there's no need
                    if (old != attr[key]) {
                        // intermediate animation
                        animate(settings.onAfterFirst);
                    }

                    // avoid animating this axis again in the next iteration
                    delete attr[key];
                }
            });

            animate = function(callback) {
                $element.animate(attr, duration, settings.easing, callback
                                && function() {
                                    callback.call(this, target, settings);
                                });
            };

            animate(settings.onAfter);
        }).end();
    };

    /**
     * Goes to maximum scrolling, works on quirks mode It only fails (not too
     * badly) on IE, quirks mode.
     *
     * @param {Element}
     *            element The element to be used aas reference for the scroll.
     * @param {String}
     *            axis The axis to be used in scroll reference.
     * @return {Element} The input element.
     */
    $scrollTo.max = function(element, axis) {
        var Dim = axis == "x" ? "Width" : "Height", scroll = "scroll" + Dim;

        if (!$(element).is("html,body"))
            return element[scroll] - $(element)[Dim.toLowerCase()]();

        var size = "client" + Dim, html = element.ownerDocument.documentElement, body = element.ownerDocument.body;

        return Math.max(html[scroll], body[scroll])
                - Math.min(html[size], body[size]);
    };

    var both = function(val) {
        return typeof val == "object" ? val : {
            top : val,
            left : val
        };
    };
})(jQuery);
