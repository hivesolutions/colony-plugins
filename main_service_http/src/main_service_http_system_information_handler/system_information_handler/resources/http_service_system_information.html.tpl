<!DOCTYPE html>
<html lang="en">
    <head>
        <title>Colony Framework</title>

        <!--  metadata inclusion -->
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />

        <!-- css inclusion -->
        <link rel="stylesheet" type="text/css" href="/system_information_handler/css/main.css" />

        <!-- favicon inclusion -->
        <link rel="icon" href="/system_information_handler/images/favicon.ico" type="image/x-icon" />

        <!-- javascript inclusion -->
        <script type="text/javascript" src="/system_information_handler/js/main.js"></script>
    </head>
    <body>
        <div id="wiki-header">
            <div class="wiki-header-contents">
                <div class="logo-image">
                    <img src="/system_information_handler/images/colony_logo.png"/>
                </div>
            </div>
        </div>
        <div id="wiki-contents">
            <p></p>
            <div class="highlight">
                <img class="system-information-list-image" src="/system_information_handler/images/logo_datacenter.png"/>
                <div class="system-information-list-text">
                    <b>System Information</b>
                    <p>Colony Framework ${out_none value=plugin_manager_version xml_escape=True /} r${out_none value=plugin_manager_release xml_escape=True /}</p>
                </div>
            </div>
            <p></p>
            <div class="system-information-list">
                ${foreach item=system_information_item from=system_information}
                    <div class="table-view">
                        <span class="title">${out_none value=system_information_item.name xml_escape=True /}</span>
                        ${foreach item=system_information_item_item from=system_information_item.items}
                            <div class="table">
                                ${if item=system_information_item_item.type value="map" operator=eq}
                                    <table class="element-${count value=system_information_item_item.columns /}" cellspacing="0">
                                        <thead>
                                            <tr>
                                                ${foreach item=system_information_item_item_column from=system_information_item_item.columns}
                                                    <th class="column ${out_none value=system_information_item_item_column.type xml_escape=True /}">
                                                        <a href="#">${out_none value=system_information_item_item_column.value xml_escape=True /}</a>
                                                    </th>
                                                ${/foreach}
                                            </tr>
                                        </thead>
                                        <tbody>
                                            ${foreach item=value key=key from=system_information_item_item.values}
                                                <tr>
                                                    <td class="name">${out_none value=key xml_escape=True /}</td>
                                                    ${foreach item=_value from=value}
                                                        <td class="value">${out_none value=_value xml_escape=True /}</td>
                                                    ${/foreach}
                                                </tr>
                                            ${/foreach}
                                        </tbody>
                                        <tfoot></tfoot>
                                    </table>
                                ${elif item=system_information_item_item.type value="simple" operator=eq /}
                                    <table class="element-1" cellspacing="0">
                                        <thead>
                                        </thead>
                                        <tbody>
                                            <tr>
                                                <td class="name">${out_none value=system_information_item_item.value xml_escape=True /}</td>
                                            </tr>
                                        </tbody>
                                        <tfoot></tfoot>
                                    </table>
                                ${/if}
                            </div>
                        ${/foreach}
                    </div>
                ${/foreach}
            </div>
        </div>
        <div id="wiki-footer">
            <div class="wiki-footer-contents">
                <div class="logo-image">
                    <a href="http://getcolony.com">
                        <img src="/system_information_handler/images/powered_by_colony.png"/>
                    </a>
                </div>
                <div class="separator">
                    <img src="/system_information_handler/images/separator.png"/>
                </div>
                <div class="text-contents">Document provided by colony framework in ${out_none value=delta_time xml_escape=True /} seconds
                    <br />Copyright
                    <a href="http://hive.pt">Hive Solutions Lda.</a> distributed under
                    <a href="http://creativecommons.org/licenses/by-sa/3.0"> Creative Commons License</a>
                </div>
            </div>
        </div>
    </body>
</html>
