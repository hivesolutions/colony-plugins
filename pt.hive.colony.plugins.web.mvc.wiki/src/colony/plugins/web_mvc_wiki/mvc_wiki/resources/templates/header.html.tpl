<div id="wiki-header">
    <div class="wiki-header-contents">
        <div class="logo-image">
            <a href="${out_none value=base_path /}${out_none value=instance_name /}/${out_none value=main_page /}"><img src="${out_none value=base_path /}${out_none value=instance_name /}/${out_none value=logo_path /}"/></a>
        </div>
        <div class="menu-contents">
            <ul>
                <li class="menu">
                    <a href="${out_none value=base_path /}${out_none value=instance_name /}/${out_none value=main_page /}">Home</a>
                </li>
                <li class="menu menu-index">
                    <a id="index-opener" href="#" onclick="switchMenu(); return false;">Index</a>
                    <div id="index" style="opacity: 0.0;visibility: hidden;">
                        <hr/>
                        <dl>
                            ${foreach item=instance_configuration_item from=instance_configuration_index}
                                <dt>${out_none value=instance_configuration_item.name /}</dt>
                                ${foreach item=instance_configuration_item_item from=instance_configuration_item.items}
                                    <dd>
                                        <a href="${out_none value=instance_configuration_item_item.link /}">${out_none value=instance_configuration_item_item.name /}</a>
                                    </dd>
                                ${/foreach}
                            ${/foreach}
                        </dl>
                    </div>
                </li>
                ${foreach item=header_link from=header_links}
                    <li class="menu">
                        <a href="${out_none value=base_path /}${out_none value=instance_name /}/${out_none value=header_link.address /}">${out_none value=header_link.name /}</a>
                    </li>
                ${/foreach}
                <li>
                    <input id="wiki-page-search" name="wiki-page-search" class="wiki-input" type="text" value="Search" current_status="" original_value="Search" />
                </li>
            </ul>
        </div>
    </div>
</div>
<div id="environment-variables">
    <div id="base-path">${out_none value=base_path xml_escape=True /}</div>
</div>
