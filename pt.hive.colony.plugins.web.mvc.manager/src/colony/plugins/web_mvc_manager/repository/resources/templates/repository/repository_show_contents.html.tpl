<div id="includes">
    <div class="javascript">repositories/resources/templates/js/repository/repository_show_contents.js</div>
    <div class="css">repositories/resources/templates/css/repository/repository_show_contents.css</div>
</div>
<div id="meta-data">
    <div class="area">update</div>
    <div class="side-panel">side_panel/update</div>
</div>
<div id="contents">
    <h1>Update</h1>
    <h2>Repository - ${out_none value=repository.name xml_escape=True /}</h2>
    <div id="repository-groups-table">
        <table class="table" cellspacing="0" cellpadding="0">
            <thead>
                <tr>
                    <th><span>Group Name</span><span class="order-down-inactive"></span></th>
                    <th width="75"><span>Count</span><span class="order-down-inactive"></span></th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td><a href="#repositories/${out_none value=repository_index xml_escape=True /}/bundles">Bundles</a></td>
                    <td>N/A</td>
                </tr>
                <tr>
                    <td><a href="#repositories/${out_none value=repository_index xml_escape=True /}/plugins">Plugins</a></td>
                    <td>N/A</td>
                </tr>
                <tr>
                    <td><a href="#repositories/${out_none value=repository_index xml_escape=True /}/containers">Containers</a></td>
                    <td>N/A</td>
                </tr>
            </tbody>
            <tfoot></tfoot>
        </table>
    </div>
</div>
