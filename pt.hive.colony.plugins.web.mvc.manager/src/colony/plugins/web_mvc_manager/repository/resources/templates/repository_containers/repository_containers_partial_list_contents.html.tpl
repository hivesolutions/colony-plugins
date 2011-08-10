<div id="partial-contents">
    <table id="table">
        <tbody id="table-body">
            ${foreach item=repository_container from=repository_containers}
                <tr>
                    <td>
                        <a href="#containers/${out_none value=repository_container.id xml_escape=True /}">${out_none value=repository_container.id xml_escape=True /}</a>
                    </td>
                    <td>
                        ${if item=repository_container.status value="not_installed" operator=eq}
                            <div class="submit button button-green"
                                 data-container_id="${out_none value=repository_container.id xml_escape=True /}"
                                 data-container_version="${out_none value=repository_container.version xml_escape=True /}"
                                 data-container_status="${out_none value=repository_container.status xml_escape=True /}">
                                Install
                            </div>
                        ${elif item=repository_container.status value="newer_version" operator=eq /}
                            <div class="submit button button-green"
                                 data-container_id="${out_none value=repository_container.id xml_escape=True /}"
                                 data-container_version="${out_none value=repository_container.version xml_escape=True /}"
                                 data-container_status="${out_none value=repository_container.status xml_escape=True /}">
                                Upgrade
                            </div>
                        ${elif item=repository_container.status value="older_version" operator=eq /}
                            <div class="submit button button-gray"
                                 data-container_id="${out_none value=repository_container.id xml_escape=True /}"
                                 data-container_version="${out_none value=repository_container.version xml_escape=True /}"
                                 data-container_status="${out_none value=repository_container.status xml_escape=True /}">
                                Older Version
                            </div>
                        ${elif item=repository_container.status value="same_version" operator=eq /}
                            <div class="submit button button-gray"
                                 data-container_id="${out_none value=repository_container.id xml_escape=True /}"
                                 data-container_version="${out_none value=repository_container.version xml_escape=True /}"
                                 data-container_status="${out_none value=repository_container.status xml_escape=True /}">
                                Remove
                            </div>
                        ${elif item=repository_container.status value="different_digest" operator=eq /}
                            <div class="submit button button-blue"
                                 data-container_id="${out_none value=repository_container.id xml_escape=True /}"
                                 data-container_version="${out_none value=repository_container.version xml_escape=True /}"
                                 data-container_status="${out_none value=repository_container.status xml_escape=True /}">
                                Upgrade
                            </div>
                        ${/if}
                    </td>
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
