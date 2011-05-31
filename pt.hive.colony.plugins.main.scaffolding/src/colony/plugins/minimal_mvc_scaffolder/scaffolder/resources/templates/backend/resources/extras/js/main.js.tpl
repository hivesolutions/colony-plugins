function onClick(event) {
    // prevents the default event
    event.preventDefault();

    // posts the form to delete item
    var postForm = document.getElementById("post-form");
    postForm.setAttribute("action", event.srcElement.href);
    postForm.submit();
}

function onLoad() {
    // registers the on click event for all delete elements
    var deleteElements = document.getElementsByName("delete");
    for(var index = 0; index < deleteElements.length; index++) {
        var deleteElement = deleteElements[index];
        deleteElement.onclick = onClick;
    }
}

// sets the on load handler
window.onload = onLoad;
