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

function onClick(event) {
    // prevents the default event
    event.preventDefault();

    // retrieves the element's href
    var href = event.srcElement.href;

    // retrieves the post form
    var postForm = document.getElementById("post-form");

    // sets the form's href
    postForm.setAttribute("action", href);

    // submits the form
    postForm.submit();
}

function onLoad() {
    // retrieves the delete elements
    var deleteElements = document.getElementsByName("delete");

    // retrieves the delete elements length
    var deleteElementsLength = deleteElements.length;

    // for each delete element
    for(var index = 0; index < deleteElementsLength; index++) {
        // retrieves the delete element
        var deleteElement = deleteElements[index];

        // registers the on click event
        deleteElement.onclick = onClick;
    }
}

// sets the on load handler
window.onload = onLoad;
