<div id="wiki-page-new-container">
    <div id="wiki-page-new">
        <form action="pages" id="wiki-page-new-form" method="post">
            <input name="page[name]" type="hidden" value="${out_none value=page_name /}" />
            <div class="wiki-page-new-line">
                   <div class="error">This page does not exist yet. Please make sure no similar pages exist before creating it.</div>
            </div>
            <div class="wiki-page-new-line">
                <div class="warning">For help regarding the wiki syntax please refer to <a href="documentation_demo.html">reference</a>.</div>
            </div>
            <div class="wiki-page-new-line">
                <div id="wiki-controls">
                    <div id="wiki-controls-icons">
                        <div class="wiki-control-icon wiki-control-icon-bold"></div>
                        <div class="wiki-control-icon wiki-control-icon-italic"></div>
                        <div class="wiki-control-icon wiki-control-icon-quote"></div>
                    </div>
                </div>
                <textarea id="wiki-page-new-contents-text-area" name="page[contents]" class="wiki-text-area">${out_none value=page_source /}</textarea>
            </div>
            <div class="wiki-page-new-line">
                <input id="wiki-page-new-summary-input" name="page[summary]" class="wiki-input" type="text" value="Describe your new page" current_status="" original_value="Describe your new page" />
            </div>
            <div id="wiki-page-new-buttons" class="wiki-page-new-line">
                <div id="wiki-page-new-publish-button" class="wiki-button wiki-button-blue">Publish</div>
                <div class="wiki-button wiki-button-blue disabled">Preview</div>
            </div>
        </form>
    </div>
</div>
