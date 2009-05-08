-- 200905081749

-- moves table foreign keys for the money sale slip <-> sale transaction relation from the money sale slip table to the sale transaction table
-- due to pre-existing redundant "mapped by" definitions in the data model

BEGIN TRANSACTION;

UPDATE SaleTransaction
   SET money_sale_slip = (SELECT MoneySaleSlip.object_id
                            FROM MoneySaleSlip
                           WHERE MoneySaleSlip.sale_transaction = SaleTransaction.object_id)
 WHERE EXISTS (SELECT MoneySaleSlip.object_id FROM MoneySaleSlip WHERE MoneySaleSlip.sale_transaction = SaleTransaction.object_id);

UPDATE MoneySaleSlip
   SET sale_transaction = NULL
 WHERE sale_transaction IS NOT NULL;

COMMIT;
