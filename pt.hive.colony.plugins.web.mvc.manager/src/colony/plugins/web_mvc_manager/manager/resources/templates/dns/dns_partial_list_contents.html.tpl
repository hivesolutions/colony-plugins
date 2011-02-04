<div id="partial-contents">
    <table id="table">
        <tbody id="table-body">
            ${foreach item=dns_zone index=dns_zone_index from=dns_zones}
                <tr>
                    <td>
                        <a href="#dns/${out_none value=dns_zone_index xml_escape=True /}">${out_none value=dns_zone.name xml_escape=True /}</a>
                    </td>
                    <td>${out_none value=dns_zone.description xml_escape=True /}</td>
                    <td>${out_none value=dns_zone.layout xml_escape=True /}</td>
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
