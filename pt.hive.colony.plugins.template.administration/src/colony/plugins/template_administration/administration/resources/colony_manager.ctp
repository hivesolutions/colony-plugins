<!DOCTYPE html 
    PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" 
    "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd"> 
<html xmlns="http://www.w3.org/1999/xhtml" lang="en" xml:lang="en"> 

<!-- the head of the html -->
<head> 
    <title><?colony print "Hive Colony Manager" ?></title>
    <?colony self.import_js_library("jquery") ?>
    <?colony self.import_js_library("jquery.ui.core") ?>
    <?colony self.import_js_library("jquery.ui.tabs") ?>
    <?colony self.import_js_library("jquery.ui.accordion") ?>
    <?colony self.import_js_library("jquery.ui.effects.core") ?>
    <?colony self.import_js_library("jquery.ui.effects.bounce") ?>
    <?colony self.import_js_library("jquery.ui.effects.shake") ?>
    <?colony self.import_js_library("jquery.ui.effects.pulsate") ?>
    <?colony self.import_js_library("jquery.tablesorter") ?>
    <?colony self.import_js_library("jquery.contextmenu") ?>
    <?colony self.import_js_library("jquery.jgrowl") ?>
    <script type="text/javascript" src="./js/colony_manager.js"></script>
    <link rel="stylesheet" href="./css/jquery.contextmenu.css" type="text/css">
    <link rel="stylesheet" href="./css/jquery.jgrowl.css" type="text/css">
    <link rel="stylesheet" href="jquery_themes/humanity/ui.theme.css" type="text/css" media="screen" title="Themeroller (Default)">
    <link rel="stylesheet" href="./css/colony_manager.css" type="text/css">
</head>

<body>

<script type="text/javascript">
$(document).ready(function() {
    $("#mainDiv").hide();
    $("#loginLink").click(function(){
        if ($("#loginForm").is(":hidden")){
            $("#loginForm").slideDown("slow");
        }
        else{
            $("#loginForm").slideUp("slow");
        }
    });
    $("#loginFormContainer").contextMenu({
        menu: "pluginContextMenu"
	}, function(action, el, pos) {
        alert(
            'Action: ' + action + '\n\n' +
            'Element ID: ' + $(el).attr('id') + '\n\n' + 
            'X: ' + pos.x + '  Y: ' + pos.y + ' (relative to element)\n\n' + 
            'X: ' + pos.docX + '  Y: ' + pos.docY+ ' (relative to document)'
        );
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
        $("#jgrowlNotifier").jGrowl("joamag@hive.pt<br>Welcome to hive.pt", { life: 5000, header: "<img src='./pics/icons/email.png' style='float: left;'/><span style='margin-left: 5px;'>New Mail</span>"});
    });
    
    $("#addTab").click(function() {
        // retrieves the tabs length
        tabsLength = $("#mainTabPanel > ul").tabs("length");
        $("#mainTabPanel > ul").tabs("add", "#newTab", "tobias <img onclick='$(\"#mainTabPanel > ul\").tabs(\"remove\"," + tabsLength + ")'  src='./pics/icons/bullet_red.png' style='border:0px;'/>");
    });
});
</script>

<div id="clickNotification">
Clica para ver notificacao
</div>

<div id="addTab">
Clica para adicionar tab
</div>

<div id="newTab">
Nova tab
</div>

<div id="jgrowlNotifier"></div>

<div id="tooltip">
    <div id="tooltipTitle">
    </div>
    <div id="tooltipBody">
    </div>
</div>

<div id="loginFormContainer">
    <div id="loginFormShaker">
        <div id="loginForm">
            <fieldset>
                <label for="Login" class="mainTitle">Login:</label>
                <input id="login" type="text" />
                <label for="Password" class="mainTitle">Password:</label>
                <input id="password" type="password" />
                <label for="Login Type" class="mainTitle">Login Type:</label>
                <input id="login_type" type="text" />
                <table>
                <tr>
                    <td><input id="submitLogin" class="mainTitle" value="Login" type="submit" name="submit" onclick="tryLogin($('#login').attr('value'), $('#password').attr('value'))" /></td>
                    <td><span id="loginMessage" class="mainTitle">Trying to login...</span></td>
                </tr>
                </table>
            </fieldset>
        </div>
        <div id="loginLink"></div>
    </div>
