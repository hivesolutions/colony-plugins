<html>
    <body>
        <h1>Root Entity</h1>
        <form action="root_entities/new" method="get">
            <table border="1">
                <thead>
                    <th>
                    object_id
                    </th>
                    <th>
                    description
                    </th>
                    <th>
                    action
                    </th>
                </thead>
                <tbody>
                       ${foreach item=root_entity from=root_entities}
                        <tr>
                            <td>
                            ${out value=root_entity.object_id /}
                            </td>
                            <td>
                            ${out value=root_entity.description /}
                            </td>
                            <td>
                                <a href="root_entities/${out value=root_entity.object_id /}">Show</a>
                                <a href="root_entities/${out value=root_entity.object_id /}/update">Update</a>
                                <a href="root_entities/${out value=root_entity.object_id /}/delete">Delete</a>
                            </td>
                        </tr>
                    ${/foreach}
                    <tr>
                        <td colspan="3" align="right">
                            <input type="submit" value="create" />
                        </td>
                    </tr>
                </tbody>
            </table>
        </form>
    </body>
</html>
