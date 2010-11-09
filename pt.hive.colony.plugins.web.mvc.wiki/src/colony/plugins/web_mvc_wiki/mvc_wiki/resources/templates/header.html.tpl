<div id="wiki-header">
    <div class="wiki-header-contents">
        <div class="logo-image">
            <a href="${out_none value=base_path /}index"><img src="${out_none value=base_path /}images/colony_logo.png"/></a>
        </div>
        <div class="menu-contents">
            <ul>
                <li class="menu"><a href="${out_none value=base_path /}index">Home</a></li>
                <li class="menu menu-index"><a id="index-opener" href="#" onclick="switchMenu(); return false;">Index</a></li>
                <li class="menu"><a href="documentation_how_can_i_help.html">Contribute</a></li>
                <li class="menu"><a href="documentation_credits.html">Credits</a></li>
                <li class="menu"><a id="wiki-more-button" href="#">More</a></li>
            </ul>
        </div>
    </div>
</div>
<div id="wiki-sub-header">
    <div id="wiki-sub-header-contents">
        <div id="wiki-sub-header-left">
            <h1 id="wiki-page-title">${out_none value=page_name /}</h1>
        </div>
        <div id="wiki-sub-header-right">
            <div class="wiki-float-left">
                <div id="wiki-page-edit-button" class="wiki-button wiki-button-blue">Edit</div>
            </div>
            <div id="wiki-page-search-container" class="wiki-float-left">
                <input id="wiki-page-search" name="wiki-page-search" class="wiki-input" type="text" value="Search" current_status="" original_value="Search" />
                <div id="wiki-page-search-background"></div>
            </div>
        </div>
    </div>
</div>
<div id="wiki-page-edit-container">
    <div id="wiki-page-edit">
        <div class="wiki-page-edit-line">
            <input id="wiki-summary-input" name="wiki-summary-input" class="wiki-input" type="text" value="Describe your wiki modification" current_status="" original_value="Describe your wiki modification" />
        </div>
        <div class="wiki-page-edit-line">
            <div id="wiki-controls">
                <div id="wiki-controls-icons">
                    <div class="wiki-control-icon wiki-control-icon-bold"></div>
                    <div class="wiki-control-icon wiki-control-icon-italic"></div>
                    <div class="wiki-control-icon wiki-control-icon-quote"></div>
                </div>
            </div>
            <textarea id="wiki-page-contents-text-area" class="wiki-text-area">${out_none value=page_source /}</textarea>
        </div>
        <div id="wiki-page-edit-buttons" class="wiki-page-edit-line">
            <div id="wiki-publish-button" class="wiki-button wiki-button-blue">Publish</div>
            <div class="wiki-button wiki-button-blue disabled">Preview</div>
        </div>
    </div>
</div>
<div id="environment-variables">
    <div id="base-path">${out_none value=base_path xml_escape=True /}</div>
</div>
