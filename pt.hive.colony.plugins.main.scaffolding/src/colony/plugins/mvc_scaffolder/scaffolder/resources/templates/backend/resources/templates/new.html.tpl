<html>
    <body>
        <h1>${out value=scaffold_attributes.model.name /}</h1>
        <form action="$\{out_none value=base_path /}${out value=scaffold_attributes.model.variable_name_plural /}" method="post">
            <table>
                <tr>
                    <th>
                        attribute
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
                            <input name="${out value=scaffold_attributes.model.variable_name /}[${out value=attribute.name /}]" />
                        </td>
                    </tr>
                ${/foreach}
            </table>
            <p>
                <input type="submit" value="create" />
            </p>
        </form>
    </body>
</html>
