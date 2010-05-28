<div id="includes">
</div>
<div id="meta-data">
    <div class="area">contacts</div>
    <div class="side-panel">side_panel/contacts</div>
</div>
<div id="contents">
    <h1>Contactos</h1>
    <h2>Empresa - ${out_none value=company.name xml_escape=True /}</h2>
    <div class="message">${out_none value=result_message xml_escape=True /}</div>
    <form action_target="companies/edit/${out_none value=company.object_id xml_escape=True /}" id="edit-company" method="post">
        <div class="form-field-area">
            <h4>Dados da Empresa</h4>
            <hr/>
            <div class="column-first">
                <div class="form-field">
                    <label class="mandatory">Nome:</label>
                    <div><input class="text" name="company[name]" type="text" tabindex="1" value="${out_none value=company.name xml_escape=True /}" error="${out_none value=company.validation_errors_map.name /}" /></div>
                </div>
                <div class="form-field">
                    <label class="mandatory">Contribuinte:</label>
                    <div><input class="text" name="company[fiscal_id]" type="text" tabindex="3" value="${out_none value=company.fiscal_id xml_escape=True /}" error="${out_none value=company.validation_errors_map.fiscal_id /}" /></div>
                </div>
                <div class="form-field">
                    <label>Observações:</label>
                    <div><textarea class="text" name="company[observations]" tabindex="5">${out_none value=company.observations xml_escape=True /}</textarea></div>
                </div>
            </div>
            <div class="column-second">
                <div class="form-field">
                    <label class="mandatory">Morada:</label>
                    <div><input class="text" name="company[primary_contact_information][address]" type="text" tabindex="2" value="${out_none value=company.primary_contact_information.address xml_escape=True /}" error="${out_none value=company.primary_contact_information.validation_errors_map.address /}" /></div>
                </div>
                <div class="form-field">
                    <label class="mandatory">Cód. Postal: </label>
                    <div><input class="text" name="company[primary_contact_information][postal_code]" type="text" tabindex="4" value="${out_none value=company.primary_contact_information.postal_code xml_escape=True /}" error="${out_none value=company.primary_contact_information.validation_errors_map.postal_code /}" /></div>
                </div>
                <div class="form-field">
                    <label class="mandatory">País:</label>
                    <div>
                        <select name="company[primary_contact_information][country]" tabindex="6">
                            <option value="Portugal" ${if item=company.primary_contact_information.country value="Portugal" operator=eq}selected="selected"${/if}>Portugal</option>
                            <option value="United States" ${if item=company.primary_contact_information.country value="United States" operator=eq}selected="selected"${/if}>United States</option>
                            <option value="UK" ${if item=company.primary_contact_information.country value="UK" operator=eq}selected="selected"${/if}>UK</option>
                            <option value="Ireland" ${if item=company.primary_contact_information.country value="Ireland" operator=eq}selected="selected"${/if}>Ireland</option>
                            <option value="Canada" ${if item=company.primary_contact_information.country value="Canada" operator=eq}selected="selected"${/if}>Canada</option>
                            <option value="Australia" ${if item=company.primary_contact_information.country value="Australia" operator=eq}selected="selected"${/if}>Australia</option>
                            <option value="New Zealand" ${if item=company.primary_contact_information.country value="New Zealand" operator=eq}selected="selected"${/if}>New Zealand</option>
                            <option value="South Africa" ${if item=company.primary_contact_information.country value="South Africa" operator=eq}selected="selected"${/if}>South Africa</option>
                            <option value="Afghanistan" ${if item=company.primary_contact_information.country value="Afghanistan" operator=eq}selected="selected"${/if}>Afghanistan</option>
                            <option value="Albania" ${if item=company.primary_contact_information.country value="Albania" operator=eq}selected="selected"${/if}>Albania</option>
                            <option value="Algeria" ${if item=company.primary_contact_information.country value="Algeria" operator=eq}selected="selected"${/if}>Algeria</option>
                            <option value="American Samoa" ${if item=company.primary_contact_information.country value="American Samoa" operator=eq}selected="selected"${/if}>American Samoa</option>
                            <option value="Andorra" ${if item=company.primary_contact_information.country value="Andorra" operator=eq}selected="selected"${/if}>Andorra</option>
                            <option value="Angola" ${if item=company.primary_contact_information.country value="Angola" operator=eq}selected="selected"${/if}>Angola</option>
                            <option value="Anguilla" ${if item=company.primary_contact_information.country value="Anguilla" operator=eq}selected="selected"${/if}>Anguilla</option>
                            <option value="Antigua and Barbuda" ${if item=company.primary_contact_information.country value="Antigua and Barbuda" operator=eq}selected="selected"${/if}>Antigua and Barbuda</option>
                            <option value="Argentina" ${if item=company.primary_contact_information.country value="Argentina" operator=eq}selected="selected"${/if}>Argentina</option>
                            <option value="Armenia" ${if item=company.primary_contact_information.country value="Armenia" operator=eq}selected="selected"${/if}>Armenia</option>
                            <option value="Aruba" ${if item=company.primary_contact_information.country value="Aruba" operator=eq}selected="selected"${/if}>Aruba</option>
                            <option value="Austria" ${if item=company.primary_contact_information.country value="Austria" operator=eq}selected="selected"${/if}>Austria</option>
                            <option value="Azerbaijan" ${if item=company.primary_contact_information.country value="Azerbaijan" operator=eq}selected="selected"${/if}>Azerbaijan</option>
                            <option value="Bahamas" ${if item=company.primary_contact_information.country value="Bahamas" operator=eq}selected="selected"${/if}>Bahamas</option>
                            <option value="Bahrain" ${if item=company.primary_contact_information.country value="Bahrain" operator=eq}selected="selected"${/if}>Bahrain</option>
                            <option value="Bangladesh" ${if item=company.primary_contact_information.country value="Bangladesh" operator=eq}selected="selected"${/if}>Bangladesh</option>
                            <option value="Barbados" ${if item=company.primary_contact_information.country value="Barbados" operator=eq}selected="selected"${/if}>Barbados</option>
                            <option value="Belarus" ${if item=company.primary_contact_information.country value="Belarus" operator=eq}selected="selected"${/if}>Belarus</option>
                            <option value="Belgium" ${if item=company.primary_contact_information.country value="Belgium" operator=eq}selected="selected"${/if}>Belgium</option>
                            <option value="Belize" ${if item=company.primary_contact_information.country value="Belize" operator=eq}selected="selected"${/if}>Belize</option>
                            <option value="Benin" ${if item=company.primary_contact_information.country value="Benin" operator=eq}selected="selected"${/if}>Benin</option>
                            <option value="Bermuda" ${if item=company.primary_contact_information.country value="Bermuda" operator=eq}selected="selected"${/if}>Bermuda</option>
                            <option value="Bhutan" ${if item=company.primary_contact_information.country value="Bhutan" operator=eq}selected="selected"${/if}>Bhutan</option>
                            <option value="Bolivia" ${if item=company.primary_contact_information.country value="Bolivia" operator=eq}selected="selected"${/if}>Bolivia</option>
                            <option value="Bosnia-Herzegovina" ${if item=company.primary_contact_information.country value="Bosnia-Herzegovina" operator=eq}selected="selected"${/if}>Bosnia-Herzegovina</option>
                            <option value="Botswana" ${if item=company.primary_contact_information.country value="Botswana" operator=eq}selected="selected"${/if}>Botswana</option>
                            <option value="Brazil" ${if item=company.primary_contact_information.country value="Brazil" operator=eq}selected="selected"${/if}>Brazil</option>
                            <option value="British Indian Ocean Territory" ${if item=company.primary_contact_information.country value="British Indian Ocean Territory" operator=eq}selected="selected"${/if}>British Indian Ocean Territory</option>
                            <option value="Brunei" ${if item=company.primary_contact_information.country value="Brunei" operator=eq}selected="selected"${/if}>Brunei</option>
                            <option value="Bulgaria" ${if item=company.primary_contact_information.country value="Bulgaria" operator=eq}selected="selected"${/if}>Bulgaria</option>
                            <option value="Burkina Faso" ${if item=company.primary_contact_information.country value="Burkina Faso" operator=eq}selected="selected"${/if}>Burkina Faso</option>
                            <option value="Burma" ${if item=company.primary_contact_information.country value="Burma" operator=eq}selected="selected"${/if}>Burma</option>
                            <option value="Burundi" ${if item=company.primary_contact_information.country value="Burundi" operator=eq}selected="selected"${/if}>Burundi</option>
                            <option value="Cambodia" ${if item=company.primary_contact_information.country value="Cambodia" operator=eq}selected="selected"${/if}>Cambodia</option>
                            <option value="Cameroon" ${if item=company.primary_contact_information.country value="Cameroon" operator=eq}selected="selected"${/if}>Cameroon</option>
                            <option value="Canton and Enderbury Islands" ${if item=company.primary_contact_information.country value="Canton and Enderbury Islands" operator=eq}selected="selected"${/if}>Canton and Enderbury Islands</option>
                            <option value="Cape Verde" ${if item=company.primary_contact_information.country value="Cape Verde" operator=eq}selected="selected"${/if}>Cape Verde</option>
                            <option value="Cayman Islands" ${if item=company.primary_contact_information.country value="Cayman Islands" operator=eq}selected="selected"${/if}>Cayman Islands</option>
                            <option value="Côte d'Ivoire" ${if item=company.primary_contact_information.country value="Côte d'Ivoire" operator=eq}selected="selected"${/if}>Côte d'Ivoire</option>
                            <option value="Central African Republic" ${if item=company.primary_contact_information.country value="Central African Republic" operator=eq}selected="selected"${/if}>Central African Republic</option>
                            <option value="Chad" ${if item=company.primary_contact_information.country value="Chad" operator=eq}selected="selected"${/if}>Chad</option>
                            <option value="Chile" ${if item=company.primary_contact_information.country value="Chile" operator=eq}selected="selected"${/if}>Chile</option>
                            <option value="China" ${if item=company.primary_contact_information.country value="China" operator=eq}selected="selected"${/if}>China</option>
                            <option value="Christmas Island" ${if item=company.primary_contact_information.country value="Christmas Island" operator=eq}selected="selected"${/if}>Christmas Island</option>
                            <option value="Cocos (Keeling) Islands" ${if item=company.primary_contact_information.country value="Cocos (Keeling) Islands" operator=eq}selected="selected"${/if}>Cocos (Keeling) Islands</option>
                            <option value="Colombia" ${if item=company.primary_contact_information.country value="Colombia" operator=eq}selected="selected"${/if}>Colombia</option>
                            <option value="Comoros" ${if item=company.primary_contact_information.country value="Comoros" operator=eq}selected="selected"${/if}>Comoros</option>
                            <option value="Congo" ${if item=company.primary_contact_information.country value="Congo" operator=eq}selected="selected"${/if}>Congo</option>
                            <option value="Congo, Democratic Republic" ${if item=company.primary_contact_information.country value="Congo, Democratic Republic" operator=eq}selected="selected"${/if}>Congo, Democratic Republic</option>
                            <option value="Cook Islands" ${if item=company.primary_contact_information.country value="Cook Islands" operator=eq}selected="selected"${/if}>Cook Islands</option>
                            <option value="Costa Rica" ${if item=company.primary_contact_information.country value="Costa Rica" operator=eq}selected="selected"${/if}>Costa Rica</option>
                            <option value="Croatia" ${if item=company.primary_contact_information.country value="Croatia" operator=eq}selected="selected"${/if}>Croatia</option>
                            <option value="Cuba" ${if item=company.primary_contact_information.country value="Cuba" operator=eq}selected="selected"${/if}>Cuba</option>
                            <option value="Cyprus" ${if item=company.primary_contact_information.country value="Cyprus" operator=eq}selected="selected"${/if}>Cyprus</option>
                            <option value="Czech Republic" ${if item=company.primary_contact_information.country value="Czech Republic" operator=eq}selected="selected"${/if}>Czech Republic</option>
                            <option value="Denmark" ${if item=company.primary_contact_information.country value="Denmark" operator=eq}selected="selected"${/if}>Denmark</option>
                            <option value="Djibouti" ${if item=company.primary_contact_information.country value="Djibouti" operator=eq}selected="selected"${/if}>Djibouti</option>
                            <option value="Dominica" ${if item=company.primary_contact_information.country value="Dominica" operator=eq}selected="selected"${/if}>Dominica</option>
                            <option value="Dominican Republic" ${if item=company.primary_contact_information.country value="Dominican Republic" operator=eq}selected="selected"${/if}>Dominican Republic</option>
                            <option value="Dronning Maud Land" ${if item=company.primary_contact_information.country value="Dronning Maud Land" operator=eq}selected="selected"${/if}>Dronning Maud Land</option>
                            <option value="East Timor" ${if item=company.primary_contact_information.country value="East Timor" operator=eq}selected="selected"${/if}>East Timor</option>
                            <option value="Ecuador" ${if item=company.primary_contact_information.country value="Ecuador" operator=eq}selected="selected"${/if}>Ecuador</option>
                            <option value="Egypt" ${if item=company.primary_contact_information.country value="Egypt" operator=eq}selected="selected"${/if}>Egypt</option>
                            <option value="El Salvador" ${if item=company.primary_contact_information.country value="El Salvador" operator=eq}selected="selected"${/if}>El Salvador</option>
                            <option value="Equatorial Guinea" ${if item=company.primary_contact_information.country value="Equatorial Guinea" operator=eq}selected="selected"${/if}>Equatorial Guinea</option>
                            <option value="Eritrea" ${if item=company.primary_contact_information.country value="Eritrea" operator=eq}selected="selected"${/if}>Eritrea</option>
                            <option value="Estonia" ${if item=company.primary_contact_information.country value="Estonia" operator=eq}selected="selected"${/if}>Estonia</option>
                            <option value="Ethiopia" ${if item=company.primary_contact_information.country value="Ethiopia" operator=eq}selected="selected"${/if}>Ethiopia</option>
                            <option value="Faeroe Islands (Føroyar)" ${if item=company.primary_contact_information.country value="Faeroe Islands (Føroyar)" operator=eq}selected="selected"${/if}>Faeroe Islands (Føroyar)</option>
                            <option value="Falkland Islands" ${if item=company.primary_contact_information.country value="Falkland Islands" operator=eq}selected="selected"${/if}>Falkland Islands</option>
                            <option value="Fiji" ${if item=company.primary_contact_information.country value="Fiji" operator=eq}selected="selected"${/if}>Fiji</option>
                            <option value="Finland" ${if item=company.primary_contact_information.country value="Finland" operator=eq}selected="selected"${/if}>Finland</option>
                            <option value="France" ${if item=company.primary_contact_information.country value="France" operator=eq}selected="selected"${/if}>France</option>
                            <option value="French Guiana" ${if item=company.primary_contact_information.country value="French Guiana" operator=eq}selected="selected"${/if}>French Guiana</option>
                            <option value="French Polynesia" ${if item=company.primary_contact_information.country value="French Polynesia" operator=eq}selected="selected"${/if}>French Polynesia</option>
                            <option value="Gabon" ${if item=company.primary_contact_information.country value="Gabon" operator=eq}selected="selected"${/if}>Gabon</option>
                            <option value="Gambia" ${if item=company.primary_contact_information.country value="Gambia" operator=eq}selected="selected"${/if}>Gambia</option>
                            <option value="Georgia" ${if item=company.primary_contact_information.country value="Georgia" operator=eq}selected="selected"${/if}>Georgia</option>
                            <option value="Germany" ${if item=company.primary_contact_information.country value="Germany" operator=eq}selected="selected"${/if}>Germany</option>
                            <option value="Ghana" ${if item=company.primary_contact_information.country value="Ghana" operator=eq}selected="selected"${/if}>Ghana</option>
                            <option value="Gibraltar" ${if item=company.primary_contact_information.country value="Gibraltar" operator=eq}selected="selected"${/if}>Gibraltar</option>
                            <option value="Great Britain" ${if item=company.primary_contact_information.country value="Great Britain" operator=eq}selected="selected"${/if}>Great Britain</option>
                            <option value="Greece" ${if item=company.primary_contact_information.country value="Greece" operator=eq}selected="selected"${/if}>Greece</option>
                            <option value="Greenland" ${if item=company.primary_contact_information.country value="Greenland" operator=eq}selected="selected"${/if}>Greenland</option>
                            <option value="Grenada" ${if item=company.primary_contact_information.country value="Grenada" operator=eq}selected="selected"${/if}>Grenada</option>
                            <option value="Guadeloupe" ${if item=company.primary_contact_information.country value="Guadeloupe" operator=eq}selected="selected"${/if}>Guadeloupe</option>
                            <option value="Guam" ${if item=company.primary_contact_information.country value="Guam" operator=eq}selected="selected"${/if}>Guam</option>
                            <option value="Guatemala" ${if item=company.primary_contact_information.country value="Guatemala" operator=eq}selected="selected"${/if}>Guatemala</option>
                            <option value="Guernsey" ${if item=company.primary_contact_information.country value="Guernsey" operator=eq}selected="selected"${/if}>Guernsey</option>
                            <option value="Guinea" ${if item=company.primary_contact_information.country value="Guinea" operator=eq}selected="selected"${/if}>Guinea</option>
                            <option value="Guinea-Bissau" ${if item=company.primary_contact_information.country value="Guinea-Bissau" operator=eq}selected="selected"${/if}>Guinea-Bissau</option>
                            <option value="Guyana" ${if item=company.primary_contact_information.country value="Guyana" operator=eq}selected="selected"${/if}>Guyana</option>
                            <option value="Haiti" ${if item=company.primary_contact_information.country value="Haiti" operator=eq}selected="selected"${/if}>Haiti</option>
                            <option value="Heard and McDonald Islands" ${if item=company.primary_contact_information.country value="Heard and McDonald Islands" operator=eq}selected="selected"${/if}>Heard and McDonald Islands</option>
                            <option value="Honduras" ${if item=company.primary_contact_information.country value="Honduras" operator=eq}selected="selected"${/if}>Honduras</option>
                            <option value="Hong Kong" ${if item=company.primary_contact_information.country value="Hong Kong" operator=eq}selected="selected"${/if}>Hong Kong</option>
                            <option value="Hungary" ${if item=company.primary_contact_information.country value="Hungary" operator=eq}selected="selected"${/if}>Hungary</option>
                            <option value="Iceland" ${if item=company.primary_contact_information.country value="Iceland" operator=eq}selected="selected"${/if}>Iceland</option>
                            <option value="India" ${if item=company.primary_contact_information.country value="India" operator=eq}selected="selected"${/if}>India</option>
                            <option value="Indonesia" ${if item=company.primary_contact_information.country value="Indonesia" operator=eq}selected="selected"${/if}>Indonesia</option>
                            <option value="International Monetary Fund" ${if item=company.primary_contact_information.country value="International Monetary Fund" operator=eq}selected="selected"${/if}>International Monetary Fund</option>
                            <option value="Iran" ${if item=company.primary_contact_information.country value="Iran" operator=eq}selected="selected"${/if}>Iran</option>
                            <option value="Iraq" ${if item=company.primary_contact_information.country value="Iraq" operator=eq}selected="selected"${/if}>Iraq</option>
                            <option value="Isle of Man" ${if item=company.primary_contact_information.country value="Isle of Man" operator=eq}selected="selected"${/if}>Isle of Man</option>
                            <option value="Israel" ${if item=company.primary_contact_information.country value="Israel" operator=eq}selected="selected"${/if}>Israel</option>
                            <option value="Italy" ${if item=company.primary_contact_information.country value="Italy" operator=eq}selected="selected"${/if}>Italy</option>
                            <option value="Ivory Coast" ${if item=company.primary_contact_information.country value="Ivory Coast" operator=eq}selected="selected"${/if}>Ivory Coast</option>
                            <option value="Jamaica" ${if item=company.primary_contact_information.country value="Jamaica" operator=eq}selected="selected"${/if}>Jamaica</option>
                            <option value="Japan" ${if item=company.primary_contact_information.country value="Japan" operator=eq}selected="selected"${/if}>Japan</option>
                            <option value="Jersey" ${if item=company.primary_contact_information.country value="Jersey" operator=eq}selected="selected"${/if}>Jersey</option>
                            <option value="Johnston Island" ${if item=company.primary_contact_information.country value="Johnston Island" operator=eq}selected="selected"${/if}>Johnston Island</option>
                            <option value="Jordan" ${if item=company.primary_contact_information.country value="Jordan" operator=eq}selected="selected"${/if}>Jordan</option>
                            <option value="Kampuchea" ${if item=company.primary_contact_information.country value="Kampuchea" operator=eq}selected="selected"${/if}>Kampuchea</option>
                            <option value="Kazakhstan" ${if item=company.primary_contact_information.country value="Kazakhstan" operator=eq}selected="selected"${/if}>Kazakhstan</option>
                            <option value="Kenya" ${if item=company.primary_contact_information.country value="Kenya" operator=eq}selected="selected"${/if}>Kenya</option>
                            <option value="Kiribati" ${if item=company.primary_contact_information.country value="Kiribati" operator=eq}selected="selected"${/if}>Kiribati</option>
                            <option value="Korea, North" ${if item=company.primary_contact_information.country value="Korea, North" operator=eq}selected="selected"${/if}>Korea, North</option>
                            <option value="Korea, South" ${if item=company.primary_contact_information.country value="Korea, South" operator=eq}selected="selected"${/if}>Korea, South</option>
                            <option value="Kuwait" ${if item=company.primary_contact_information.country value="Kuwait" operator=eq}selected="selected"${/if}>Kuwait</option>
                            <option value="Kyrgyzstan" ${if item=company.primary_contact_information.country value="Kyrgyzstan" operator=eq}selected="selected"${/if}>Kyrgyzstan</option>
                            <option value="Laos" ${if item=company.primary_contact_information.country value="Laos" operator=eq}selected="selected"${/if}>Laos</option>
                            <option value="Latvia" ${if item=company.primary_contact_information.country value="Latvia" operator=eq}selected="selected"${/if}>Latvia</option>
                            <option value="Lebanon" ${if item=company.primary_contact_information.country value="Lebanon" operator=eq}selected="selected"${/if}>Lebanon</option>
                            <option value="Lesotho" ${if item=company.primary_contact_information.country value="Lesotho" operator=eq}selected="selected"${/if}>Lesotho</option>
                            <option value="Liberia" ${if item=company.primary_contact_information.country value="Liberia" operator=eq}selected="selected"${/if}>Liberia</option>
                            <option value="Libya" ${if item=company.primary_contact_information.country value="Libya" operator=eq}selected="selected"${/if}>Libya</option>
                            <option value="Liechtenstein" ${if item=company.primary_contact_information.country value="Liechtenstein" operator=eq}selected="selected"${/if}>Liechtenstein</option>
                            <option value="Lithuania" ${if item=company.primary_contact_information.country value="Lithuania" operator=eq}selected="selected"${/if}>Lithuania</option>
                            <option value="Luxembourg" ${if item=company.primary_contact_information.country value="Luxembourg" operator=eq}selected="selected"${/if}>Luxembourg</option>
                            <option value="Macau" ${if item=company.primary_contact_information.country value="Macau" operator=eq}selected="selected"${/if}>Macau</option>
                            <option value="Macedonia (Former Yug. Rep.)" ${if item=company.primary_contact_information.country value="Macedonia (Former Yug. Rep.)" operator=eq}selected="selected"${/if}>Macedonia (Former Yug. Rep.)</option>
                            <option value="Madagascar" ${if item=company.primary_contact_information.country value="Madagascar" operator=eq}selected="selected"${/if}>Madagascar</option>
                            <option value="Malawi" ${if item=company.primary_contact_information.country value="Malawi" operator=eq}selected="selected"${/if}>Malawi</option>
                            <option value="Malaysia" ${if item=company.primary_contact_information.country value="Malaysia" operator=eq}selected="selected"${/if}>Malaysia</option>
                            <option value="Maldives" ${if item=company.primary_contact_information.country value="Maldives" operator=eq}selected="selected"${/if}>Maldives</option>
                            <option value="Mali" ${if item=company.primary_contact_information.country value="Mali" operator=eq}selected="selected"${/if}>Mali</option>
                            <option value="Malta" ${if item=company.primary_contact_information.country value="Malta" operator=eq}selected="selected"${/if}>Malta</option>
                            <option value="Martinique" ${if item=company.primary_contact_information.country value="Martinique" operator=eq}selected="selected"${/if}>Martinique</option>
                            <option value="Mauritania" ${if item=company.primary_contact_information.country value="Mauritania" operator=eq}selected="selected"${/if}>Mauritania</option>
                            <option value="Mauritius" ${if item=company.primary_contact_information.country value="Mauritius" operator=eq}selected="selected"${/if}>Mauritius</option>
                            <option value="Mayotte" ${if item=company.primary_contact_information.country value="Mayotte" operator=eq}selected="selected"${/if}>Mayotte</option>
                            <option value="Mexico" ${if item=company.primary_contact_information.country value="Mexico" operator=eq}selected="selected"${/if}>Mexico</option>
                            <option value="Micronesia" ${if item=company.primary_contact_information.country value="Micronesia" operator=eq}selected="selected"${/if}>Micronesia</option>
                            <option value="Midway Islands" ${if item=company.primary_contact_information.country value="Midway Islands" operator=eq}selected="selected"${/if}>Midway Islands</option>
                            <option value="Moldova" ${if item=company.primary_contact_information.country value="Moldova" operator=eq}selected="selected"${/if}>Moldova</option>
                            <option value="Monaco" ${if item=company.primary_contact_information.country value="Monaco" operator=eq}selected="selected"${/if}>Monaco</option>
                            <option value="Mongolia" ${if item=company.primary_contact_information.country value="Mongolia" operator=eq}selected="selected"${/if}>Mongolia</option>
                            <option value="Montenegro" ${if item=company.primary_contact_information.country value="Montenegro" operator=eq}selected="selected"${/if}>Montenegro</option>
                            <option value="Montserrat" ${if item=company.primary_contact_information.country value="Montserrat" operator=eq}selected="selected"${/if}>Montserrat</option>
                            <option value="Morocco" ${if item=company.primary_contact_information.country value="Morocco" operator=eq}selected="selected"${/if}>Morocco</option>
                            <option value="Mozambique" ${if item=company.primary_contact_information.country value="Mozambique" operator=eq}selected="selected"${/if}>Mozambique</option>
                            <option value="Myanmar" ${if item=company.primary_contact_information.country value="Myanmar" operator=eq}selected="selected"${/if}>Myanmar</option>
                            <option value="Namibia" ${if item=company.primary_contact_information.country value="Namibia" operator=eq}selected="selected"${/if}>Namibia</option>
                            <option value="Nauru" ${if item=company.primary_contact_information.country value="Nauru" operator=eq}selected="selected"${/if}>Nauru</option>
                            <option value="Nepal" ${if item=company.primary_contact_information.country value="Nepal" operator=eq}selected="selected"${/if}>Nepal</option>
                            <option value="Netherlands" ${if item=company.primary_contact_information.country value="Netherlands" operator=eq}selected="selected"${/if}>Netherlands</option>
                            <option value="Netherlands Antilles" ${if item=company.primary_contact_information.country value="Netherlands Antilles" operator=eq}selected="selected"${/if}>Netherlands Antilles</option>
                            <option value="New Caledonia" ${if item=company.primary_contact_information.country value="New Caledonia" operator=eq}selected="selected"${/if}>New Caledonia</option>
                            <option value="Nicaragua" ${if item=company.primary_contact_information.country value="Nicaragua" operator=eq}selected="selected"${/if}>Nicaragua</option>
                            <option value="Niger" ${if item=company.primary_contact_information.country value="Niger" operator=eq}selected="selected"${/if}>Niger</option>
                            <option value="Nigeria" ${if item=company.primary_contact_information.country value="Nigeria" operator=eq}selected="selected"${/if}>Nigeria</option>
                            <option value="Niue" ${if item=company.primary_contact_information.country value="Niue" operator=eq}selected="selected"${/if}>Niue</option>
                            <option value="Norfolk Island" ${if item=company.primary_contact_information.country value="Norfolk Island" operator=eq}selected="selected"${/if}>Norfolk Island</option>
                            <option value="Northern Mariana Islands" ${if item=company.primary_contact_information.country value="Northern Mariana Islands" operator=eq}selected="selected"${/if}>Northern Mariana Islands</option>
                            <option value="Norway" ${if item=company.primary_contact_information.country value="Norway" operator=eq}selected="selected"${/if}>Norway</option>
                            <option value="Oman" ${if item=company.primary_contact_information.country value="Oman" operator=eq}selected="selected"${/if}>Oman</option>
                            <option value="Pakistan" ${if item=company.primary_contact_information.country value="Pakistan" operator=eq}selected="selected"${/if}>Pakistan</option>
                            <option value="Palau" ${if item=company.primary_contact_information.country value="Palau" operator=eq}selected="selected"${/if}>Palau</option>
                            <option value="Panama" ${if item=company.primary_contact_information.country value="Panama" operator=eq}selected="selected"${/if}>Panama</option>
                            <option value="Papua New Guinea" ${if item=company.primary_contact_information.country value="Papua New Guinea" operator=eq}selected="selected"${/if}>Papua New Guinea</option>
                            <option value="Paraguay" ${if item=company.primary_contact_information.country value="Paraguay" operator=eq}selected="selected"${/if}>Paraguay</option>
                            <option value="Peru" ${if item=company.primary_contact_information.country value="Peru" operator=eq}selected="selected"${/if}>Peru</option>
                            <option value="Philippines" ${if item=company.primary_contact_information.country value="Philippines" operator=eq}selected="selected"${/if}>Philippines</option>
                            <option value="Pitcairn Island" ${if item=company.primary_contact_information.country value="Pitcairn Island" operator=eq}selected="selected"${/if}>Pitcairn Island</option>
                            <option value="Poland" ${if item=company.primary_contact_information.country value="Poland" operator=eq}selected="selected"${/if}>Poland</option>
                            <option value="Puerto Rico" ${if item=company.primary_contact_information.country value="Puerto Rico" operator=eq}selected="selected"${/if}>Puerto Rico</option>
                            <option value="Qatar" ${if item=company.primary_contact_information.country value="Qatar" operator=eq}selected="selected"${/if}>Qatar</option>
                            <option value="Reunion" ${if item=company.primary_contact_information.country value="Reunion" operator=eq}selected="selected"${/if}>Reunion</option>
                            <option value="Romania" ${if item=company.primary_contact_information.country value="Romania" operator=eq}selected="selected"${/if}>Romania</option>
                            <option value="Russia" ${if item=company.primary_contact_information.country value="Russia" operator=eq}selected="selected"${/if}>Russia</option>
                            <option value="Rwanda" ${if item=company.primary_contact_information.country value="Rwanda" operator=eq}selected="selected"${/if}>Rwanda</option>
                            <option value="Samoa (America)" ${if item=company.primary_contact_information.country value="Samoa (America)" operator=eq}selected="selected"${/if}>Samoa (America)</option>
                            <option value="Samoa (Western)" ${if item=company.primary_contact_information.country value="Samoa (Western)" operator=eq}selected="selected"${/if}>Samoa (Western)</option>
                            <option value="San Marino" ${if item=company.primary_contact_information.country value="San Marino" operator=eq}selected="selected"${/if}>San Marino</option>
                            <option value="Saudi Arabia" ${if item=company.primary_contact_information.country value="Saudi Arabia" operator=eq}selected="selected"${/if}>Saudi Arabia</option>
                            <option value="São Tomé and Príncipe" ${if item=company.primary_contact_information.country value="São Tomé and Príncipe" operator=eq}selected="selected"${/if}>São Tomé and Príncipe</option>
                            <option value="Sénégal" ${if item=company.primary_contact_information.country value="Sénégal" operator=eq}selected="selected"${/if}>Sénégal</option>
                            <option value="Serbia" ${if item=company.primary_contact_information.country value="Serbia" operator=eq}selected="selected"${/if}>Serbia</option>
                            <option value="Seychelles" ${if item=company.primary_contact_information.country value="Seychelles" operator=eq}selected="selected"${/if}>Seychelles</option>
                            <option value="Sierra Leone" ${if item=company.primary_contact_information.country value="Sierra Leone" operator=eq}selected="selected"${/if}>Sierra Leone</option>
                            <option value="Singapore" ${if item=company.primary_contact_information.country value="Singapore" operator=eq}selected="selected"${/if}>Singapore</option>
                            <option value="Slovakia" ${if item=company.primary_contact_information.country value="Slovakia" operator=eq}selected="selected"${/if}>Slovakia</option>
                            <option value="Slovenia" ${if item=company.primary_contact_information.country value="Slovenia" operator=eq}selected="selected"${/if}>Slovenia</option>
                            <option value="Solomon Islands" ${if item=company.primary_contact_information.country value="Solomon Islands" operator=eq}selected="selected"${/if}>Solomon Islands</option>
                            <option value="Somalia" ${if item=company.primary_contact_information.country value="Somalia" operator=eq}selected="selected"${/if}>Somalia</option>
                            <option value="Spain" ${if item=company.primary_contact_information.country value="Spain" operator=eq}selected="selected"${/if}>Spain</option>
                            <option value="Sri Lanka" ${if item=company.primary_contact_information.country value="Sri Lanka" operator=eq}selected="selected"${/if}>Sri Lanka</option>
                            <option value="St. Helena" ${if item=company.primary_contact_information.country value="St. Helena" operator=eq}selected="selected"${/if}>St. Helena</option>
                            <option value="St. Kitts and Nevis" ${if item=company.primary_contact_information.country value="St. Kitts and Nevis" operator=eq}selected="selected"${/if}>St. Kitts and Nevis</option>
                            <option value="St. Lucia" ${if item=company.primary_contact_information.country value="St. Lucia" operator=eq}selected="selected"${/if}>St. Lucia</option>
                            <option value="St. Vincent and the Grenadines" ${if item=company.primary_contact_information.country value="St. Vincent and the Grenadines" operator=eq}selected="selected"${/if}>St. Vincent and the Grenadines</option>
                            <option value="Sudan" ${if item=company.primary_contact_information.country value="Sudan" operator=eq}selected="selected"${/if}>Sudan</option>
                            <option value="Suriname" ${if item=company.primary_contact_information.country value="Suriname" operator=eq}selected="selected"${/if}>Suriname</option>
                            <option value="Svalbard and Jan Mayen Islands" ${if item=company.primary_contact_information.country value="Svalbard and Jan Mayen Islands" operator=eq}selected="selected"${/if}>Svalbard and Jan Mayen Islands</option>
                            <option value="Swaziland" ${if item=company.primary_contact_information.country value="Swaziland" operator=eq}selected="selected"${/if}>Swaziland</option>
                            <option value="Sweden" ${if item=company.primary_contact_information.country value="Sweden" operator=eq}selected="selected"${/if}>Sweden</option>
                            <option value="Switzerland" ${if item=company.primary_contact_information.country value="Switzerland" operator=eq}selected="selected"${/if}>Switzerland</option>
                            <option value="Syria" ${if item=company.primary_contact_information.country value="Syria" operator=eq}selected="selected"${/if}>Syria</option>
                            <option value="Tahiti" ${if item=company.primary_contact_information.country value="Tahiti" operator=eq}selected="selected"${/if}>Tahiti</option>
                            <option value="Taiwan" ${if item=company.primary_contact_information.country value="Taiwan" operator=eq}selected="selected"${/if}>Taiwan</option>
                            <option value="Tajikistan" ${if item=company.primary_contact_information.country value="Tajikistan" operator=eq}selected="selected"${/if}>Tajikistan</option>
                            <option value="Tanzania" ${if item=company.primary_contact_information.country value="Tanzania" operator=eq}selected="selected"${/if}>Tanzania</option>
                            <option value="Thailand" ${if item=company.primary_contact_information.country value="Thailand" operator=eq}selected="selected"${/if}>Thailand</option>
                            <option value="Timor-Leste" ${if item=company.primary_contact_information.country value="Timor-Leste" operator=eq}selected="selected"${/if}>Timor-Leste</option>
                            <option value="Togo" ${if item=company.primary_contact_information.country value="Togo" operator=eq}selected="selected"${/if}>Togo</option>
                            <option value="Trinidad and Tobago" ${if item=company.primary_contact_information.country value="Trinidad and Tobago" operator=eq}selected="selected"${/if}>Trinidad and Tobago</option>
                            <option value="Tunisia" ${if item=company.primary_contact_information.country value="Tunisia" operator=eq}selected="selected"${/if}>Tunisia</option>
                            <option value="Turkey" ${if item=company.primary_contact_information.country value="Turkey" operator=eq}selected="selected"${/if}>Turkey</option>
                            <option value="Turkmenistan" ${if item=company.primary_contact_information.country value="Turkmenistan" operator=eq}selected="selected"${/if}>Turkmenistan</option>
                            <option value="Turks and Caicos Islands" ${if item=company.primary_contact_information.country value="Turks and Caicos Islands" operator=eq}selected="selected"${/if}>Turks and Caicos Islands</option>
                            <option value="Tuvalu" ${if item=company.primary_contact_information.country value="Tuvalu" operator=eq}selected="selected"${/if}>Tuvalu</option>
                            <option value="Uganda" ${if item=company.primary_contact_information.country value="Uganda" operator=eq}selected="selected"${/if}>Uganda</option>
                            <option value="Ukraine" ${if item=company.primary_contact_information.country value="Ukraine" operator=eq}selected="selected"${/if}>Ukraine</option>
                            <option value="United Arab Emirates" ${if item=company.primary_contact_information.country value="United Arab Emirates" operator=eq}selected="selected"${/if}>United Arab Emirates</option>
                            <option value="Upper Volta" ${if item=company.primary_contact_information.country value="Upper Volta" operator=eq}selected="selected"${/if}>Upper Volta</option>
                            <option value="Uruguay" ${if item=company.primary_contact_information.country value="Uruguay" operator=eq}selected="selected"${/if}>Uruguay</option>
                            <option value="Uzbekistan" ${if item=company.primary_contact_information.country value="Uzbekistan" operator=eq}selected="selected"${/if}>Uzbekistan</option>
                            <option value="Vanuatu" ${if item=company.primary_contact_information.country value="Vanuatu" operator=eq}selected="selected"${/if}>Vanuatu</option>
                            <option value="Vatican" ${if item=company.primary_contact_information.country value="Vatican" operator=eq}selected="selected"${/if}>Vatican</option>
                            <option value="Venezuela" ${if item=company.primary_contact_information.country value="Venezuela" operator=eq}selected="selected"${/if}>Venezuela</option>
                            <option value="Vietnam" ${if item=company.primary_contact_information.country value="Vietnam" operator=eq}selected="selected"${/if}>Vietnam</option>
                            <option value="Virgin Islands" ${if item=company.primary_contact_information.country value="Virgin Islands" operator=eq}selected="selected"${/if}>Virgin Islands</option>
                            <option value="Wake Island" ${if item=company.primary_contact_information.country value="Wake Island" operator=eq}selected="selected"${/if}>Wake Island</option>
                            <option value="Wallis and Futuna Islands" ${if item=company.primary_contact_information.country value="Wallis and Futuna Islands" operator=eq}selected="selected"${/if}>Wallis and Futuna Islands</option>
                            <option value="Western Sahara" ${if item=company.primary_contact_information.country value="Western Sahara" operator=eq}selected="selected"${/if}>Western Sahara</option>
                            <option value="Western Samoa" ${if item=company.primary_contact_information.country value="Western Samoa" operator=eq}selected="selected"${/if}>Western Samoa</option>
                            <option value="Yemen" ${if item=company.primary_contact_information.country value="Yemen" operator=eq}selected="selected"${/if}>Yemen</option>
                            <option value="Zaïre" ${if item=company.primary_contact_information.country value="Zaïre" operator=eq}selected="selected"${/if}>Zaïre</option>
                            <option value="Zambia" ${if item=company.primary_contact_information.country value="Zambia" operator=eq}selected="selected"${/if}>Zambia</option>
                            <option value="Zimbabwe" ${if item=company.primary_contact_information.country value="Zimbabwe" operator=eq}selected="selected"${/if}>Zimbabwe</option>
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
                    <div><input class="text" name="company[primary_contact_information][name]" type="text" tabindex="7" value="${out_none value=company.primary_contact_information.name xml_escape=True /}" /></div>
                </div>
                <div class="form-field">
                    <label>Email:</label>
                    <div><input class="text" name="company[primary_contact_information][email]" type="text" tabindex="9" value="${out_none value=company.primary_contact_information.email xml_escape=True /}" /></div>
                </div>
                <div class="form-field">
                    <label>Website:</label>
                    <div><input class="text" name="company[primary_contact_information][website]" type="text" tabindex="11" value="${out_none value=company.primary_contact_information.website xml_escape=True /}" /></div>
                </div>
            </div>
            <div class="column-second">
                <div class="form-field">
                    <label>Telefone:</label>
                    <input class="text" name="company[primary_contact_information][phone_number]" type="text" tabindex="8" value="${out_none value=company.primary_contact_information.phone_number xml_escape=True /}" />
                </div>
                <div class="form-field">
                    <label>Fax:</label>
                    <input class="text" name="company[primary_contact_information][fax_number]" type="text" tabindex="10" value="${out_none value=company.primary_contact_information.fax_number xml_escape=True /}" />
                </div>
            </div>
            <div class="clear"></div>
        </div>
        <div class="form-button-area">
            <div class="cancel button button-blue" tabindex="13">Cancelar</div>
            <div class="submit button button-green" tabindex="12">Actualizar</div>
        </div>
    </form>
</div>
