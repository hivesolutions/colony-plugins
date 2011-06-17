<div id="includes">
</div>
<div id="meta-data">
    <div class="area">configuration</div>
    <div class="side-panel">side_panel/configuration</div>
</div>
<div id="contents">
    <h1>Configuration</h1>
    <h2>Capability - ${out_none value=capability xml_escape=True /}</h2>
    <div class="message">${out_none value=result_message xml_escape=True /}</div>
    <form data-action_target="plugins/edit/${out_none value=plugin.id xml_escape=True /}" id="edit-plugin" method="post">
        <div class="form-field-area">
            <h4>Plugin Data</h4>
            <hr/>
            <div class="column-first">
                <div class="form-field">
                    <label class="mandatory">Name:</label>
                    <div><input class="text" name="capability[name]" type="text" tabindex="1" value="${out_none value=capability xml_escape=True /}" error="${out_none value=capability.validation_errors_map.name /}" /></div>
                </div>
            </div>
            <div class="column-second">
            </div>
            <div class="clear"></div>
        </div>
        <div class="form-field-area">
            <h4>Plugins</h4>
            <hr/>
            <div class="column-first">
                <div class="form-field">
                    <label>Plugins providing capability: </label>
                    ${foreach item=providing_plugin from=plugins_capability.providing}
                        <label>
                            <a href="#plugins/${out_none value=providing_plugin.id xml_escape=True /}">${out_none value=providing_plugin.id xml_escape=True /}</a>
                        </label>
                    ${/foreach}
                </div>
            </div>
            <div class="column-second">
                <div class="form-field">
                    <label>Plugins allowing capability: </label>
                    ${foreach item=allowing_plugin from=plugins_capability.allowing}
                        <label>
                            <a href="#plugins/${out_none value=allowing_plugin.id xml_escape=True /}">${out_none value=allowing_plugin.id xml_escape=True /}</a>
                        </label>
                    ${/foreach}
                </div>
            </div>
            <div class="clear"></div>
        </div>
        <div class="form-field-area">
            <h4>Sub-Capabilities</h4>
            <hr/>
            <div class="column-first">
                ${foreach item=sub_capability from=sub_capabilities}
                    <div class="form-field">
                        <label>
                            <a href="#capabilities/${out_none value=sub_capability xml_escape=True /}">${out_none value=sub_capability xml_escape=True /}</a>
                        </label>
                    </div>
                ${/foreach}
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
