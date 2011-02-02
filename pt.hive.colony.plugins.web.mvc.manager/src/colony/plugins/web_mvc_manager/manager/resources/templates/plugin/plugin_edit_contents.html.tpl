<div id="includes">
</div>
<div id="meta-data">
    <div class="area">configuration</div>
    <div class="side-panel">side_panel/configuration</div>
</div>
<div id="contents">
    <h1>Configuration</h1>
    <h2>Plugin - ${out_none value=plugin.id xml_escape=True /}</h2>
    <div class="message">${out_none value=result_message xml_escape=True /}</div>
    <form data-action_target="plugins/edit/${out_none value=plugin.id xml_escape=True /}" id="edit-plugin" method="post">
        <div class="form-field-area">
            <h4>Plugin Data</h4>
            <hr/>
            <div class="column-first">
                <div class="form-field">
                    <label class="mandatory">Name:</label>
                    <div><input class="text" name="plugin[name]" type="text" tabindex="1" value="${out_none value=plugin.name xml_escape=True /}" error="${out_none value=plugin.validation_errors_map.name /}" /></div>
                </div>
                <div class="form-field">
                    <label class="mandatory">Short Name:</label>
                    <div><input class="text" name="plugin[short_name]" type="text" tabindex="3" value="${out_none value=plugin.short_name xml_escape=True /}" error="${out_none value=plugin.validation_errors_map.short_name /}" /></div>
                </div>
                <div class="form-field">
                    <label>Description:</label>
                    <div><textarea class="text" name="plugin[description]" tabindex="5">${out_none value=plugin.description xml_escape=True /}</textarea></div>
                </div>
            </div>
            <div class="column-second">
                <div class="form-field">
                    <label class="mandatory">Version:</label>
                    <div><input class="text" name="plugin[version]" type="text" tabindex="3" value="${out_none value=plugin.version xml_escape=True /}" error="${out_none value=plugin.validation_errors_map.version /}" /></div>
                </div>
                <div class="form-field">
                    <label class="mandatory">Author: </label>
                    <div><input class="text" name="plugin[author]" type="text" tabindex="4" value="${out_none value=plugin.author xml_escape=True /}" error="${out_none value=plugin.validation_errors_map.author /}" /></div>
                </div>
            </div>
            <div class="clear"></div>
        </div>
        <div class="form-field-area">
            <h4>Capabilities</h4>
            <hr/>
            <div class="column-first">
                ${foreach item=capability from=plugin.capabilities}
                <div class="form-field">
                    <label><a href="#capabilities/${out_none value=capability xml_escape=True /}">${out_none value=capability xml_escape=True /}</a></label>
                </div>
                ${/foreach}
            </div>
            <div class="column-second">
            </div>
            <div class="clear"></div>
        </div>
        <div class="form-field-area">
            <h4>Dependencies</h4>
            <hr/>
            <div class="column-first">
                ${foreach item=dependency from=plugin.dependencies}
                <div class="form-field">
                    <label><a href="#plugins/${out_none value=dependency.plugin_id xml_escape=True /}">${out_none value=dependency.plugin_id xml_escape=True /} [${out_none value=dependency.plugin_version xml_escape=True /}]</a></label>
                </div>
                ${/foreach}
            </div>
            <div class="column-second">
                ${foreach item=dependency from=plugin.dependencies}
                <div class="form-field">
                    <label>${out_none value=dependency.package_name xml_escape=True /} [${out_none value=dependency.package_version xml_escape=True /}]</label>
                </div>
                ${/foreach}
            </div>
            <div class="clear"></div>
        </div>
        <div class="form-button-area">
            <div class="cancel button button-blue" tabindex="13">Cancelar</div>
            <div class="submit button button-green" tabindex="12">Actualizar</div>
        </div>
    </form>
</div>
