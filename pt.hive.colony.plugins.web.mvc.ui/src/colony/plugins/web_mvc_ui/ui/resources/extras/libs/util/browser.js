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
