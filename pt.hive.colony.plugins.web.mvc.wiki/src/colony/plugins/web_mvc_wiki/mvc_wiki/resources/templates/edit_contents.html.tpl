<div id="wiki-page-edit-container">
    <div id="wiki-page-edit">
        <form action="update" id="wiki-page-edit-form" method="post">
            <input name="page[name]" type="hidden" value="${out_none value=page_name /}" />
            <div class="wiki-page-edit-line">
                <div class="warning">For help regarding the wiki syntax please refer to <a href="${out_none value=base_path /}${out_none value=instance_name /}/documentation_demo.html">reference</a>.</div>
            </div>
            <div class="wiki-page-edit-line">
                <div id="wiki-controls">
                    <div id="wiki-controls-icons">
                        <div class="wiki-control-icon wiki-control-icon-bold"></div>
                        <div class="wiki-control-icon wiki-control-icon-italic"></div>
                        <div class="wiki-control-icon wiki-control-icon-quote"></div>
                    </div>
                </div>
                <textarea id="wiki-page-edit-contents-text-area" name="page[contents]" class="wiki-text-area">${out_none value=page_source /}</textarea>
            </div>
            <div class="wiki-page-edit-line">
                <input id="wiki-page-edit-summary-input" name="page[summary]" class="wiki-input" type="text" value="Describe your change" current_status="" original_value="Describe your change" />
            </div>
            <div id="wiki-page-edit-buttons" class="wiki-page-edit-line">
                <div id="wiki-page-edit-publish-button" class="wiki-button wiki-button-blue">Save Page</div>
                <div id="wiki-page-edit-preview-button" class="wiki-button wiki-button-blue">Show Preview</div>
            </div>
        </form>
    </div>
</div>
${if item=page_contents value=None operator=neq}
    <div class="wiki-separator"></div>
    <div id="wiki-preview">
        ${out_none value=page_contents /}
    </div>
${/if}
