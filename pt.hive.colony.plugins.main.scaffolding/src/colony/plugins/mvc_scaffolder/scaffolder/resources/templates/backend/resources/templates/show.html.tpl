<html>
    <body>
        <h1>${out value=scaffold_attributes.model.name /}</h1>
        <table>
            <tr>
                <th>
                    name
                </th>
                <th>
                    value
                </th>
            </tr>
            ${foreach item=attribute from=scaffold_attributes.model.attributes}
                <tr>
                    <td>
                        ${out value=attribute.name /}
                    </td>
                    <td>
                        $\{out value=${out value=scaffold_attributes.model.variable_name /}.${out value=attribute.name /} /}
                    </td>
                </tr>
            ${/foreach}
        </table>
    </body>
</html>
