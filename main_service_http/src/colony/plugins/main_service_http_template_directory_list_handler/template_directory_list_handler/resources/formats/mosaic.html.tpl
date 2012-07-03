<div class="mosaic-view">
    ${foreach item=directory_entry from=directory_entries}
        <div class="item ${out_none value=directory_entry.type xml_escape=True /}-large">
            <p class="name">
                <a href="${out_none value=directory_entry.name quote=True xml_escape=True /}">${out_none value=directory_entry.name xml_escape=True /}</a>
            </p>
            <p class="description">${out_none value=directory_entry.type xml_escape=True /}</p>
            <p class="description">${out_none value=directory_entry.size_string xml_escape=True /}</p>
        </div>
    ${/foreach}
</div>
