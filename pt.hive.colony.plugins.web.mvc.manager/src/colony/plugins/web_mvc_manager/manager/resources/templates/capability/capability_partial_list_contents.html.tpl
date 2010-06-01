<tbody id="company-table-body">
${foreach item=company from=companies_page.companies}
<tr>
    <td><a href="#companies/${out_none value=company.object_id xml_escape=True /}">${out_none value=company.name xml_escape=True /}</a></td>
    <td>${out_none value=company.fiscal_id xml_escape=True /}</td>
    <td>${out_none value=company.primary_contact_information.address xml_escape=True /}</td>
    <td>${out_none value=company.last_invoice_issue_date xml_escape=True /}</td>
    <td>${out_none value=company.next_invoice_due_date xml_escape=True /}</td>
</tr>
${/foreach}
</tbody>
<div id="start-record">${out value=companies_page.start_record xml_escape=True /}</div>
<div id="end-record">${out value=companies_page.end_record xml_escape=True /}</div>
<div id="number-records">${out value=companies_page.number_records xml_escape=True /}</div>
<div id="previous-start-record">${out value=companies_page.previous_start_record xml_escape=True /}</div>
<div id="next-start-record">${out value=companies_page.next_start_record xml_escape=True /}</div>
<div id="total-number-records">${out value=companies_page.total_number_records xml_escape=True /}</div>
