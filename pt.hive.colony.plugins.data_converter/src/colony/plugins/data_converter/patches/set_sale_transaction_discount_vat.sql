-- 200905070000

-- recalculates the discount with vat using the discount and an estimated vat rate due
-- to wrong values in the internal structure (discount vat was being interpreted as "vat accrue on the discount")

BEGIN TRANSACTION;

-- update 20% VAT transactions
UPDATE SaleTransaction
   SET discount_vat = round(discount * 1.2, 2)
 WHERE object_id IN (
       -- 20% VAT sales
       SELECT s.object_id
         FROM SaleTransaction s, Price p
        WHERE s.price = p.object_id
          AND round(s.vat / p.value , 2) = 0.20);

-- update 21% VAT transactions
UPDATE SaleTransaction
   SET discount_vat = round(discount * 1.21, 2)
 WHERE object_id IN (
       -- 20% VAT sales
       SELECT s.object_id
         FROM SaleTransaction s, Price p
        WHERE s.price = p.object_id
          AND round(s.vat / p.value , 2) = 0.21);

-- update 14% VAT transaction
UPDATE SaleTransaction
   SET discount_vat = round(discount * 1.14, 2)
 WHERE object_id IN (
       -- 20% VAT sales
       SELECT s.object_id
         FROM SaleTransaction s, Price p
        WHERE s.price = p.object_id
          AND round(s.vat / p.value , 2) = 0.14);

-- recalculates the unit discount vat in sale lines, using the unit discount and the previous discount vat (which was incorrectly being populated
-- with the vat accrued on the discount)

UPDATE SaleMerchandiseHierarchyTreeNode
   SET unit_discount_vat = unit_discount + unit_discount_vat;

UPDATE PurchaseMerchandiseHierarchyTreeNode
   SET unit_discount_vat = unit_discount + unit_discount_vat;

COMMIT;
