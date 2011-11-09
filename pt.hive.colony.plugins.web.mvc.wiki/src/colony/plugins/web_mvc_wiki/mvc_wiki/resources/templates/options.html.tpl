${if item=options_enabled value=True operator=eq}
    <div id="wiki-contents-header">
        <div class="wiki-float-left">
            <span class="wiki-contents-title">${out_none value=page_name /}</span>
        </div>
        ${if item=section value="new" operator=neq}
            <div class="wiki-float-right">
                ${if item=section value="show" operator=eq}
                    <a href="${out_none value=base_path /}${out_none value=instance_name /}/pages/${out_none value=page_name /}" class="wiki-contents-action active">Read</a>
                ${else /}
                    <a href="${out_none value=base_path /}${out_none value=instance_name /}/pages/${out_none value=page_name /}" class="wiki-contents-action">Read</a>
                ${/if}
                ${if item=section value="edit" operator=eq}
                    <a href="${out_none value=base_path /}${out_none value=instance_name /}/pages/${out_none value=page_name /}/edit" class="wiki-contents-action active">Edit</a>
                ${else /}
                    <a href="${out_none value=base_path /}${out_none value=instance_name /}/pages/${out_none value=page_name /}/edit" class="wiki-contents-action">Edit</a>
                ${/if}
                ${if item=section value="history" operator=eq}
                    <a href="#" class="wiki-contents-action active">History</a>
                ${else /}
                    <a href="#" class="wiki-contents-action">History</a>
                ${/if}
                ${if item=print_enabled value=True operator=eq}
                    <a href="${out_none value=base_path /}${out_none value=instance_name /}/${out_none value=page_name /}.prt" class="wiki-contents-action">Print</a>
                ${/if}
            </div>
        ${/if}
        <div class="wiki-clear"></div>
    </div>
${/if}
