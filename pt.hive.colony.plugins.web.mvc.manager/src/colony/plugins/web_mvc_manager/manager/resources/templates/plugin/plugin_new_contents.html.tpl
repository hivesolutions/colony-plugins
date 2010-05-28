<div id="includes">
</div>
<div id="meta-data">
    <div class="area">contacts</div>
    <div class="side-panel">side_panel/contacts</div>
</div>
<div id="contents">
    <h1>Contactos</h1>
    <h2>Criar Empresa</h2>
    <div class="message">${out_none value=result_message xml_escape=True /}</div>
    <form action_target="companies/new" class="new-company" method="post">
        <div class="form-field-area">
            <h4>Dados da Empresa</h4>
            <hr/>
            <div class="column-first">
                <div class="form-field">
                    <label class="mandatory">Nome:</label>
                    <div>
                        <input class="text" name="company[name]" type="text" tabindex="1" value="${out_none value=company.name /}" error="${out_none value=company.validation_errors_map.name /}" />
                    </div>
                </div>
                <div class="form-field">
                    <label class="mandatory">Contribuinte:</label>
                    <div>
                        <input class="text" name="company[fiscal_id]" type="text" tabindex="3" value="${out_none value=company.fiscal_id /}" error="${out_none value=company.validation_errors_map.fiscal_id /}" />
                    </div>
                </div>
                <div class="form-field">
                    <label>Observações:</label>
                    <div>
                        <textarea class="text" name="company[observations]" tabindex="5">${out_none value=company.observations /}</textarea>
                    </div>
                </div>
            </div>
            <div class="column-second">
                <div class="form-field">
                    <label class="mandatory">Morada:</label>
                    <div>
                        <input class="text" name="company[primary_contact_information][address]" type="text" tabindex="2" value="${out_none value=company.primary_contact_information.address /}" error="${out_none value=company.primary_contact_information.validation_errors_map.address /}" />
                    </div>
                </div>
                <div class="form-field">
                    <label class="mandatory">Cód. Postal:</label>
                    <div>
                        <input class="text" name="company[primary_contact_information][postal_code]" type="text" tabindex="4" value="${out_none value=company.primary_contact_information.postal_code /}" error="${out_none value=company.primary_contact_information.validation_errors_map.postal_code /}" />
                    </div>
                </div>
                <div class="form-field">
                    <label class="mandatory">País:</label>
                    <div>
                        <select name="company[primary_contact_information][country]" tabindex="6">
                            <option value="Portugal" selected="selected">Portugal</option>
                            <option value="United States">United States</option>
                            <option value="UK">UK</option>
                            <option value="Ireland">Ireland</option>
                            <option value="Canada">Canada</option>
                            <option value="Australia">Australia</option>
                            <option value="New Zealand">New Zealand</option>
                            <option value="South Africa">South Africa</option>
                            <option value="Afghanistan">Afghanistan</option>
                            <option value="Albania">Albania</option>
                            <option value="Algeria">Algeria</option>
                            <option value="American Samoa">American Samoa</option>
                            <option value="Andorra">Andorra</option>
                            <option value="Angola">Angola</option>
                            <option value="Anguilla">Anguilla</option>
                            <option value="Antigua and Barbuda">Antigua and Barbuda</option>
                            <option value="Argentina">Argentina</option>
                            <option value="Armenia">Armenia</option>
                            <option value="Aruba">Aruba</option>
                            <option value="Austria">Austria</option>
                            <option value="Azerbaijan">Azerbaijan</option>
                            <option value="Bahamas">Bahamas</option>
                            <option value="Bahrain">Bahrain</option>
                            <option value="Bangladesh">Bangladesh</option>
                            <option value="Barbados">Barbados</option>
                            <option value="Belarus">Belarus</option>
                            <option value="Belgium">Belgium</option>
                            <option value="Belize">Belize</option>
                            <option value="Benin">Benin</option>
                            <option value="Bermuda">Bermuda</option>
                            <option value="Bhutan">Bhutan</option>
                            <option value="Bolivia">Bolivia</option>
                            <option value="Bosnia-Herzegovina">Bosnia-Herzegovina</option>
                            <option value="Botswana">Botswana</option>
                            <option value="Brazil">Brazil</option>
                            <option value="British Indian Ocean Territory">British Indian Ocean Territory</option>
                            <option value="Brunei">Brunei</option>
                            <option value="Bulgaria">Bulgaria</option>
                            <option value="Burkina Faso">Burkina Faso</option>
                            <option value="Burma">Burma</option>
                            <option value="Burundi">Burundi</option>
                            <option value="Cambodia">Cambodia</option>
                            <option value="Cameroon">Cameroon</option>
                            <option value="Canton and Enderbury Islands">Canton and Enderbury Islands</option>
                            <option value="Cape Verde">Cape Verde</option>
                            <option value="Cayman Islands">Cayman Islands</option>
                            <option value="Côte d'Ivoire">Côte d'Ivoire</option>
                            <option value="Central African Republic">Central African Republic</option>
                            <option value="Chad">Chad</option>
                            <option value="Chile">Chile</option>
                            <option value="China">China</option>
                            <option value="Christmas Island">Christmas Island</option>
                            <option value="Cocos (Keeling) Islands">Cocos (Keeling) Islands</option>
                            <option value="Colombia">Colombia</option>
                            <option value="Comoros">Comoros</option>
                            <option value="Congo">Congo</option>
                            <option value="Congo, Democratic Republic">Congo, Democratic Republic</option>
                            <option value="Cook Islands">Cook Islands</option>
                            <option value="Costa Rica">Costa Rica</option>
                            <option value="Croatia">Croatia</option>
                            <option value="Cuba">Cuba</option>
                            <option value="Cyprus">Cyprus</option>
                            <option value="Czech Republic">Czech Republic</option>
                            <option value="Denmark">Denmark</option>
                            <option value="Djibouti">Djibouti</option>
                            <option value="Dominica">Dominica</option>
                            <option value="Dominican Republic">Dominican Republic</option>
                            <option value="Dronning Maud Land">Dronning Maud Land</option>
                            <option value="East Timor">East Timor</option>
                            <option value="Ecuador">Ecuador</option>
                            <option value="Egypt">Egypt</option>
                            <option value="El Salvador">El Salvador</option>
                            <option value="Equatorial Guinea">Equatorial Guinea</option>
                            <option value="Eritrea">Eritrea</option>
                            <option value="Estonia">Estonia</option>
                            <option value="Ethiopia">Ethiopia</option>
                            <option value="Faeroe Islands (Føroyar)">Faeroe Islands (Føroyar)</option>
                            <option value="Falkland Islands">Falkland Islands</option>
                            <option value="Fiji">Fiji</option>
                            <option value="Finland">Finland</option>
                            <option value="France">France</option>
                            <option value="French Guiana">French Guiana</option>
                            <option value="French Polynesia">French Polynesia</option>
                            <option value="Gabon">Gabon</option>
                            <option value="Gambia">Gambia</option>
                            <option value="Georgia">Georgia</option>
                            <option value="Germany">Germany</option>
                            <option value="Ghana">Ghana</option>
                            <option value="Gibraltar">Gibraltar</option>
                            <option value="Great Britain">Great Britain</option>
                            <option value="Greece">Greece</option>
                            <option value="Greenland">Greenland</option>
                            <option value="Grenada">Grenada</option>
                            <option value="Guadeloupe">Guadeloupe</option>
                            <option value="Guam">Guam</option>
                            <option value="Guatemala">Guatemala</option>
                            <option value="Guernsey">Guernsey</option>
                            <option value="Guinea">Guinea</option>
                            <option value="Guinea-Bissau">Guinea-Bissau</option>
                            <option value="Guyana">Guyana</option>
                            <option value="Haiti">Haiti</option>
                            <option value="Heard and McDonald Islands">Heard and McDonald Islands</option>
                            <option value="Honduras">Honduras</option>
                            <option value="Hong Kong">Hong Kong</option>
                            <option value="Hungary">Hungary</option>
                            <option value="Iceland">Iceland</option>
                            <option value="India">India</option>
                            <option value="Indonesia">Indonesia</option>
                            <option value="International Monetary Fund">International Monetary Fund</option>
                            <option value="Iran">Iran</option>
                            <option value="Iraq">Iraq</option>
                            <option value="Isle of Man">Isle of Man</option>
                            <option value="Israel">Israel</option>
                            <option value="Italy">Italy</option>
                            <option value="Ivory Coast">Ivory Coast</option>
                            <option value="Jamaica">Jamaica</option>
                            <option value="Japan">Japan</option>
                            <option value="Jersey">Jersey</option>
                            <option value="Johnston Island">Johnston Island</option>
                            <option value="Jordan">Jordan</option>
                            <option value="Kampuchea">Kampuchea</option>
                            <option value="Kazakhstan">Kazakhstan</option>
                            <option value="Kenya">Kenya</option>
                            <option value="Kiribati">Kiribati</option>
                            <option value="Korea, North">Korea, North</option>
                            <option value="Korea, South">Korea, South</option>
                            <option value="Kuwait">Kuwait</option>
                            <option value="Kyrgyzstan">Kyrgyzstan</option>
                            <option value="Laos">Laos</option>
                            <option value="Latvia">Latvia</option>
                            <option value="Lebanon">Lebanon</option>
                            <option value="Lesotho">Lesotho</option>
                            <option value="Liberia">Liberia</option>
                            <option value="Libya">Libya</option>
                            <option value="Liechtenstein">Liechtenstein</option>
                            <option value="Lithuania">Lithuania</option>
                            <option value="Luxembourg">Luxembourg</option>
                            <option value="Macau">Macau</option>
                            <option value="Macedonia (Former Yug. Rep.)">Macedonia (Former Yug. Rep.)</option>
                            <option value="Madagascar">Madagascar</option>
                            <option value="Malawi">Malawi</option>
                            <option value="Malaysia">Malaysia</option>
                            <option value="Maldives">Maldives</option>
                            <option value="Mali">Mali</option>
                            <option value="Malta">Malta</option>
                            <option value="Martinique">Martinique</option>
                            <option value="Mauritania">Mauritania</option>
                            <option value="Mauritius">Mauritius</option>
                            <option value="Mayotte">Mayotte</option>
                            <option value="Mexico">Mexico</option>
                            <option value="Micronesia">Micronesia</option>
                            <option value="Midway Islands">Midway Islands</option>
                            <option value="Moldova">Moldova</option>
                            <option value="Monaco">Monaco</option>
                            <option value="Mongolia">Mongolia</option>
                            <option value="Montenegro">Montenegro</option>
                            <option value="Montserrat">Montserrat</option>
                            <option value="Morocco">Morocco</option>
                            <option value="Mozambique">Mozambique</option>
                            <option value="Myanmar">Myanmar</option>
                            <option value="Namibia">Namibia</option>
                            <option value="Nauru">Nauru</option>
                            <option value="Nepal">Nepal</option>
                            <option value="Netherlands">Netherlands</option>
                            <option value="Netherlands Antilles">Netherlands Antilles</option>
                            <option value="New Caledonia">New Caledonia</option>
                            <option value="Nicaragua">Nicaragua</option>
                            <option value="Niger">Niger</option>
                            <option value="Nigeria">Nigeria</option>
                            <option value="Niue">Niue</option>
                            <option value="Norfolk Island">Norfolk Island</option>
                            <option value="Northern Mariana Islands">Northern Mariana Islands</option>
                            <option value="Norway">Norway</option>
                            <option value="Oman">Oman</option>
                            <option value="Pakistan">Pakistan</option>
                            <option value="Palau">Palau</option>
                            <option value="Panama">Panama</option>
                            <option value="Papua New Guinea">Papua New Guinea</option>
                            <option value="Paraguay">Paraguay</option>
                            <option value="Peru">Peru</option>
                            <option value="Philippines">Philippines</option>
                            <option value="Pitcairn Island">Pitcairn Island</option>
                            <option value="Poland">Poland</option>
                            <option value="Puerto Rico">Puerto Rico</option>
                            <option value="Qatar">Qatar</option>
                            <option value="Reunion">Reunion</option>
                            <option value="Romania">Romania</option>
                            <option value="Russia">Russia</option>
                            <option value="Rwanda">Rwanda</option>
                            <option value="Samoa (America)">Samoa (America)</option>
                            <option value="Samoa (Western)">Samoa (Western)</option>
                            <option value="San Marino">San Marino</option>
                            <option value="Saudi Arabia">Saudi Arabia</option>
                            <option value="São Tomé and Príncipe">São Tomé and Príncipe</option>
                            <option value="Sénégal">Sénégal</option>
                            <option value="Serbia">Serbia</option>
                            <option value="Seychelles">Seychelles</option>
                            <option value="Sierra Leone">Sierra Leone</option>
                            <option value="Singapore">Singapore</option>
                            <option value="Slovakia">Slovakia</option>
                            <option value="Slovenia">Slovenia</option>
                            <option value="Solomon Islands">Solomon Islands</option>
                            <option value="Somalia">Somalia</option>
                            <option value="Spain">Spain</option>
                            <option value="Sri Lanka">Sri Lanka</option>
                            <option value="St. Helena">St. Helena</option>
                            <option value="St. Kitts and Nevis">St. Kitts and Nevis</option>
                            <option value="St. Lucia">St. Lucia</option>
                            <option value="St. Vincent and the Grenadines">St. Vincent and the Grenadines</option>
                            <option value="Sudan">Sudan</option>
                            <option value="Suriname">Suriname</option>
                            <option value="Svalbard and Jan Mayen Islands">Svalbard and Jan Mayen Islands</option>
                            <option value="Swaziland">Swaziland</option>
                            <option value="Sweden">Sweden</option>
                            <option value="Switzerland">Switzerland</option>
                            <option value="Syria">Syria</option>
                            <option value="Tahiti">Tahiti</option>
                            <option value="Taiwan">Taiwan</option>
                            <option value="Tajikistan">Tajikistan</option>
                            <option value="Tanzania">Tanzania</option>
                            <option value="Thailand">Thailand</option>
                            <option value="Timor-Leste">Timor-Leste</option>
                            <option value="Togo">Togo</option>
                            <option value="Trinidad and Tobago">Trinidad and Tobago</option>
                            <option value="Tunisia">Tunisia</option>
                            <option value="Turkey">Turkey</option>
                            <option value="Turkmenistan">Turkmenistan</option>
                            <option value="Turks and Caicos Islands">Turks and Caicos Islands</option>
                            <option value="Tuvalu">Tuvalu</option>
                            <option value="Uganda">Uganda</option>
                            <option value="Ukraine">Ukraine</option>
                            <option value="United Arab Emirates">United Arab Emirates</option>
                            <option value="Upper Volta">Upper Volta</option>
                            <option value="Uruguay">Uruguay</option>
                            <option value="Uzbekistan">Uzbekistan</option>
                            <option value="Vanuatu">Vanuatu</option>
                            <option value="Vatican">Vatican</option>
                            <option value="Venezuela">Venezuela</option>
                            <option value="Vietnam">Vietnam</option>
                            <option value="Virgin Islands">Virgin Islands</option>
                            <option value="Wake Island">Wake Island</option>
                            <option value="Wallis and Futuna Islands">Wallis and Futuna Islands</option>
                            <option value="Western Sahara">Western Sahara</option>
                            <option value="Western Samoa">Western Samoa</option>
                            <option value="Yemen">Yemen</option>
                            <option value="Zaïre">Zaïre</option>
                            <option value="Zambia">Zambia</option>
                            <option value="Zimbabwe">Zimbabwe</option>
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
                        <input class="text" name="company[primary_contact_information][name]" type="text" tabindex="7" value="${out_none value=company.primary_contact_information.name /}" />
                    </div>
                </div>
                <div class="form-field">
                    <label>Email:</label>
                    <div>
                        <input class="text" name="company[primary_contact_information][email]" type="text" tabindex="9" value="${out_none value=company.primary_contact_information.email /}" />
                    </div>
                </div>
                <div class="form-field">
                    <label>Website:</label>
                    <div>
                        <input class="text" name="company[primary_contact_information][website]" type="text" tabindex="11" value="${out_none value=company.primary_contact_information.website /}" />
                    </div>
                </div>
            </div>
            <div class="column-second">
                <div class="form-field">
                    <label>Telefone:</label>
                    <input class="text" name="company[primary_contact_information][phone_number]" type="text" tabindex="8" value="${out_none value=company.primary_contact_information.phone_number /}" />
                </div>
                <div class="form-field">
                    <label>Fax:</label>
                    <input class="text" name="company[primary_contact_information][fax_number]" type="text" tabindex="10" value="${out_none value=company.primary_contact_information.fax_number /}" />
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