</div>

<div id="mainDiv">
    <table id="mainTable">
        <tr>
            <div style="float: right;">
                <p id="topMenuBar" class="mainTitle">username: tobias | Settings | Help | About | Sign Out</p>
            </div>
            <div>
                <p class="mainTitle">Manager | Forum | Development</p>
            </div>
        </tr>
        <tr>
            <td>
                <img src="./pics/hive_logo_development.png">
            </td>
            <td class="mainPanelCell3">
                <div id="mainStatusBar">
                    <!-- The search Form -->
                    <div id="searchForm">
                        <table align="right">
                            <tr>
                                <td>
                                    <div style="text-align: right;">
                                        <span class="mainTitle" style="text-align: right;">
                                            <img id="bugIcon" src="./pics/icons/bug.png"/>
                                            <img src="./pics/icons/brick.png"/>
                                            <img src="./pics/icons/building.png"/>
                                            <img id="emailIcon" src="./pics/icons/email.png"/>
                                        </span>
                                    </div>
                                </td>
                            </tr>
                            <tr>
                                <td><input id="searchInput" type="text" /></td>
                            </tr>
                        </table>
                    </div>
                </div>
            </td>
        </tr>
        <tr>
            <td class="mainPanelCell">
                <div class="lateralMenu">
                    <table id="menuTable">
                        <tr>
                            <td class="menuItem">
                                <div onclick="$('#colonyMenuItems').slideToggle('normal')">
                                    <span class="mainTitle menuItem">Colony</span>
                                </div>
                                <div id="colonyMenuItems" class="itemsMenu hidable">
                                    <table>
                                        <tr><td>Colony Plugin Administration<td></tr>
                                        <tr><td>Colony Information</td></tr>
                                    </table>
                                </div>
                            </td>
                        </tr>
                        <tr>
                            <td class="menuItem">
                                <div onclick="$('#buildAutomationMenuItems').slideToggle('normal')">
                                    <span class="mainTitle menuItem">Build Automation</span>
                                </div>
                                 <div id="buildAutomationMenuItems" class="itemsMenu hidable">
                                    <table>
                                        <tr><td>Automation Administration<td></tr>
                                        <tr><td>Scheduling Results</td></tr>
                                    </table>
                                </div>
                            </td>
                        </tr>
                        <tr>
                            <td class="menuItem">
                                <div onclick="$('#bonjourMenuItems').slideToggle('normal')">
                                    <span class="mainTitle menuItem">Bonjour</span>
                                </div>
                                <div id="bonjourMenuItems" class="itemsMenu hidable">
                                    <table>
                                        <tr><td>Bonjour Administration<td></tr>
                                    </table>
                                </div>
                            </td>
                        </tr>
                    </table>
                </div>
            </td>
            <td class="mainPanelCell2">
                <div id="mainTabPanel" class="flora">
                    <ul>
                        <li><a href="#fragment-1"><span>Colony Plugin Administration <img src='./pics/icons/bullet_red.png' style='border:0px;'/></span></a></li>
                        <li><a href="#fragment-2"><span>Automation Administration <img src='./pics/icons/bullet_red.png' style='border:0px;'/></span></a></li>
                        <li><a href="#fragment-3"><span>Bonjour Administration <img src='./pics/icons/bullet_red.png' style='border:0px;'/></span></a></li>
                    </ul>
                    <div id="fragment-1">
                        <h2 class="mainTitle">The plugins list</h2>
                        <p>Here you can do some plugin manager management: </p>
                        <?colony
