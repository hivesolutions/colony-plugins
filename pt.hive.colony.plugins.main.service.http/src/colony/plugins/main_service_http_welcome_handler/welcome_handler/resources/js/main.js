// Hive Colony Web Framework
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

// __author__    = João Magalhães <joamag@hive.pt>
// __version__   = 1.0.0
// __revision__  = $LastChangedRevision: 195 $
// __date__      = $LastChangedDate: 2008-10-26 20:43:25 +0000 (dom, 26 Out 2008) $
// __copyright__ = Copyright (c) 2008 Hive Solutions Lda.
// __license__   = General Public License (GPL), Version 3

/**
 * Thw welcome logo images list.
 *
 * @type List
 */
WELCOME_LOGO_IMAGES = ["/welcome_handler/images/colony_welcome_screen_1.png",
        "/welcome_handler/images/colony_welcome_screen_2.png",
        "/welcome_handler/images/colony_welcome_screen_3.png"]

/**
 * Function called uppon loading of the document (window).
 */
function onLoad() {
    // retrieves the welcome logo images length
    var welcomeLogoImagesLenght = WELCOME_LOGO_IMAGES.length;

    // retrieves the random welcome logo images index
    var welcomeLogoImagesIndex = parseInt(Math.random() * 3);

    // retrieves the welcome logo image (source path)
    var welcomeLogoImage = WELCOME_LOGO_IMAGES[welcomeLogoImagesIndex];

    // retrieves the welcome logo element
    var welcomeLogo = document.getElementById("welcome-logo");

    // sets the welcome logo image in the welcome logo element
    welcomeLogo.src = welcomeLogoImage;
}
