-- sale transaction and purchase transaction calculated prices/costs were being having manually assigned object_ids that were conflicting with others
-- removing them and recalculating them removes the inconsistency (this step takes care of removing them, the migration has a post process for this recalculation)

DELETE FROM Price
 WHERE object_id IN (
      SELECT p.object_id
        FROM Price p, SaleTransaction s
       WHERE p.object_id = s.price);

DELETE FROM Cost
 WHERE object_id IN (
      SELECT c.object_id
        FROM Cost c, PurchaseTransaction s
       WHERE c.object_id = s.cost);

UPDATE SaleTransaction SET price = NULL;
UPDATE PurchaseTransaction SET cost = NULL;
