<html>
    <body>
        <h1>${out value=scaffold_attributes.model.name /}</h1>
        <form method="post">
            <table>
                <thead>
                    <th>attribute</th>
                    <th>value</th>
                </thead>
                <tbody>
                    ${foreach item=attribute from=scaffold_attributes.model.attributes}
                        <tr>
                            <td>${out value=attribute.name /}
                            </td>
                            <td><input name="${out value=scaffold_attributes.model.variable_name /}[${out value=attribute.name /}]" /></td>
                        </tr>
                    ${/foreach}
                </tbody>
            </table>
            <p><input type="submit" value="create" /></p>
        </form>
    </body>
</html>
