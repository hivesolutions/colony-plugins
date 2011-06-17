<div id="partial-contents">
    <table id="table">
        <tbody id="table-body">
            ${foreach item=capability from=capabilities}
                <tr>
                    <td>
                        <a href="#capabilities/${out_none value=capability xml_escape=True /}">${out_none value=capability xml_escape=True /}</a>
                    </td>
                    <td>0</td>
                </tr>
            ${/foreach}
        </tbody>
    </table>
    <div id="meta-data">
        <div id="start-record">${out value=start_record xml_escape=True /}</div>
        <div id="number-records">${out value=number_records xml_escape=True /}</div>
        <div id="total-number-records">${out value=total_number_records xml_escape=True /}</div>
    </div>
</div>
