<html>
    <body>
        <h1>${out value=scaffold_attributes.model.name /}</h1>
        <table>
            <thead>
                <th>
                    name
                </th>
                <th>
                    value
                </th>
            </thead>
            <tbody>
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
            </tbody>
        </table>
    </body>
</html>
