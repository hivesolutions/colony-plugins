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

            jQuery(".console .text").keypress(function() {
                        var element = jQuery(this);
                        jQuery(".console .line").html(element.val());
                    });

            jQuery(".console .text").keydown(function() {
                        var element = jQuery(this);
                        jQuery(".console .line").html(element.val());
                    });

            jQuery(".console .text").focus(function() {
                        jQuery(".console .cursor").css("display",
                                "inline-block");
                    });

            jQuery(".console .text").blur(function() {
                        jQuery(".console .cursor").css("display", "none");
                    });
        });
