<div id="includes">
    <div class="javascript">resources/templates/js/capability/capability_list_contents.js</div>
    <div class="css">resources/templates/css/capability/capability_list_contents.css</div>
</div>
<div id="meta-data">
    <div class="area">configuration</div>
    <div class="side-panel">side_panel/configuration</div>
</div>
<div id="contents">
    <h1>Configuration</h1>
    <h2>Capabilities</h2>
    <table id="capability-table" class="table" cellspacing="0" cellpadding="0">
        <thead>
            <tr>
                <th><span>Capability Name</span><span class="order-down-inactive"></span></th>
                <th width="100"><span>Plugin Count</span><span class="order-down-inactive"></span></th>
            </tr>
        </thead>
        <tbody>
            ${foreach item=capability from=capabilities}
            <tr>
                <td><a href="#capabilities/${out_none value=capability xml_escape=True /}">${out_none value=capability xml_escape=True /}</a></td>
                <td>0</td>
            </tr>
            ${/foreach}
        </tbody>
        <tfoot>
        </tfoot>
    </table>
</div>
