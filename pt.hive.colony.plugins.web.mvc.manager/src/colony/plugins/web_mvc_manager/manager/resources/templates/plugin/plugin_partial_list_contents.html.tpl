<div id="partial-contents">
    <table id="table">
        <tbody id="table-body">
        ${foreach item=plugin from=plugins}
        <tr>
            <td><a href="#plugins/${out_none value=plugin.id xml_escape=True /}">${out_none value=plugin.id xml_escape=True /}</a></td>
            <td><div class="switch-button ${if item=plugin.loaded value=True operator=eq}on${/if}${if item=plugin.loaded value=False operator=eq}off${/if}" plugin="${out_none value=plugin.id xml_escape=True /}"></div></td>
        </tr>
        ${/foreach}
        </tbody>
    </table>
    <div id="meta-data">
        <div id="start-record">${out value=companies_page.start_record xml_escape=True /}</div>
        <div id="end-record">${out value=companies_page.end_record xml_escape=True /}</div>
        <div id="number-records">${out value=companies_page.number_records xml_escape=True /}</div>
        <div id="previous-start-record">${out value=companies_page.previous_start_record xml_escape=True /}</div>
        <div id="next-start-record">${out value=companies_page.next_start_record xml_escape=True /}</div>
        <div id="total-number-records">${out value=companies_page.total_number_records xml_escape=True /}</div>
    </div>
</div>
