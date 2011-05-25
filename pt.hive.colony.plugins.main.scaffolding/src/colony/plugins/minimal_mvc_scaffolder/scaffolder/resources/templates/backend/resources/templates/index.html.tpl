<html>
    <body>
        <form action="root_entities.json" method="post">
            <input type="text" name="root_entity[description]" />
            <input type="submit" value="create" />
        </form>
        ${foreach item=root_entity from=root_entities}
        <li>
            <a href="root_entities/${out value=root_entity.object_id /}.json">${out value=root_entity.object_id /} - ${out value=root_entity.description /}</a>
            <a href="root_entities/${out value=root_entity.object_id /}/delete.json">delete</a>
        </li>
        ${/foreach}
    </body>
</html>
