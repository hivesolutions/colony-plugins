<tr>
    <td class="label light-blue">Memory</td>
    <td class="value ${if item=memory_usage value=100 operator=lt}green${/if}${if item=memory_usage value=100 operator=gte}red${/if}">${out_none value=memory_usage xml_escape=True /}M</td>
</tr>
<tr class="section-end">
    <td class="label light-blue">CPU</td>
    <td class="value ${if item=cpu_usage value=50 operator=lt}green${/if}${if item=cpu_usage value=50 operator=gte}red${/if}">${out_none value=cpu_usage xml_escape=True /}%</td>
</tr>
