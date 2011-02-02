<div id="partial-contents">
    <table id="table">
        <tbody id="table-body">
            ${foreach item=plugin from=plugins}
                <tr>
                    <td>
                        <a href="#plugins/${out_none value=plugin.id xml_escape=True /}">${out_none value=plugin.id xml_escape=True /}</a>
                    </td>
                    <td>
                        <div class="switch-button ${if item=plugin.loaded value=True operator=eq}on${/if}${if item=plugin.loaded value=False operator=eq}off${/if}" plugin="${out_none value=plugin.id xml_escape=True /}"></div>
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
