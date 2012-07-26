<div class="links sub-links">
    ${if item=sub_area value="info" operator=eq}
        <a href="${out_none value=base_path /}plugins/${out_none value=plugin.short_name /}" class="active">info</a>
    ${else /}
        <a href="${out_none value=base_path /}plugins/${out_none value=plugin.short_name /}">info</a>
    ${/if}
    //
    ${if item=plugin.loaded value=True operator=eq}
        ${if item=sub_area value="reload" operator=eq}
            <a href="${out_none value=base_path /}plugins/${out_none value=plugin.short_name /}/reload" class="active">reload</a>
        ${else /}
            <a href="${out_none value=base_path /}plugins/${out_none value=plugin.short_name /}/reload">reload</a>
        ${/if}
        //
          ${if item=sub_area value="unload" operator=eq}
            <a href="${out_none value=base_path /}plugins/${out_none value=plugin.short_name /}/unload" class="active">unload</a>
        ${else /}
            <a href="${out_none value=base_path /}plugins/${out_none value=plugin.short_name /}/unload">unload</a>
        ${/if}
    ${else /}
          ${if item=sub_area value="load" operator=eq}
            <a href="${out_none value=base_path /}plugins/${out_none value=plugin.short_name /}/load" class="active">load</a>
        ${else /}
            <a href="${out_none value=base_path /}plugins/${out_none value=plugin.short_name /}/load">load</a>
        ${/if}
    ${/if}
</div>
