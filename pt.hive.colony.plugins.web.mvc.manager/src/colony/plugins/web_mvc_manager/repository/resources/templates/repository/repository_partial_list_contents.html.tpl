<div id="partial-contents">
    <table id="table">
        <tbody id="table-body">
            ${foreach item=repository index=repository_index from=repositories}
                <tr>
                    <td>
                        <a href="#repositories/${out_none value=repository_index xml_escape=True /}">${out_none value=repository.name xml_escape=True /}</a>
                    </td>
                    <td>${out_none value=repository.description xml_escape=True /}</td>
                    <td>${out_none value=repository.layout xml_escape=True /}</td>
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
