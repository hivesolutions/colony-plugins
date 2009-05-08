-- 200905070000

-- marks all products that have subproduct as not sellable, and all others as sellable

UPDATE Product SET sellable = 1;
UPDATE SubProduct SET sellable = 1;

UPDATE Product
   SET sellable = 0
 WHERE object_id IN (
       -- ERROR: sellable products with children
       SELECT object_id
         FROM Product
        WHERE object_id IN (
              -- the products with children
              SELECT t.parent_tree_node_object_id
                FROM TreeNodeTreeNodeRelation t
               WHERE t.child_tree_node_object_id IS NOT NULL)
          AND sellable = 1);
