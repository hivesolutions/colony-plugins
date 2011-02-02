<div id="partial-contents">
    <table id="table">
        <tbody id="table-body">
            ${foreach item=repository_plugin from=repository_plugins}
                <tr>
                    <td>
                        <a href="#plugins/${out_none value=repository_plugin.id xml_escape=True /}">${out_none value=repository_plugin.id xml_escape=True /}</a>
                    </td>
                    <td>
                        <div class="submit button button-green" plugin_id="${out_none value=repository_plugin.id xml_escape=True /}" plugin_version="${out_none value=repository_plugin.version xml_escape=True /}" >Install</div>
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
