<div id="includes">
</div>
<div id="meta-data">
    <div class="area">configuration</div>
    <div class="side-panel">side_panel/configuration</div>
</div>
<div id="contents">
    <h1>Configuration</h1>
    <h2>Install Plugin</h2>
    <div class="message">${out_none value=result_message xml_escape=True /}</div>
    <form action_target="plugins" class="new-plugin" method="post">
        <div class="form-field-area">
            <h4>Dados da Empresa</h4>
            <hr/>
            <input type="file" name="files" multiple="true" />
            <div class="clear"></div>
            <input type="file" name="tobias" multiple="true" />
            <div class="clear"></div>
            <div class="column-first">
                <div class="form-field">
                    <label class="mandatory">Nome:</label>
                    <div>
                        <input class="text" name="plugin[name]" type="text" tabindex="1" value="${out_none value=plugin.name /}" error="${out_none value=plugin.validation_errors_map.name /}" />
                    </div>
                </div>
                <div class="form-field">
                    <label class="mandatory">Contribuinte:</label>
                    <div>
                        <input class="text" name="plugin[fiscal_id]" type="text" tabindex="3" value="${out_none value=plugin.fiscal_id /}" error="${out_none value=plugin.validation_errors_map.fiscal_id /}" />
                    </div>
                </div>
                <div class="form-field">
                    <label>Observações:</label>
                    <div>
                        <textarea class="text" name="plugin[observations]" tabindex="5">${out_none value=plugin.observations /}</textarea>
                    </div>
                </div>
            </div>
            <div class="column-second">
                <div class="form-field">
                    <label class="mandatory">Morada:</label>
                    <div>
                        <input class="text" name="plugin[primary_contact_information][address]" type="text" tabindex="2" value="${out_none value=plugin.primary_contact_information.address /}" error="${out_none value=plugin.primary_contact_information.validation_errors_map.address /}" />
                    </div>
                </div>
                <div class="form-field">
                    <label class="mandatory">Cód. Postal:</label>
                    <div>
                        <input class="text" name="plugin[primary_contact_information][postal_code]" type="text" tabindex="4" value="${out_none value=plugin.primary_contact_information.postal_code /}" error="${out_none value=plugin.primary_contact_information.validation_errors_map.postal_code /}" />
                    </div>
                </div>
                <div class="form-field">
                    <label class="mandatory">País:</label>
                    <div>
                        <select name="plugin[primary_contact_information][country]" tabindex="6">
                            <option value="Portugal" selected="selected">Portugal</option>
                        </select>
                    </div>
                </div>
            </div>
            <div class="clear"></div>
        </div>
        <div class="form-field-area">
            <h4>Contactos</h4>
            <hr/>
            <div class="column-first">
                <div class="form-field">
                    <label>Nome:</label>
                    <div>
                        <input class="text" name="plugin[primary_contact_information][name]" type="text" tabindex="7" value="${out_none value=plugin.primary_contact_information.name /}" />
                    </div>
                </div>
                <div class="form-field">
                    <label>Email:</label>
                    <div>
                        <input class="text" name="plugin[primary_contact_information][email]" type="text" tabindex="9" value="${out_none value=plugin.primary_contact_information.email /}" />
                    </div>
                </div>
                <div class="form-field">
                    <label>Website:</label>
                    <div>
                        <input class="text" name="plugin[primary_contact_information][website]" type="text" tabindex="11" value="${out_none value=plugin.primary_contact_information.website /}" />
                    </div>
                </div>
            </div>
            <div class="column-second">
                <div class="form-field">
                    <label>Telefone:</label>
                    <input class="text" name="plugin[primary_contact_information][phone_number]" type="text" tabindex="8" value="${out_none value=plugin.primary_contact_information.phone_number /}" />
                </div>
                <div class="form-field">
                    <label>Fax:</label>
                    <input class="text" name="plugin[primary_contact_information][fax_number]" type="text" tabindex="10" value="${out_none value=plugin.primary_contact_information.fax_number /}" />
                </div>
            </div>
            <div class="clear"></div>
        </div>
        <div class="form-button-area">
            <div class="cancel button button-blue" tabindex="13">Cancelar</div>
            <div class="submit button button-green" tabindex="12">Criar</div>
        </div>
    </form>
</div>
