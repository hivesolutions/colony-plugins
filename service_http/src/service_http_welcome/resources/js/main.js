// Hive Colony Framework
// Copyright (c) 2008-2020 Hive Solutions Lda.
//
// This file is part of Hive Colony Framework.
//
// Hive Colony Framework is free software: you can redistribute it and/or modify
// it under the terms of the Apache License as published by the Apache
// Foundation, either version 2.0 of the License, or (at your option) any
// later version.
//
// Hive Colony Framework is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
// Apache License for more details.
//
// You should have received a copy of the Apache License along with
// Hive Colony Framework. If not, see <http://www.apache.org/licenses/>.

// __author__    = João Magalhães <joamag@hive.pt>
// __version__   = 1.0.0
// __revision__  = $LastChangedRevision$
// __date__      = $LastChangedDate$
// __copyright__ = Copyright (c) 2008-2020 Hive Solutions Lda.
// __license__   = Apache License, Version 2.0

/**
 * Thw welcome logo images list.
 *
 * @type List
 */
WELCOME_LOGO_IMAGES = ["/welcome_handler/images/colony_welcome_screen_1.png",
    "/welcome_handler/images/colony_welcome_screen_2.png",
    "/welcome_handler/images/colony_welcome_screen_3.png"
]

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
