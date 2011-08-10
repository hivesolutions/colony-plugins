<div id="partial-contents">
    <table id="table">
        <tbody id="table-body">
            ${foreach item=repository_bundle from=repository_bundles}
                <tr>
                    <td>
                        <a href="#bundles/${out_none value=repository_bundle.id xml_escape=True /}">${out_none value=repository_bundle.id xml_escape=True /}</a>
                    </td>
                    <td>
                        ${if item=repository_bundle.status value="not_installed" operator=eq}
                            <div class="submit button button-green"
                                 data-bundle_id="${out_none value=repository_bundle.id xml_escape=True /}"
                                 data-bundle_version="${out_none value=repository_bundle.version xml_escape=True /}"
                                 data-bundle_status="${out_none value=repository_bundle.status xml_escape=True /}">
                                Install
                            </div>
                        ${elif item=repository_bundle.status value="newer_version" operator=eq /}
                            <div class="submit button button-green"
                                 data-bundle_id="${out_none value=repository_bundle.id xml_escape=True /}"
                                 data-bundle_version="${out_none value=repository_bundle.version xml_escape=True /}"
                                 data-bundle_status="${out_none value=repository_bundle.status xml_escape=True /}">
                                Upgrade
                            </div>
                        ${elif item=repository_bundle.status value="older_version" operator=eq /}
                            <div class="submit button button-gray"
                                 data-bundle_id="${out_none value=repository_bundle.id xml_escape=True /}"
                                 data-bundle_version="${out_none value=repository_bundle.version xml_escape=True /}"
                                 data-bundle_status="${out_none value=repository_bundle.status xml_escape=True /}">
                                Older Version
                            </div>
                        ${elif item=repository_bundle.status value="same_version" operator=eq /}
                            <div class="submit button button-gray"
                                 data-bundle_id="${out_none value=repository_bundle.id xml_escape=True /}"
                                 data-bundle_version="${out_none value=repository_bundle.version xml_escape=True /}"
                                 data-bundle_status="${out_none value=repository_bundle.status xml_escape=True /}">
                                Remove
                            </div>
                        ${elif item=repository_bundle.status value="different_digest" operator=eq /}
                            <div class="submit button button-blue"
                                 data-bundle_id="${out_none value=repository_bundle.id xml_escape=True /}"
                                 data-bundle_version="${out_none value=repository_bundle.version xml_escape=True /}"
                                 data-bundle_status="${out_none value=repository_bundle.status xml_escape=True /}">
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
