-- 200905070000

-- sets default values in different tables

UPDATE Document SET document_status = 2;
UPDATE Receipt SET document_status = 2;
UPDATE MoneySaleSlip SET document_status = 2;
UPDATE TransportationSlip SET document_status = 2;
UPDATE ProformaInvoice SET document_status = 2;
UPDATE ExpeditionSlip SET document_status = 2;
UPDATE WarrantyCertificate SET document_status = 2;
UPDATE AuthenticityCertificate SET document_status = 2;
UPDATE DebitNote SET document_status = 2;
UPDATE AdvancedShipmentNotification SET document_status = 2;
UPDATE DuttyFreeSlip SET document_status = 2;
UPDATE ReturnToVendorSlip SET document_status = 2;
UPDATE ConsignmentSlip SET document_status = 2;
UPDATE Invoice SET document_status = 2;
UPDATE CreditNote SET document_status = 2;
UPDATE GiftCertificate SET document_status = 2;
UPDATE MoneyCertificate SET document_status = 2;
UPDATE DiscountCertificate SET document_status = 2;
UPDATE BonusCertificate SET document_status = 2;
UPDATE MerchandiseContactableOrganizationalHierarchyTreeNode SET discount = 0 where discount is NULL;
UPDATE MerchandiseContactableOrganizationalHierarchyTreeNode SET min_stock= 0 where min_stock is NULL;
UPDATE MerchandiseContactableOrganizationalHierarchyTreeNode SET stock_in_transit=0 where stock_in_transit is NULL;
UPDATE MerchandiseContactableOrganizationalHierarchyTreeNode SET stock_reserved=0 where stock_reserved is NULL;
update PurchaseMerchandiseHierarchyTreeNode set unit_discount = 0 where unit_discount IS NULL;
update PurchaseMerchandiseHierarchyTreeNode set unit_discount_vat = 0 where unit_discount_vat IS NULL;
update PurchaseMerchandiseHierarchyTreeNode set unit_vat = 0 where unit_vat IS NULL;
update PurchaseMerchandiseHierarchyTreeNode set vat_rate = 0 where vat_rate IS NULL;
UPDATE CustomerPerson SET gender = 2 WHERE gender IS NULL;
