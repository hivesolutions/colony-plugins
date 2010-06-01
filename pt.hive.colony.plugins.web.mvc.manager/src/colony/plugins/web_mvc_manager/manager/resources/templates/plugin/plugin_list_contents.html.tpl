<div id="includes">
    <div class="javascript">resources/templates/js/plugin/plugin_list_contents.js</div>
    <div class="css">resources/templates/css/plugin/plugin_list_contents.css</div>
</div>
<div id="meta-data">
    <div class="area">configuration</div>
    <div class="side-panel">side_panel/configuration</div>
</div>
<div id="contents">
    <h1>Configuration</h1>
    <h2>Plugins</h2>
    <table id="plugin-table" class="table" cellspacing="0" cellpadding="0">
        <thead>
            <tr>
                <th><span>Plugin ID</span> <span class="order-down"></span></th>
                <th><span>Status</span> <span class="order-down-inactive"></span></th>
            </tr>
        </thead>
        <tbody>
            ${foreach item=plugin from=plugins}
            <tr>
                <td><a href="#plugins/${out_none value=plugin.id xml_escape=True /}">${out_none value=plugin.id xml_escape=True /}</a></td>
                <td><div class="switch-button ${if item=plugin.loaded value=True operator=eq}on${/if}${if item=plugin.loaded value=False operator=eq}off${/if}" plugin="${out_none value=plugin.id xml_escape=True /}"></div></td>
            </tr>
            ${/foreach}
        </tbody>
        <tfoot>
        </tfoot>
    </table>
    <div class="pagging-area">
        <a id="previous-button" class="control-button">Previous</a>
        <span id="page-indicator">
        </span>
        <a id="next-button" class="control-button">Next</a>
    </div>
</div>
