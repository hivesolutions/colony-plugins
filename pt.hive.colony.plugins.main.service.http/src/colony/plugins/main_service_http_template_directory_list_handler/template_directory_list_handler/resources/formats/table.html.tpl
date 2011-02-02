<div class="table-view">
    <table cellspacing="0">
        <thead>
            <tr>
                <th class="column name"><a href="?comparator=name&sort=${out_none value=sort_orders.name xml_escape=True /}">Name</a></th>
                <th class="column date"><a href="?comparator=modified_date&sort=${out_none value=sort_orders.modified_date xml_escape=True /}">Modified Date</a></th>
                <th class="column size"><a href="?comparator=size&sort=${out_none value=sort_orders.size xml_escape=True /}">Size</a></th>
            </tr>
        </thead>
        <tbody>
            ${foreach item=directory_entry from=directory_entries}
                <tr>
                    <td class="name ${out_none value=directory_entry.type xml_escape=True /}-small">
                        <a href="${out_none value=directory_entry.name quote=True xml_escape=True /}">${out_none value=directory_entry.name xml_escape=True /}</a>
                    </td>
                    <td class="date">${format_datetime value=directory_entry.modified_date format="%d/%m/%y %H:%M:%S" xml_escape=True /}</td>
                    <td class="size">${out_none value=directory_entry.size_string xml_escape=True /}</td>
                </tr>
            ${/foreach}
        </tbody>
        <tfoot></tfoot>
    </table>
</div>
