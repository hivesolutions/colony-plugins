${if item=options_enabled value=True operator=eq}
    <div id="wiki-contents-header">
        <div class="wiki-float-left">
            <span class="wiki-contents-title">${out_none value=page_name /}</span>
        </div>
        <div class="wiki-float-right">
            <a class="wiki-contents-action">Read</a>
            <a class="wiki-contents-action">Edit</a>
            ${if item=print_enabled value=True operator=eq}
                <a href="${out_none value=base_path /}${out_none value=instance_name /}/${out_none value=page_name /}.prt" class="wiki-contents-action">Print</a>
            ${/if}
            <a class="wiki-contents-action">View History</a>
        </div>
        <div class="wiki-clear"></div>
    </div>
${/if}
