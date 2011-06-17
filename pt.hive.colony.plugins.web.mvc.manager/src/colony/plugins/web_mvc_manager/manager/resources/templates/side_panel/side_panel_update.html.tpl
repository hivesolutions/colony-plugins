<div id="icon-bar" class="brown">
    <div id="content-icon">
        <img src="${out_none value=base_path /}resources/images/icon/icon-omni.png" height="32" width="32" alt="Bill"/>
    </div>
</div>
<div id="left-column">
    <h1 id="assistants">Assistants</h1>
    <ul id="assistants">
    </ul>
    <h1 id="lists">Lists</h1>
    <ul id="lists">
    </ul>
    ${foreach item=panel_item from=panel_items}
        ${out_none value=panel_item /}
    ${/foreach}
</div>
