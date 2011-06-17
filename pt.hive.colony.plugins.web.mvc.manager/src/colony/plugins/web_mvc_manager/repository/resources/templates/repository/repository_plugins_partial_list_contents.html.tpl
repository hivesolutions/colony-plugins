<div id="partial-contents">
    <table id="table">
        <tbody id="table-body">
            ${foreach item=repository_plugin from=repository_plugins}
                <tr>
                    <td>
                        <a href="#plugins/${out_none value=repository_plugin.id xml_escape=True /}">${out_none value=repository_plugin.id xml_escape=True /}</a>
                    </td>
                    <td>
                        ${if item=repository_plugin.status value="not_installed" operator=eq}
                            <div class="submit button button-green"
                                 data-plugin_id="${out_none value=repository_plugin.id xml_escape=True /}"
                                 data-plugin_version="${out_none value=repository_plugin.version xml_escape=True /}"
                                 data-plugin_status="${out_none value=repository_plugin.status xml_escape=True /}">
                                 Install
                            </div>
                        ${elif item=repository_plugin.status value="newer_version" operator=eq /}
                            <div class="submit button button-green"
                                 data-plugin_id="${out_none value=repository_plugin.id xml_escape=True /}"
                                 data-plugin_version="${out_none value=repository_plugin.version xml_escape=True /}"
                                 data-plugin_status="${out_none value=repository_plugin.status xml_escape=True /}">
                                 Upgrade
                            </div>
                        ${elif item=repository_plugin.status value="older_version" operator=eq /}
                            <div class="submit button button-gray"
                                 data-plugin_id="${out_none value=repository_plugin.id xml_escape=True /}"
                                 data-plugin_version="${out_none value=repository_plugin.version xml_escape=True /}"
                                 data-plugin_status="${out_none value=repository_plugin.status xml_escape=True /}">
                                 Older Version
                               </div>
                        ${elif item=repository_plugin.status value="same_version" operator=eq /}
                            <div class="submit button button-gray"
                                 data-plugin_id="${out_none value=repository_plugin.id xml_escape=True /}"
                                 data-plugin_version="${out_none value=repository_plugin.version xml_escape=True /}"
                                 data-plugin_status="${out_none value=repository_plugin.status xml_escape=True /}">
                                Installed
                            </div>
                        ${elif item=repository_plugin.status value="different_digest" operator=eq /}
                            <div class="submit button button-blue"
                                 data-plugin_id="${out_none value=repository_plugin.id xml_escape=True /}"
                                 data-plugin_version="${out_none value=repository_plugin.version xml_escape=True /}"
                                 data-plugin_status="${out_none value=repository_plugin.status xml_escape=True /}">
                                Upgrade
                            </div>
                        ${/if}
                    </td>
                </tr>
            ${/foreach}
        </tbody>
    </table>
    <div id="meta-data">
        <div id="start-record">${out value=start_record xml_escape=True /}</div>
        <div id="number-records">${out value=number_records xml_escape=True /}</div>
        <div id="total-number-records">${out value=total_number_records xml_escape=True /}</div>
    </div>
</div>
