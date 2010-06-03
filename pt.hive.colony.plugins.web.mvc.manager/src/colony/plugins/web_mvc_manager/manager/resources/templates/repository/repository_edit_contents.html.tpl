<div id="includes">
    <div class="javascript">resources/templates/js/repository/repository_edit_contents.js</div>
    <div class="css">resources/templates/css/repository/repository_edit_contents.css</div>
</div>
<div id="meta-data">
    <div class="area">update</div>
    <div class="side-panel">side_panel/update</div>
</div>
<div id="contents">
    <h1>Update</h1>
    <h2>Repository - ${out_none value=repository.name xml_escape=True /}</h2>
    <div class="message">${out_none value=result_message xml_escape=True /}</div>
    <form id="edit-repository" method="post">
        <div class="form-field-area">
            <h4>Plugin Data</h4>
            <hr/>
            <div class="column-first">
                <div class="form-field">
                    <label class="mandatory">Name:</label>
                    <div><input class="text" name="repository[name]" type="text" tabindex="1" value="${out_none value=repository.name xml_escape=True /}" error="${out_none value=repository.validation_errors_map.name /}" /></div>
                </div>
                <div class="form-field">
                    <label class="mandatory">Description:</label>
                    <div><input class="text" name="repository[description]" type="text" tabindex="3" value="${out_none value=repository.description xml_escape=True /}" error="${out_none value=repository.validation_errors_map.description /}" /></div>
                </div>
            </div>
            <div class="column-second">
                <div class="form-field">
                    <label class="mandatory">Layout:</label>
                    <div><input class="text" name="repository[layout]" type="text" tabindex="2" value="${out_none value=repository.layout xml_escape=True /}" error="${out_none value=repository.validation_errors_map.layout /}" /></div>
                </div>
            </div>
            <div class="clear"></div>
        </div>
        <div class="form-field-area">
            <h4>Plugins</h4>
            <hr/>
            <div id="repository-plugins-table" class="search-table" provider_url="repositories/${out_none value=repository_index xml_escape=True /}/plugins_partial">
                <table class="table" cellspacing="0" cellpadding="0">
                    <thead>
                        <tr>
                            <th><span>Plugin ID</span><span class="order-down-inactive"></span></th>
                            <th width="75"><span>Install</span><span class="order-down-inactive"></span></th>
                        </tr>
                    </thead>
                    <tbody>
                    </tbody>
                    <tfoot>
                    </tfoot>
                </table>
            </div>
            <div class="clear"></div>
        </div>
        <div class="form-field-area">
            <h4>Packages</h4>
            <hr/>
            <div class="column-first">
            </div>
            <div class="column-second">
            </div>
            <div class="clear"></div>
        </div>
        <div class="form-button-area">
            <div class="cancel button button-blue" tabindex="4">Cancelar</div>
            <div class="submit button button-green" tabindex="5">Actualizar</div>
        </div>
    </form>
</div>
