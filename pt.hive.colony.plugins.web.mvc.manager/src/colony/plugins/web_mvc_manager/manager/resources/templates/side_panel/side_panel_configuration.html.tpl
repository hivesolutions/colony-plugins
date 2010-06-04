<div id="icon-bar" class="brown">
    <div id="content-icon">
        <img src="resources/images/icon/icon-omni.png" height="32" width="32" alt="Bill"/>
    </div>
</div>
<div id="left-column">
    <h1 id="assistants">Assistants</h1>
    <ul id="assistants">
        <li target_request="plugins/new"><span>Install Plugin</span></li>
    </ul>
    <h1 id="lists">Lists</h1>
    <ul id="lists">
        <li target_request="plugins"><span>Plugins</span></li>
        <li target_request="capabilities"><span>Capabilities</span></li>
    </ul>
    <h1 id="status">Status</h1>
    <div class="widget-table">
        <table>
            <tr>
                <td class="label light-blue">Plugins</td>
                <td class="value light-blue">${out_none value=plugin_count xml_escape=True /}</td>
            </tr>
            <tr>
                <td class="label light-blue">Loaded Plugins</td>
                <td class="value light-blue">${out_none value=plugin_loaded_count xml_escape=True /}</td>
            </tr>
            <tr class="section-end">
                <td class="label light-blue">Capabilities</td>
                <td class="value light-blue">${out_none value=capabilities_count xml_escape=True /}</td>
            </tr>
            <tr>
                <td class="label light-blue">Memory</td>
                <td class="value ${if item=memory_usage value=100 operator=lt}green${/if}${if item=memory_usage value=100 operator=gte}red${/if}">${out_none value=memory_usage xml_escape=True /}M</td>
            </tr>
            <tr class="section-end">
                <td class="label light-blue">CPU</td>
                <td class="value ${if item=cpu_usage value=50 operator=lt}green${/if}${if item=cpu_usage value=50 operator=gte}red${/if}">${out_none value=cpu_usage xml_escape=True /}%</td>
            </tr>
            <tr>
                <td class="label dark-blue bold">Uptime</td>
                <td class="value dark-blue bold">${out_none value=uptime xml_escape=True /}</td>
            </tr>
        </table>
    </div>
    ${foreach item=panel_item from=panel_items}
        ${out_none value=panel_item /}
    ${/foreach}
</div>
