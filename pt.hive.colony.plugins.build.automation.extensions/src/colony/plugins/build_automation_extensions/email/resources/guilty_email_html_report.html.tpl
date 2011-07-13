<!--
 Hive Colony Framework
 Copyright (C) 2008 Hive Solutions Lda.

 This file is part of Hive Colony Framework.

 Hive Colony Framework is free software: you can redistribute it and/or modify
 it under the terms of the GNU General Public License as published by
 the Free Software Foundation, either version 3 of the License, or
 (at your option) any later version.

 Hive Colony Framework is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
 GNU General Public License for more details.

 You should have received a copy of the GNU General Public License
 along with Hive Colony Framework. If not, see <http://www.gnu.org/licenses/>.
-->

<!--
 __author__    = João Magalhães <joamag@hive.pt>
 __version__   = 1.0.0
 __revision__  = $LastChangedRevision: 9251 $
 __date__      = $LastChangedDate: 2010-07-09 23:19:45 +0100 (sex, 09 Jul 2010) $
 __copyright__ = Copyright (c) 2008 Hive Solutions Lda.
 __license__   = GNU General Public License (GPL), Version 3
-->

<!DOCTYPE html>
<html lang="en">
    <head>
        <title>Hive Solutions</title>
    </head>
    <body>
        <center>
            <br />
            <table width="700" cellpadding="0" cellspacing="0">
                <tr>
                    <td colspan="3">
                        <img src="cid:email_header.gif" height="44" width="700" alt="Hive Solutions" />
                    </td>
                </tr>
                <tr>
                    <td colspan="3" align="right" cellpadding="0" cellspacing="0" height="70" background="cid:build_line.gif">
                        <table width="160" cellpadding="0">
                            <tr height="20">
                                <td align="center">
                                    <font face="Rockwell, Arial" size="5" color="#214c8f">build</font>
                                    <font face="Rockwell, Arial" size="5" color="#214c8f"><b>${out_none value=build_automation.build xml_escape=True /}</b></font>
                                </td>
                            </tr>
                            ${if item=build_automation.success value=True operator=eq}
                                <tr height="10" background="cid:build_line_green.gif">
                                    <td></td>
                                </tr>
                                <tr height="0" background="cid:build_line_red.gif">
                                    <td></td>
                                </tr>
                            ${else /}
                                <tr height="10" background="cid:build_line_red.gif">
                                    <td></td>
                                </tr>
                                <tr height="0" background="cid:build_line_green.gif">
                                    <td></td>
                                </tr>
                            ${/if}
                            <tr height="10">
                                <td></td>
                            </tr>
                        </table>
                    </td>
                </tr>
                <tr>
                    <td width="100"></td>
                    <td width="500" align="left" style="line-height:1.8em;margin-bottom:20px;margin-top:0;">
                        <h1 style="margin-bottom:1.2em;">
                            <font face="Rockwell, Arial" size="3" color="#214c8f">${out_none value=build_automation.plugin_name xml_escape=True /}</font>
                            ${if item=build_automation.success value=True operator=eq}
                                <font face="Rockwell, Arial" size="3" color="#214c8f">had</font> <font face="Rockwell, Arial" size="3" color="#4d9341">${out_none value=build_automation.success_capitals xml_escape=True /}</font>
                            ${else /}
                                <font face="Rockwell, Arial" size="3" color="#214c8f">has</font> <font face="Rockwell, Arial" size="3" color="#dc1c28">${out_none value=build_automation.success_capitals xml_escape=True /}</font>
                            ${/if}
                            <br />
                            <font face="Rockwell, Arial" size="2" color="#214c8f"><b>You are a <font face="Rockwell, Arial" size="2" color="#dc1c28">SUSPECT</font>, make sure you're innocent</b></font>
                        </h1>
                        <p>
                            <font face="Arial" size="2" color="#333333">
                                Code has been updated to <font face="Rockwell, Arial" size="2" color="#214c8f"><b>r${out_none value=build_automation.build xml_escape=True /}</b></font>.<br />
                                The updating of the code involved:
                                ${foreach item=changer from=build_automation.changers_list}
                                    <font face="Rockwell, Arial" size="2" color="#214c8f"><b>${out_none value=changer.name xml_escape=True /} (${out_none value=changer.username xml_escape=True /})</b></font>,
                                ${/foreach}.
                                <br />
                                The total time for the build automation run was <font face="Rockwell, Arial" size="2" color="#214c8f"><b>${out_none value=build_automation.total_time_formated xml_escape=True /}</b></font>.
                            </font>
                        </p>
                        <p>
                            <img src="cid:line.gif" width="100%" height="1" alt="separator" />
                        </p>
                        <font face="Rockwell, Arial" size="3" color="#808080"><strong>Code Changes</strong></font>
                        <br />
                        ${foreach item=change from=build_automation.changelog_list}
                            <p>
                                <font face="Arial" size="2" color="#333333">
                                    <font face="Rockwell, Arial" size="3" color="#214c8f"><b><a href="${out_none value=build_automation.changelog_url xml_escape=True /}/${out_none value=change.number xml_escape=True /}">${out_none value=change.number xml_escape=True /}</a> - ${out_none value=change.user.name xml_escape=True /} (${out_none value=change.user.username xml_escape=True /})</b></font><br />
                                    ${out_none value=change.message xml_escape=True /}
                                </font>
                            </p>
                        ${/foreach}
                        <img src="cid:line.gif" width="100%" height="1" alt="separator" />
                        <p align="right">
                            <font face="Arial" size="2" color="#333333"><a href="#">code changes details ></a></font>
                        </p>
                        <font face="Rockwell, Arial" size="3" color="#808080"><strong>Issues</strong></font>
                        <br />
                        ${foreach item=issue from=build_automation.issues_list}
                            <p>
                                <font face="Arial" size="2" color="#333333">
                                    <font face="Rockwell, Arial" size="3" color="#214c8f"><b><a href="#">${out_none value=issue.number xml_escape=True /}</a> - ${out_none value=issue.title xml_escape=True /}</b></font><br />
                                    ${out_none value=issue.description xml_escape=True /}
                                </font>
                            </p>
                        ${/foreach}
                        <img src="cid:line.gif" width="100%" height="1" alt="separator" />
                        <p align="right"><font face="Arial" size="2" color="#333333"><a href="#">issues details ></a></font></p>
                        <br />
                        <p align="center">
                            <font face="Arial" size="2" color="#333333">
                                <a href="#">View Report</a> -
                                <a href="#">Post Comment</a> -
                                <a href="${out_none value=build_automation.repository_url xml_escape=True /}">View Artifacts</a> -
                                <a href="${out_none value=build_automation.repository_url xml_escape=True /}/${out_none value=build_automation.log_file_path xml_escape=True /}">Download Log</a>
                            </font>
                        </p>
                        <p>
                            <img src="cid:line.gif" width="100%" height="1" alt="separator" />
                        </p>
                        <table id="footer">
                            <tr>
                                <td width="70" align="left"><img src="cid:angry_stickman.gif" height="100" width="50" /></td>
                                <td>
                                    <font face="Rockwell, Arial" size="3" color="#808080"><strong>Colony Build Automation</strong></font><br />
                                    <font face="Rockwell, Arial" size="2" color="#808080">Automation the easy way</font><br />
                                    <font face="Rockwell, Arial" size="2">automation@getcolony.com</font><br />
                                </td>
                            </tr>
                        </table>
                    </td>
                    <td width="100"></td>
                </tr>
                <tr height="86">
                    <td colspan="3" valign="bottom" align="left" id="copyright">
                        <font face="verdana" size="1" color="#dddddd">© Copyright ${year /} Hive Solutions Lda. - All rights reseved</font>
                    </td>
                </tr>
            </table>
            <br />
            <p id="policy">
                <font face="verdana" size="1" color="#dddddd">
                    This email was sent to you with your consent via automation@getcolony.com.<br />
                    To ensure that you continue receiving our emails,<br />
                    please add us to your address book or safe list.<br />
                    View this email on the web here. You can also forward to a friend.<br />
                </font>
            </p>
        </center>
    </body>
</html>
