<div id="partial-contents">
    <table id="table">
        <tbody id="table-body">
        ${foreach item=root_entity from=root_entities}
        <tr>
            <td>
                <a href="plugins#root_entities/${out value=root_entity.object_id /}/delete">${out value=root_entity.description xml_escape=True /}</a>
            </td>
        </tr>
        ${/foreach}
        </tbody>
    </table>
    <div id="meta-data">
        <div id="start-record">${out value=start_record /}</div>
        <div id="number-records">${out value=number_records /}</div>
        <div id="total-number-records">${out value=total_number_records /}</div>
    </div>
</div>
