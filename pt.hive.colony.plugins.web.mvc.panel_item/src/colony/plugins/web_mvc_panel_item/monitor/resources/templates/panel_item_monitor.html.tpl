<h1 id="status">Monitor</h1>
<div class="widget-table">
    <table>
        ${foreach item=monitor_item from=monitor_items}
            ${out_none value=monitor_item /}
        ${/foreach}
    </table>
</div>
