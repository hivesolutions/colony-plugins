<div id="includes">
    <div class="javascript">resources/templates/js/plugin/plugin_list_contents.js</div>
    <div class="css">resources/templates/css/plugin/plugin_list_contents.css</div>
</div>
<div id="meta-data">
    <div class="area">configuration</div>
    <div class="side-panel">side_panel/configuration</div>
</div>
<div id="contents">
    <div id="option-buttons-area">
        <div class="button-drop-small-gray">
            <div class="label">Clonar</div>
            <div class="arrow"></div>
        </div>
        <div class="button-drop-small-gray">
            <div class="label">Importar</div>
            <div class="arrow"></div>
        </div>
    </div>
    <h1>Configuration</h1>
    <h2>Plugins</h2>
    <table id="plugin-table" class="table" cellspacing="0" cellpadding="0">
        <thead>
            <tr>
                <th><span>Id</span> <span class="order-down"></span></th>
                <th><span>Name</span> <span class="order-down-inactive"></span></th>
                <th><span>Status</span> <span class="order-down-inactive"></span></th>
            </tr>
        </thead>
        <tbody>
            ${foreach item=plugin from=plugins}
            <tr>
                <td>${out_none value=plugin.id xml_escape=True /}</td>
                <td>${out_none value=plugin.name xml_escape=True /}</td>
                <td>active</td>
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
