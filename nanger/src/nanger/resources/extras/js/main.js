// Hive Colony Framework
// Copyright (c) 2008-2012 Hive Solutions Lda.
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
// __revision__  = $LastChangedRevision$
// __date__      = $LastChangedDate$
// __copyright__ = Copyright (c) 2008-2012 Hive Solutions Lda.
// __license__   = GNU General Public License (GPL), Version 3

jQuery(document).ready(function() {
    jQuery(".console").click(function() {
                var element = jQuery(this);
                var text = jQuery(".text", element);
                text.focus();
            });

    jQuery(".console .text").keyup(function() {
                var element = jQuery(this);
                jQuery(".console .line").html(element.val());
            });

    jQuery(".console .text").keypress(function(event) {
        // retrieves the element
        var element = jQuery(this);

        // retrieves the key value
        var keyValue = event.keyCode ? event.keyCode : event.charCode
                ? event.charCode
                : event.which;

        // switches over the key value
        switch (keyValue) {
            case 13 :
                var value = element.val();

                // tenho de chamar a execucao do comando
                // neste ponto
                jQuery.ajax({
                    url : "console/execute",
                    data : {
                        command : value,
                        instance : jQuery(".console").data("instance")
                    },
                    success : function(data) {
                        var result = data["result"];
                        var instance = data["instance"];

                        jQuery(".console").data("instance", instance);

                        element.val("");
                        jQuery(".console .previous").append("<div><span class=\"prompt\"># </span><span>"
                                + value + "</span></div>");
                        var resultLine = jQuery("<span></span>");
                        resultLine.text(result);
                        var line = resultLine.html();
                        line = line.replace(/\n/g, "<br/>");
                        line = line.replace(/ /g, "&nbsp;");
                        jQuery(".console .previous").append("<div>" + line
                                + "</div>");
                        jQuery(".console .line").html("");
                        jQuery(".console").scrollTop(jQuery(".console")[0].scrollHeight);
                    }
                });

                // breaks the switch
                break;

            default :
                jQuery(".console .line").html(element.val());

                break;
        }
    });

    jQuery(".console .text").keydown(function() {
                var element = jQuery(this);
                jQuery(".console .line").html(element.val());
            });

    jQuery(".console .text").focus(function() {
                jQuery(".console .cursor").css("display", "inline-block");
            });

    jQuery(".console .text").blur(function() {
                jQuery(".console .cursor").css("display", "none");
            });

    // resets the console text to avoid any possible auto
    // complete operation
    jQuery(".console .text").val("");

    // "clicks" in the console so that the focus is started
    // at the console (immediate interaction)
    jQuery(".console").click();
});
