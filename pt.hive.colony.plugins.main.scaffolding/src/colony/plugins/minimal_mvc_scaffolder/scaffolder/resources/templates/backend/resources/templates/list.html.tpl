<html>
    <head>
        <script type="text/javascript" src="$\{out_none value=base_path /}resources/js/main.js"></script>
    </head>
    <body>
        <h1>${out value=scaffold_attributes.model.name /}</h1>
        <table>
            <tr>
                ${foreach item=attribute from=scaffold_attributes.model.attributes}
                    <th>${out value=attribute.name /}
                    </th>
                ${/foreach}
                <th>action</th>
            </tr>
            $\{foreach item=${out value=scaffold_attributes.model.variable_name /} from=${out value=scaffold_attributes.model.variable_name_plural /}}
                <tr>
                    ${foreach item=attribute from=scaffold_attributes.model.attributes}
                        <td>$\{out value=${out value=scaffold_attributes.model.variable_name /}.${out value=attribute.name /} /}</td>
                    ${/foreach}
                    <td>
                        <a href="$\{out_none value=base_path /}${out value=scaffold_attributes.model.variable_name_plural /}/$\{out value=${out value=scaffold_attributes.model.variable_name /}.object_id /}">show</a>
                        <a href="$\{out_none value=base_path /}${out value=scaffold_attributes.model.variable_name_plural /}/$\{out value=${out value=scaffold_attributes.model.variable_name /}.object_id /}/edit">edit</a>
                        <a name="delete" href="$\{out_none value=base_path /}${out value=scaffold_attributes.model.variable_name_plural /}/$\{out value=${out value=scaffold_attributes.model.variable_name /}.object_id /}/delete">delete</a>
                    </td>
                </tr>
            $\{/foreach}
        </table>
        <p><a href="${out value=scaffold_attributes.model.variable_name_plural /}/new">create</a></p>
        <form id="post-form" style="visibility:hidden;" method="post"></form>
    </body>
</html>
