<html>
    <body>
        <h1>Root Entity</h1>
        <form action="update" method="post">
            <table border="1">
                <thead>
                    <th>
                    attribute
                    </th>
                    <th>
                    value
                    </th>
                </thead>
                <tbody>
                    <tr>
                        <td>
                            object_id
                        </td>
                        <td>
                            ${out value=root_entity.object_id /}
                        </td>
                    </tr>
                    <tr>
                        <td>
                            description
                        </td>
                        <td>
                            <input name="root_entity[description]" value="${out value=root_entity.description /}" />
                        </td>
                    </tr>
                    <tr>
                        <td colspan="2">
                            <input type="submit" value="update" />
                        </td>
                    </tr>
                </tbody>
            </table>
        </form>
    </body>
</html>
