<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
<html>
    <head>
        <title>Hive Solutions</title>
    </head>
    <body>
        <center>
            <br />
            <table width="600" cellpadding="0" cellspacing="0">
                <tr>
                    <td colspan="3">
                        <img src="cid:email_header.gif" height="44" width="600" alt="Hive Solutions" />
                    </td>
                </tr>
                <tr height="80">
                    <td colspan="3"></td>
                </tr>
                <tr>
                    <td width="100"></td>
                    <td width="400" align="left" style="line-height:1.8em;margin-bottom:20px;margin-top:0;">
                        <h1>
                            <font face="Rockwell, Arial" size="3" color="#214c8f">${out_none value=plugin_name xml_escape=True /} - </font>
                            ${if item=success value=True operator=eq}
                                <font face="Rockwell, Arial" size="3" color="#4d9341">${out_none value=success_capitals xml_escape=True /}</font>
                            ${/if}
                            ${if item=success value=False operator=eq}
                                <font face="Rockwell, Arial" size="3" color="#dc1c28">${out_none value=success_capitals xml_escape=True /}</font>
                            ${/if}
                        </h1>
                        <p>
                            <font face="Arial" size="2" color="#333333">
                                Code has been updated by João Magalhães (joamag@hive.pt), Tiago Silva (tsilva@hive.pt).
                                3 tests ran in total.
                            </font>
                        </p>
                        <p>
                            <img src="cid:line.gif" width="400" height="1" alt="separator" />
                        </p>
                        <font face="Rockwell, Arial" size="3" color="#808080"><strong>Code Changes</strong></font>
                        <br />
                        <p>
                            <font face="Arial" size="2" color="#333333">
                                <font face="Rockwell, Arial" size="3" color="#214c8f"><b><a href="#">r16026</a> - João Magalhães (joamag@hive.pt)</b></font><br />
                                <a href="#">#ticket-123</a> First log message.
                            </font>
                        </p>
                        <p>
                            <font face="Arial" size="2" color="#333333">
                                <font face="Rockwell, Arial" size="3" color="#214c8f"><b><a href="#">r16027</a> - Tiago Silva (tsilva@hive.pt)</b></font><br />
                                <a href="#">#bug-245</a> Second log message.
                            </font>
                        </p>
                        <img src="cid:line.gif" width="400" height="1" alt="separator" />
                        <p align="right">
                            <font face="Arial" size="2" color="#333333"><a href="#">code changes details ></a></font>
                        </p>
                        <font face="Rockwell, Arial" size="3" color="#808080"><strong>Issues</strong></font>
                        <br />
                        <p>
                            <font face="Arial" size="2" color="#333333">
                                <font face="Rockwell, Arial" size="3" color="#214c8f"><b><a href="#">Ticket 123</a> - Build a meta prototype</b></font><br />
                                The meta prototypwe should contain everything specified in the specification #4134.
                            </font>
                        </p>
                        <p>
                            <font face="Arial" size="2" color="#333333">
                                <font face="Rockwell, Arial" size="3" color="#214c8f"><b><a href="#">Bug 245</a> - Fix text alignment</b></font><br />
                                The text alignment is strange it shoulb be fixed byt the operators that have created it. If not built on time
                                this bug can start to be a real big problem.
                            </font>
                        </p>
                        <img src="cid:line.gif" width="400" height="1" alt="separator" />
                        <p align="right"><font face="Arial" size="2" color="#333333"><a href="#">issues details ></a></font></p>
                        <br />
                        <p align="center">
                            <font face="Arial" size="2" color="#333333">
                                <a href="#">View Online</a> -
                                <a href="#">Add Comment</a> -
                                <a href="#">View Artifacts</a> -
                                <a href="cid:build_automation.log">Download Log</a>
                            </font>
                        </p>
                        <br />
                        <img src="cid:line.gif" width="400" height="1" alt="separator" />
                        <br />
                        <table id="footer">
                            <tr>
                                <td width="70" align="left"><img src="cid:character_l.gif" height="100" width="50" /></td>
                                <td>
                                    <font face="Rockwell, Arial" size="3" color="#808080"><strong>Colony Continuous Integration</strong></font><br />
                                    <font face="Rockwell, Arial" size="2" color="#808080">Automation the easy way</font><br />
                                    <font face="Rockwell, Arial" size="2"><a href="#">integration@getcolony.com</a></font><br />
                                </td>
                            </tr>
                        </table>
                    </td>
                    <td width="100"></td>
                </tr>
                <tr height="86">
                    <td colspan="3" valign="bottom" align="left" id="copyright">
                        <font face="verdana" size="1" color="#dddddd">© Copyright 2010 Hive Solutions Lda - All rights reseved</font>
                    </td>
                </tr>
            </table>
            <br />
            <p id="policy">
                <font face="verdana" size="1" color="#dddddd">
                    This email was sent to you with your consent via integration@getcolony.com .<br />
                    To ensure that you continue receiving our emails,<br />
                    please add us to your address book or safe list.<br />
                    View this email on the web here. You can also forward to a friend.<br />
                </font>
            </p>
        </center>
    </body>
</html>
