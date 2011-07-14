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
// __revision__  = $LastChangedRevision: 195 $
// __date__      = $LastChangedDate: 2008-10-26 20:43:25 +0000 (dom, 26 Out 2008) $
// __copyright__ = Copyright (c) 2008 Hive Solutions Lda.
// __license__   = General Public License (GPL), Version 3

/**
 * Switches the login state.
 */
switchLogin = function() {
    // retrieves the login username element
    var loginUsername = document.getElementById("login-username");

    // retrieves the login password element
    var loginPassword = document.getElementById("login-password");

    // retrieves the login loading element
    var loginLoading = document.getElementById("login-loading");

    // retrieves the login button element
    var loginButton = document.getElementById("login-button");

    // retrieves the login registration element
    var loginRegistration = document.getElementById("login-registration");

    // retrieves the login username style
    var loginUsernameStyle = loginUsername.style;

    // retrieves the login password style
    var loginPasswordStyle = loginPassword.style;

    // retrieves the login loading style
    var loginLoadingStyle = loginLoading.style;

    // retrieves the login registration style
    var loginRegistrationStyle = loginRegistration.style;

    if (loginLoadingStyle.display == "inline") {
        loginUsernameStyle.display = "inline"
        loginPasswordStyle.display = "inline"
        loginLoadingStyle.display = "none";
        loginButton.textContent = "Login";
        loginRegistrationStyle.display = "inline";
    } else {
        loginUsernameStyle.display = "none"
        loginPasswordStyle.display = "none"
        loginLoadingStyle.display = "inline";
        loginButton.textContent = "Cancel";
        loginRegistrationStyle.display = "none";
    }
}
