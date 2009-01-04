function escapeDots(stringValue) {
	var escapedStringValue = trim(stringValue).replace(/\./g, "-");
	return escapedStringValue;
}

function trim(stringValue) {
	var trimedStringValue = stringValue.replace(/\n/g, "");
	return trimedStringValue;
}

function endPluginLoad(responseText, textStatus) {
	var pluginIdsList = processAnswer(responseText);

	for (var i = 0; i < pluginIdsList.length; i++) {
		var pluginId = pluginIdsList[i];
		if (pluginId != "") {
			var element = $("#" + escapeDots(pluginId))
			element.fadeOut("fast", endPluginLoadFadeOut)
		}
	}
}

function endPluginUnLoad(responseText, textStatus) {
	var pluginIdsList = processAnswer(responseText);

	for (var i = 0; i < pluginIdsList.length; i++) {
		var pluginId = pluginIdsList[i];
		if (pluginId != "") {
			var element = $("#" + escapeDots(pluginId))
			element.fadeOut("fast", endPluginUnLoadFadeOut);
		}
	}
}

function endPluginUnLoadFadeOut() {
	var element = $(this)
	element.removeClass("loaded");
	element.addClass("unloaded");
	element.html("UNLOADED");
	element.fadeIn("fast");
	$("#pluginManagement").trigger("update");
}

function endPluginLoadFadeOut() {
	var element = $(this)
	element.removeClass("unloaded");
	element.addClass("loaded");
	element.html("LOADED");
	element.fadeIn("fast");
	$("#pluginManagement").trigger("update");
}

function processAnswer(responseText) {
	return responseText.split("\n");
}

function loadPlugin(pluginId) {
	var value = $("#" + escapeDots(pluginId)).html()

	if (value == "LOADED") {
		var type = "unload";
		var handler = endPluginUnLoad;
	} else if (value == "UNLOADED") {
		var type = "load";
		var handler = endPluginLoad;
	}

	$.post("plugin_loader.ctp", {
				"pluginId" : pluginId,
				"type" : type
			}, handler);
}

function tryLogin(username, password) {
	$("#loginMessage").html("Trying to login...");
	$("#loginMessage").fadeIn("fast");
	$.post("login_validator.ctp", {
				"username" : username,
				"password" : password
			}, loginHandler);
}

function loginHandler(responseText, textStatus) {
	var answerList = processAnswer(responseText);
	var returnValue = answerList[0];

	if (returnValue == "True")
		setTimeout("tryLoginSuccessful();", 500);
	else
		setTimeout("tryLoginUnsuccessful();", 500);
}

function tryLoginSuccessful() {
	$("#loginMessage").hide();
	$("#loginForm").slideUp("slow", endLogin);
}

function tryLoginUnsuccessful() {
	$("#loginMessage").html("Login Unsuccessful...");
	$("#loginMessage").fadeIn("fast");
	$("#loginFormShaker").effect("shake", {
				times : 3
			}, 75);
}

function endLogin() {
	$("#loginFormContainer").hide()
	loadMain()
}

function loadMain() {
	$("#mainDiv").show();
	$("#pluginManagement").tablesorter();
	$("#mainTabPanel > ul").tabs();
	$("#mainAccordionMenu").accordion();
	hideHidable();
}

function hideHidable() {
	items = $(".hidable");

	items.each(function() {
				$(this).hide();
			});
}
