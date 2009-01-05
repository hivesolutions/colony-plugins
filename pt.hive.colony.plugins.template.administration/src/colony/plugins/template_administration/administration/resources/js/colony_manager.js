// Hive Colony Framework
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
// __revision__  = $LastChangedRevision: 684 $
// __date__      = $LastChangedDate: 2008-12-08 15:16:55 +0000 (seg, 08 Dez 2008) $
// __copyright__ = Copyright (c) 2008 Hive Solutions Lda.
// __license__   = GNU General Public License (GPL), Version 3

function escapeDots(stringValue) {
	var escapedStringValue = trim(stringValue).replace(/\./g, "-");
	return escapedStringValue;
}

function trim(stringValue) {
	var rightTrimedStringValue = rightTrim(stringValue)
	var trimedStringValue = leftTrim(rightTrimedStringValue)
	return trimedStringValue;
}

function rightTrim(stringValue) {
	var trimedStringValue = stringValue.replace(/^\s+/, "");
    return trimedStringValue;
}

function leftTrim(stringValue) {
	var trimedStringValue = stringValue.replace(/\s+$/, "");
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
	responseTextTrimed = rightTrim(responseText);
	return responseTextTrimed.split("\n");
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
