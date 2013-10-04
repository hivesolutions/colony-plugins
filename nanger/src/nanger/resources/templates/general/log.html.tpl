<div class="log">
    ${foreach item=line from=latest}
        <div class="line">${out_none value=line xml_escape=True /}</div>
    ${/foreach}
</div>
