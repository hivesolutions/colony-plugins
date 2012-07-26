<div class="quote">${out_none value=plugin.name xml_escape=True /}</div>
<div class="separator-horizontal"></div>
<table>
    <tbody>
        <tr>
            <td class="right label" width="50%">status</td>
            ${if item=plugin.loaded value=True operator=eq}
                <td class="left value valid" width="50%">active</td>
            ${else /}
                <td class="left value invalid" width="50%">inactive</td>
            ${/if}
        </tr>
        <tr>
            <td class="right label" width="50%">id</td>
            <td class="left value" width="50%">${out_none value=plugin.id xml_escape=True /}</td>
        </tr>
        <tr>
            <td class="right label" width="50%">version</td>
            <td class="left value" width="50%">${out_none value=plugin.version xml_escape=True /}</td>
        </tr>
        <tr>
            <td class="right label" width="50%">author</td>
            <td class="left value" width="50%">${out_none value=plugin.get_author_name xml_escape=True /}</td>
        </tr>
        ${if item=plugin.loaded value=True operator=eq}
            <tr>
                <td class="right label" width="50%">uptime</td>
                <td class="left value" width="50%">${out_none value=plugin.get_uptime xml_escape=True /}</td>
            </tr>
        ${/if}
    </tbody>
</table>
