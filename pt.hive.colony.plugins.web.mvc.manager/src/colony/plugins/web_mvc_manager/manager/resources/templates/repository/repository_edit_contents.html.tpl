<div id="includes">
</div>
<div id="meta-data">
    <div class="area">update</div>
    <div class="side-panel">side_panel/update</div>
</div>
<div id="contents">
    <h1>Update</h1>
    <h2>Capability - ${out_none value=capability xml_escape=True /}</h2>
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
                    <div><input class="text" name="repository[layout]" type="text" tabindex="3" value="${out_none value=repository.layout xml_escape=True /}" error="${out_none value=repository.validation_errors_map.layout /}" /></div>
                </div>
            </div>
            <div class="clear"></div>
        </div>
        <div class="form-field-area">
            <h4>Plugins</h4>
            <hr/>
            <div class="search-field" id="search-list-field">
                <div>
                    <input class="text" name="search_query" id="search-query" type="text" value="${out_none value=search_query /}"/>
                    <div class="search-button"></div>
                </div>
             </div>
            <table id="plugin-table" class="table" cellspacing="0" cellpadding="0">
                <thead>
                    <tr>
                        <th><span>Plugin ID</span><span class="order-down"></span></th>
                        <th width="60"><span>Status</span><span class="order-down-inactive"></span></th>
                    </tr>
                </thead>
                <tbody>
                    ${foreach item=plugin from=repository.plugins}
                     <tr>
                        <td><a href="#plugins/${out_none value=plugin.id xml_escape=True /}">${out_none value=plugin.id xml_escape=True /}</a></td>
                        <td><div class="switch-button ${if item=plugin.loaded value=True operator=eq}on${/if}${if item=plugin.loaded value=False operator=eq}off${/if}" plugin="${out_none value=plugin.id xml_escape=True /}"></div></td>
                    </tr>
                    ${/foreach}
                </tbody>
                <tfoot>
                </tfoot>
            </table>
            <div class="clear"></div>
        </div>
        <div class="form-field-area">
            <h4>Sub-Capabilities</h4>
            <hr/>
            <div class="column-first">
            </div>
            <div class="column-second">
            </div>
            <div class="clear"></div>
        </div>
        <div class="form-button-area">
            <div class="cancel button button-blue" tabindex="13">Cancelar</div>
            <div class="submit button button-green" tabindex="12">Actualizar</div>
        </div>
    </form>
</div>