all_plugins = plugin_manager.get_all_plugins()
print "<table id=pluginManagement class=\"pluginsTable\">"
print "<thead> <tr> <th class=\"mainTitle tableHeader\">PLUGIN ID</th> <th class=\"mainTitle tableHeader\">NAME</th> <th class=\"mainTitle tableHeader\">AUTHOR</th>  <th class=\"mainTitle tableHeader\">STATUS</th> </tr> </thead>"
print "<tbody>"
for plugin in all_plugins:
    print "<tr>"
    print "<td class=\"mainTitle\" onclick=\"$('#details-" + self.escape_dots(plugin.id) + "').slideToggle('normal')\" class=\"itemValue\">" + plugin.id + "</td>"
    print "<td class=\"itemValue\">" + plugin.name + "</td>"
    print "<td class=\"itemValue\">" + plugin.author + "</td>"
    if plugin.is_loaded():
        print "<td style=\"border: 1px dashed #888897;\" id=\"" + self.escape_dots(plugin.id) + "\" class=\"loaded\" onclick=\"loadPlugin('" + plugin.id + "')\">LOADED</td>"
    else:
        print "<td style=\"border: 1px dashed #888897;\" id=\"" + self.escape_dots(plugin.id) + "\" class=\"unloaded\" onclick=\"loadPlugin('" + plugin.id + "')\">UNLOADED</td>"
    print "</tr>"
    print "<tr class=\"hiddenItemValue\">"
    print "<td colspan=4>"
    print "<div id=\"details-" + self.escape_dots(plugin.id) + "\" class=\"hiddenPluginDetails hidable\">"
    print "<table>"
    print "<tr><td class=\"pluginDetailsIdColumn\"><b>ID</b></td><td>" + plugin.id + "</td></tr>"
    print "<tr><td class=\"pluginDetailsIdColumn\"><b>SHORT NAME</b></td><td>" + plugin.short_name + "</td></tr>"
    print "<tr><td class=\"pluginDetailsIdColumn\"><b>NAME</b></td><td>" + plugin.name + "</td></tr>"
    print "<tr><td class=\"pluginDetailsIdColumn\"><b>DESCRIPTION</b></td><td>" + plugin.description + "</td></tr>"
    print "<tr><td class=\"pluginDetailsIdColumn\"><b>VERSION</b></td><td>" + plugin.version + "</td></tr>"
    print "<tr><td class=\"pluginDetailsIdColumn\"><b>AUTHOR</b></td><td>" + plugin.author + "</td></tr>"
    print "<tr><td class=\"pluginDetailsIdColumn\"><b>LOADING TYPE</b></td><td>" + str(plugin.loading_type) + "</td></tr>"
    print "<tr><td class=\"pluginDetailsIdColumn\"><b>PLATFORMS</b></td><td>" + str(plugin.platforms) + "</td></tr>"
    print "<tr><td class=\"pluginDetailsIdColumn\"><b>CAPABILITIES</b></td><td>" + str(plugin.capabilities) + "</td></tr>"
    print "<tr><td class=\"pluginDetailsIdColumn\"><b>CAPABILITIES ALLOWED</b></td><td>" + str(plugin.capabilities_allowed) + "</td></tr>"
    print "<tr><td class=\"pluginDetailsIdColumn\"><b>DEPENDENCIES</b></td><td>" + str(plugin.dependencies) + "</td></tr>"
    print "</table>"
    print "</div>"
    print "</td>"
    print "</tr>"
print "</tbody>"
print "</table>"
                        ?>
                    </div>
                    <div id="fragment-2">
                        <h2 class="mainTitle">Automation Administration</h2>
                        <p> The automation administration consists in a series of... </p>
                        <h3 class="mainTitle">Automation Types</h3>
                        <?colony
# retrieves the build automation plugin
build_automation_plugin = plugin_manager.get_plugin_by_id("pt.hive.colony.plugins.build.automation")

automation_plugins = build_automation_plugin.get_all_automation_plugins()

for automation_plugin in automation_plugins:
    print automation_plugin.id
                        ?>
                        <h3 class="mainTitle">Automation Items</h3>
                        <?colony
# retrieves the build automation plugin
build_automation_plugin = plugin_manager.get_plugin_by_id("pt.hive.colony.plugins.build.automation")

build_automation_item_plugins = build_automation_plugin.get_all_build_automation_item_plugins()

for build_automation_item_plugin in build_automation_item_plugins:
    print "<p>" + build_automation_item_plugin.id + "</p>"
                        ?>
                    </div>
                    <div id="fragment-3">
                    </div>
                </div>
            </td>
        </tr>
    </table>
    <div class="copyright">
        <span class="mainTitle">Copyright 08 Hive Solutions Lda.</span>
    </div>
</div>

<ul id="pluginContextMenu" class="contextMenu">
    <li><a class="textType" href="#unload">Unload</a></li>
    <li><a class="textType" href="#load">Load</a></li>
    <li><a class="textType" href="#remove">Remove</a></li>
</ul>

</body>
