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

var browserDetect = {
    init : function() {
        this.browser = this.searchString(this.dataBrowser)
                || "An unknown browser";
        this.version = this.searchVersion(navigator.userAgent)
                || this.searchVersion(navigator.appVersion)
                || "an unknown version";
        this.os = this.searchString(this.dataOS) || "an unknown OS";
    },
    searchString : function(data) {
        for (var i = 0; i < data.length; i++) {
            var dataString = data[i].string;
            var dataProp = data[i].prop;
            this.versionSearchString = data[i].versionSearch
                    || data[i].identity;
            if (dataString) {
                if (dataString.indexOf(data[i].subString) != -1)
                    return data[i].identity;
            } else if (dataProp)
                return data[i].identity;
        }
    },
    searchVersion : function(dataString) {
        var index = dataString.indexOf(this.versionSearchString);
        if (index == -1)
            return;
        return parseFloat(dataString.substring(index
                + this.versionSearchString.length + 1));
    },
    dataBrowser : [{
                string : navigator.userAgent,
                subString : "Chrome",
                identity : "Chrome"
            }, {
                string : navigator.userAgent,
                subString : "OmniWeb",
                versionSearch : "OmniWeb/",
                identity : "OmniWeb"
            }, {
                string : navigator.vendor,
                subString : "Apple",
                identity : "Safari",
                versionSearch : "Version"
            }, {
                prop : window.opera,
                identity : "Opera"
            }, {
                string : navigator.vendor,
                subString : "iCab",
                identity : "iCab"
            }, {
                string : navigator.vendor,
                subString : "KDE",
                identity : "Konqueror"
            }, {
                string : navigator.userAgent,
                subString : "Firefox",
                identity : "Firefox"
            }, {
                string : navigator.vendor,
                subString : "Camino",
                identity : "Camino"
            }, { // for newer Netscapes (6+)
                string : navigator.userAgent,
                subString : "Netscape",
                identity : "Netscape"
            }, {
                string : navigator.userAgent,
                subString : "MSIE",
                identity : "Explorer",
                versionSearch : "MSIE"
            }, {
                string : navigator.userAgent,
                subString : "Gecko",
                identity : "Mozilla",
                versionSearch : "rv"
            }, { // for older Netscapes (4-)
                string : navigator.userAgent,
                subString : "Mozilla",
                identity : "Netscape",
                versionSearch : "Mozilla"
            }],
    dataOS : [{
                string : navigator.platform,
                subString : "Win",
                identity : "Windows"
            }, {
                string : navigator.platform,
                subString : "Mac",
                identity : "Mac"
            }, {
                string : navigator.userAgent,
                subString : "iPhone",
                identity : "iPhone/iPod"
            }, {
                string : navigator.platform,
                subString : "Linux",
                identity : "Linux"
            }]
};

// initializes the browser detection system
browserDetect.init();
