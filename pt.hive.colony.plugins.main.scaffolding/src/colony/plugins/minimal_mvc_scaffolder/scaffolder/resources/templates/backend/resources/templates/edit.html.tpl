<html>
    <body>
        <h1>${out value=scaffold_attributes.model.name /}</h1>
        <form action="$\{out_none value=base_path /}${out value=scaffold_attributes.model.variable_name_plural /}/$\{out value=${out value=scaffold_attributes.model.variable_name /}.object_id /}/update" method="post">
            <table>
                <tr>
                    <th>name</th>
                    <th>value</th>
                </tr>
                ${foreach item=attribute from=scaffold_attributes.model.attributes}
                    <tr>
                        <td>${out value=attribute.name /}</td>
                        <td><input name="${out value=scaffold_attributes.model.variable_name /}[${out value=attribute.name /}]" value="$\{out value=${out value=scaffold_attributes.model.variable_name /}.${out value=attribute.name /} /}" /></td>
                    </tr>
                ${/foreach}
            </table>
            <p><input type="submit" value="update" /></p>
        </form>
    </body>
</html>
