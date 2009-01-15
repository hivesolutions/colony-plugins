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
// __revision__  = $LastChangedRevision: 684 $
// __date__      = $LastChangedDate: 2008-12-08 15:16:55 +0000 (seg, 08 Dez 2008) $
// __copyright__ = Copyright (c) 2008 Hive Solutions Lda.
// __license__   = GNU General Public License (GPL), Version 3

// called uppon document loading complete
$(document).ready(function() {
	// hides the main div
	$("#mainDiv").hide();

	// hides all the windows
	hideWindows();

	$(".listBox > div").click(function() {
				var divParent = $(this).parent();
				var selectedElements = divParent.children(".listBoxElementSelected");
				selectedElements.each(function() {
							$(this).removeClass("listBoxElementSelected");
						});
				$(this).addClass("listBoxElementSelected");
			});

	// called uppon clicking in the login link
	$("#loginLink").click(function() {
				if ($("#loginForm").is(":hidden")) {
					$("#loginForm").slideDown("slow");
				} else {
					$("#loginForm").slideUp("slow");
				}
			});

	$("#loginFormContainer").contextMenu({
				menu : "pluginContextMenu"
			}, function(action, el, pos) {
				alert('Action: ' + action + '\n\n' + 'Element ID: '
						+ $(el).attr('id') + '\n\n' + 'X: ' + pos.x + '  Y: '
						+ pos.y + ' (relative to element)\n\n' + 'X: '
						+ pos.docX + '  Y: ' + pos.docY
						+ ' (relative to document)');
			});

	$("#tooltip").hide();
	$("#emailIcon").mouseover(function(event) {
		$("#tooltipTitle").html("New Mails");
		$("#tooltipBody").html("2 new joamag@hive.pt<br>1 new tsilva@hive.pt<br>");
		emailIconPosition = $("#emailIcon").position()
		$("#tooltip").css("top", (emailIconPosition.top + 20) + "px")
		$("#tooltip").css("left", (emailIconPosition.left - 133) + "px")
		$("#tooltip").fadeIn("normal");
	});

	$("#emailIcon").mouseout(function(event) {
				$("#tooltip").fadeOut("normal");
			});

	$("#bugIcon").mouseover(function(event) {
		$("#tooltipTitle").html("Bug Status");
		$("#tooltipBody").html("2 high priority bugs<br>3 medium priority bugs<br>7 low priority bugs<br>");
		bugIconPosition = $("#bugIcon").position()
		emailIconPosition = $("#emailIcon").position()
		$("#tooltip").css("top", (bugIconPosition.top + 20) + "px")
		$("#tooltip").css("left", (emailIconPosition.left - 133) + "px")
		$("#tooltip").fadeIn("normal");
	});
	$("#bugIcon").mouseout(function(event) {
				$("#tooltip").fadeOut("normal");
			});

	$.jGrowl.defaults.closeTemplate = "<img src='./pics/icons/cross.png'/>"
	$.jGrowl.defaults.closerTemplate = "<div>close all</div>'";
	$.jGrowl.defaults.theme = "colony";

	$("#clickNotification").click(function() {
		$("#jgrowlNotifier").jGrowl("joamag@hive.pt<br>Welcome to hive.pt", {
			life : 5000,
			header : "<img src='./pics/icons/email.png' style='float: left;'/><span style='margin-left: 5px;'>New Mail</span>"
		});
	});

	$("#settingsButton").click(function() {
				$("#settingsWindow").show();
				$("#settingsWindow").dialog({
							"width" : 430,
							"height" : 140,
							"show" : "drop",
							"hide" : "drop"
						});
			});

	$("#testBox").colonyButton("tobias", {
				"size" : "large",
				"click" : function() {
					alert("tobias")
				},
				"image" : "pics/add.png"
			});

	// creates a new data store
	var dataStore = $("#testBox").colonyDataStore({});

	// creates the test list box
	$("#testDiv").colonyListBox(dataStore);

	// adds two elments into the data store
	$("#testBox").colonyDataStoreAddElement("joao", "CEO");
	$("#testBox").colonyDataStoreAddElement("tiago", "vice-CEO");

	$("#testBox").colonyDataStoreRemoveElement("tiago");
});

var tabsMap = {};

function addTab(tabDivId, tabName) {
	// in case the tab is already opened
	if (!(tabsMap[tabDivId] == null))
		return

	// retrieves the tabs length
	var tabsLength = $("#mainTabPanel > ul").tabs("length");

	// sets the initial index of tab div
	tabsMap[tabDivId] = tabsLength;

	// adds the tab to the main tab panel
	$("#mainTabPanel > ul").tabs(
			"add",
			"#" + tabDivId,
			tabName
					+ " <img onclick='removeTab(\""
					+ tabDivId
					+ "\")' src='./pics/icons/bullet_red.png' style='border:0px;'/>");

	// selects the added tab
	$("#mainTabPanel > ul").tabs("select", tabsLength);
}

function removeTab(tabDivId) {
	// retrieves the tab index
	var index = tabsMap[tabDivId];

	// deletes the tabs map element
	delete tabsMap[tabDivId];

	// iterates over all the tab divs in the tabs map
	for (tabDivIdKey in tabsMap) {
		// retrieves the tab index
		var tabIndex = tabsMap[tabDivIdKey];

		// in case the tab index is greater than the current index
		if (tabIndex > index)
			// decrements the tab index
			tabIndex--;

		// sets the tabs map key new value
		tabsMap[tabDivIdKey] = tabIndex;
	}

	// selects the tab div
	var tabDiv = $("#" + tabDivId);

	// removes the ui tabs panel class from the tab div
	tabDiv.removeClass("ui-tabs-panel");

	// appends the tab div to the extraContentItems div
	tabDiv.prependTo("#extraContentItems");

	// selects all the ui tab navs
	var uiTabsNavs = $(".ui-tabs-nav");

	// retrieves the first ui tab nav
	var firstUiTabNav = $(uiTabsNavs[0]);

	// retrieves the tab indicator for the given tab index
	var tabHeader = $(firstUiTabNav.children()[index]);

	// removes the tab header
	tabHeader.remove()

	// retrieves the first ui tab nav data
	var firstUiTabNavData = $.data(uiTabsNavs[0], "tabs");

	// tabifies the tab container
	firstUiTabNavData.tabify();

	// retrieves the tabs length
	var tabsLength = $("#mainTabPanel > ul").tabs("length");

	// in case there is more tabs to the right
	if (index < tabsLength)
		// selects the tab to the right
		$("#mainTabPanel > ul").tabs("select", index);
	else
		// selects the tab to the left
		$("#mainTabPanel > ul").tabs("select", index - 1);
}

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

function processAnswer(responseText) {
	responseTextTrimed = rightTrim(responseText);
	return responseTextTrimed.split("\n");
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
	// shows the main div
	$("#mainDiv").show();

	$("#pluginManagement").tablesorter();
	$("#mainTabPanel > ul").tabs();
	$("#mainAccordionMenu").accordion();
	hideHidable();
}

function hideHidable() {
	hidableItems = $(".hidable");

	hidableItems.each(function() {
				$(this).hide();
			});
}

function hideWindows() {
	windowItems = $(".window");

	windowItems.each(function() {
				$(this).hide();
			});
}
