
-- build a query from the sqlite master
SELECT "SELECT """ || name || """, object_id FROM " || name || " UNION ALL" from sqlite_master where type="table" and sql like '%object_id%' and not name like '%Relation%';

SELECT object_id, count(1)
  FROM (
    SELECT object_id FROM Tree UNION ALL
    SELECT object_id FROM OrganizationalHierarchyTree UNION ALL
    SELECT object_id FROM SupplierHierarchyTree UNION ALL
    SELECT object_id FROM CustomerHierarchyTree UNION ALL
    SELECT object_id FROM MerchandiseHierarchyTree UNION ALL
    SELECT object_id FROM TreeNode UNION ALL
    SELECT object_id FROM ValueTreeNode UNION ALL
    SELECT object_id FROM Price UNION ALL
    SELECT object_id FROM Cost UNION ALL
    SELECT object_id FROM Margin UNION ALL
    SELECT object_id FROM AbsoluteMargin UNION ALL
    SELECT object_id FROM RelativeMargin UNION ALL
    SELECT object_id FROM OrganizationalHierarchyTreeNode UNION ALL
    SELECT object_id FROM ContactableOrganizationalHierarchyTreeNode UNION ALL
    SELECT object_id FROM MerchandiseHierarchyTreeNode UNION ALL
    SELECT object_id FROM MerchandiseContactableOrganizationalHierarchyTreeNode UNION ALL
    SELECT object_id FROM SaleMerchandiseHierarchyTreeNode UNION ALL
    SELECT object_id FROM RepairMerchandiseHierarchyTreeNode UNION ALL
    SELECT object_id FROM PurchaseMerchandiseHierarchyTreeNode UNION ALL
    SELECT object_id FROM ShipmentMerchandiseHierarchyTreeNode UNION ALL
    SELECT object_id FROM TransferMerchandiseHierarchyTreeNode UNION ALL
    SELECT object_id FROM StockAdjustmentMerchandiseHierarchyTreeNode UNION ALL
    SELECT object_id FROM FunctionalUnit UNION ALL
    SELECT object_id FROM Store UNION ALL
    SELECT object_id FROM Warehouse UNION ALL
    SELECT object_id FROM Factory UNION ALL
    SELECT object_id FROM Department UNION ALL
    SELECT object_id FROM PurchaseOrder UNION ALL
    SELECT object_id FROM PurchaseOrderMerchandiseOrganizationalHierarchyTreeNode UNION ALL
    SELECT object_id FROM Location UNION ALL
    SELECT object_id FROM OrganizationalMerchandiseHierarchyTreeNodeVatClass UNION ALL
    SELECT object_id FROM VatClass UNION ALL
    SELECT object_id FROM Reason UNION ALL
    SELECT object_id FROM StockAdjustmentReason UNION ALL
    SELECT object_id FROM PriceChangeReason UNION ALL
    SELECT object_id FROM StockAdjustment UNION ALL
    SELECT object_id FROM Language UNION ALL
    SELECT object_id FROM Currency UNION ALL
    SELECT object_id FROM Company UNION ALL
    SELECT object_id FROM SupplierCompany UNION ALL
    SELECT object_id FROM PartnerCompany UNION ALL
    SELECT object_id FROM SystemCompany UNION ALL
    SELECT object_id FROM SystemSettings UNION ALL
    SELECT object_id FROM CustomerCompany UNION ALL
    SELECT object_id FROM Address UNION ALL
    SELECT object_id FROM ContactInformation UNION ALL
    SELECT object_id FROM Person UNION ALL
    SELECT object_id FROM CustomerPerson UNION ALL
    SELECT object_id FROM Employee UNION ALL
    SELECT object_id FROM Sale UNION ALL
    SELECT object_id FROM Purchase UNION ALL
    SELECT object_id FROM PurchaseTransaction UNION ALL
    SELECT object_id FROM PaymentMethod UNION ALL
    SELECT object_id FROM FreePaymentMethod UNION ALL
    SELECT object_id FROM PaidPaymentMethod UNION ALL
    SELECT object_id FROM CreditNotePayment UNION ALL
    SELECT object_id FROM CashPayment UNION ALL
    SELECT object_id FROM GiftCertificatePayment UNION ALL
    SELECT object_id FROM CheckPayment UNION ALL
    SELECT object_id FROM PostDatedCheckPayment UNION ALL
    SELECT object_id FROM CardPayment UNION ALL
    SELECT object_id FROM PaypalPayment UNION ALL
    SELECT object_id FROM BankTransferPayment UNION ALL
    SELECT object_id FROM CreditPaymentMethod UNION ALL
    SELECT object_id FROM Document UNION ALL
    SELECT object_id FROM Receipt UNION ALL
    SELECT object_id FROM MoneySaleSlip UNION ALL
    SELECT object_id FROM TransportationSlip UNION ALL
    SELECT object_id FROM ProformaInvoice UNION ALL
    SELECT object_id FROM ExpeditionSlip UNION ALL
    SELECT object_id FROM WarrantyCertificate UNION ALL
    SELECT object_id FROM AuthenticityCertificate UNION ALL
    SELECT object_id FROM DebitNote UNION ALL
    SELECT object_id FROM AdvancedShipmentNotification UNION ALL
    SELECT object_id FROM DuttyFreeSlip UNION ALL
    SELECT object_id FROM ReturnToVendorSlip UNION ALL
    SELECT object_id FROM ConsignmentSlip UNION ALL
    SELECT object_id FROM Invoice UNION ALL
    SELECT object_id FROM CreditNote UNION ALL
    SELECT object_id FROM GiftCertificate UNION ALL
    SELECT object_id FROM MoneyCertificate UNION ALL
    SELECT object_id FROM DiscountCertificate UNION ALL
    SELECT object_id FROM BonusCertificate UNION ALL
    SELECT object_id FROM Return UNION ALL
    SELECT object_id FROM CustomerReturn UNION ALL
    SELECT object_id FROM SupplierReturn UNION ALL
    SELECT object_id FROM ConsignmentReturn UNION ALL
    SELECT object_id FROM MerchandiseHierarchyTreeNodeReturn UNION ALL
    SELECT object_id FROM PaymentReturn UNION ALL
    SELECT object_id FROM Reservation UNION ALL
    SELECT object_id FROM MerchandiseHierarchyTreeNodeReservation UNION ALL
    SELECT object_id FROM CustomerReservation UNION ALL
    SELECT object_id FROM PrepaidCustomerReservation UNION ALL
    SELECT object_id FROM InitialEntranceCustomerReservation UNION ALL
    SELECT object_id FROM NormalCustomerReservation UNION ALL
    SELECT object_id FROM StoreReservation UNION ALL
    SELECT object_id FROM Consignment UNION ALL
    SELECT object_id FROM ConsignmentMerchandiseHierarchyTreeNode UNION ALL
    SELECT object_id FROM Payment UNION ALL
    SELECT object_id FROM CreditPayment UNION ALL
    SELECT object_id FROM CompanyCreditPaymentMethod UNION ALL
    SELECT object_id FROM BankCreditPaymentMethod UNION ALL
    SELECT object_id FROM PaymentPaymentMethod UNION ALL
    SELECT object_id FROM User UNION ALL
    SELECT object_id FROM UserGroup UNION ALL
    SELECT object_id FROM Profile UNION ALL
    SELECT object_id FROM AccessControlList UNION ALL
    SELECT object_id FROM AccessControlListItem UNION ALL
    SELECT object_id FROM Bank UNION ALL
    SELECT object_id FROM BankBranch UNION ALL
    SELECT object_id FROM TransactionalMerchandise UNION ALL
    SELECT object_id FROM Service UNION ALL
    SELECT object_id FROM Insurance UNION ALL
    SELECT object_id FROM Repair UNION ALL
    SELECT object_id FROM ProductSet UNION ALL
    SELECT object_id FROM SaleTransaction UNION ALL
    SELECT object_id FROM SaleQuote UNION ALL
    SELECT object_id FROM ShipmentMethod UNION ALL
    SELECT object_id FROM Shipment UNION ALL
    SELECT object_id FROM Transfer UNION ALL
    SELECT object_id FROM ShipmentMethodSale UNION ALL
    SELECT object_id FROM ShipmentMethodPurchase UNION ALL
    SELECT object_id FROM FinancialAccount UNION ALL
    SELECT object_id FROM BankAccount UNION ALL
    SELECT object_id FROM PaypalAccount UNION ALL
    SELECT object_id FROM CreditContract UNION ALL
    SELECT object_id FROM Brand UNION ALL
    SELECT object_id FROM Collection UNION ALL
    SELECT object_id FROM Category UNION ALL
    SELECT object_id FROM Material UNION ALL
    SELECT object_id FROM Product UNION ALL
    SELECT object_id FROM SubProduct UNION ALL
    SELECT object_id FROM OrganizationalHierarchyMerchandiseSupplier UNION ALL
    SELECT object_id FROM PointOfSale UNION ALL
    SELECT object_id FROM RootEntity UNION ALL
    SELECT object_id FROM Media UNION ALL
    SELECT object_id FROM PersonRelation
)
GROUP BY object_id
HAVING count(1) > 1;


-- get all the entity names and object ids
SELECT "Tree", object_id FROM Tree UNION ALL
SELECT "OrganizationalHierarchyTree", object_id FROM OrganizationalHierarchyTree UNION ALL
SELECT "SupplierHierarchyTree", object_id FROM SupplierHierarchyTree UNION ALL
SELECT "CustomerHierarchyTree", object_id FROM CustomerHierarchyTree UNION ALL
SELECT "MerchandiseHierarchyTree", object_id FROM MerchandiseHierarchyTree UNION ALL
SELECT "TreeNode", object_id FROM TreeNode UNION ALL
SELECT "ValueTreeNode", object_id FROM ValueTreeNode UNION ALL
SELECT "Price", object_id FROM Price UNION ALL
SELECT "Cost", object_id FROM Cost UNION ALL
SELECT "Margin", object_id FROM Margin UNION ALL
SELECT "AbsoluteMargin", object_id FROM AbsoluteMargin UNION ALL
SELECT "RelativeMargin", object_id FROM RelativeMargin UNION ALL
SELECT "OrganizationalHierarchyTreeNode", object_id FROM OrganizationalHierarchyTreeNode UNION ALL
SELECT "ContactableOrganizationalHierarchyTreeNode", object_id FROM ContactableOrganizationalHierarchyTreeNode UNION ALL
SELECT "MerchandiseHierarchyTreeNode", object_id FROM MerchandiseHierarchyTreeNode UNION ALL
SELECT "MerchandiseContactableOrganizationalHierarchyTreeNode", object_id FROM MerchandiseContactableOrganizationalHierarchyTreeNode UNION ALL
SELECT "SaleMerchandiseHierarchyTreeNode", object_id FROM SaleMerchandiseHierarchyTreeNode UNION ALL
SELECT "RepairMerchandiseHierarchyTreeNode", object_id FROM RepairMerchandiseHierarchyTreeNode UNION ALL
SELECT "PurchaseMerchandiseHierarchyTreeNode", object_id FROM PurchaseMerchandiseHierarchyTreeNode UNION ALL
SELECT "ShipmentMerchandiseHierarchyTreeNode", object_id FROM ShipmentMerchandiseHierarchyTreeNode UNION ALL
SELECT "TransferMerchandiseHierarchyTreeNode", object_id FROM TransferMerchandiseHierarchyTreeNode UNION ALL
SELECT "StockAdjustmentMerchandiseHierarchyTreeNode", object_id FROM StockAdjustmentMerchandiseHierarchyTreeNode UNION ALL
SELECT "FunctionalUnit", object_id FROM FunctionalUnit UNION ALL
SELECT "Store", object_id FROM Store UNION ALL
SELECT "Warehouse", object_id FROM Warehouse UNION ALL
SELECT "Factory", object_id FROM Factory UNION ALL
SELECT "Department", object_id FROM Department UNION ALL
SELECT "PurchaseOrder", object_id FROM PurchaseOrder UNION ALL
SELECT "PurchaseOrderMerchandiseOrganizationalHierarchyTreeNode", object_id FROM PurchaseOrderMerchandiseOrganizationalHierarchyTreeNode UNION ALL
SELECT "Location", object_id FROM Location UNION ALL
SELECT "OrganizationalMerchandiseHierarchyTreeNodeVatClass", object_id FROM OrganizationalMerchandiseHierarchyTreeNodeVatClass UNION ALL
SELECT "VatClass", object_id FROM VatClass UNION ALL
SELECT "Reason", object_id FROM Reason UNION ALL
SELECT "StockAdjustmentReason", object_id FROM StockAdjustmentReason UNION ALL
SELECT "PriceChangeReason", object_id FROM PriceChangeReason UNION ALL
SELECT "StockAdjustment", object_id FROM StockAdjustment UNION ALL
SELECT "Language", object_id FROM Language UNION ALL
SELECT "Currency", object_id FROM Currency UNION ALL
SELECT "Company", object_id FROM Company UNION ALL
SELECT "SupplierCompany", object_id FROM SupplierCompany UNION ALL
SELECT "PartnerCompany", object_id FROM PartnerCompany UNION ALL
SELECT "SystemCompany", object_id FROM SystemCompany UNION ALL
SELECT "SystemSettings", object_id FROM SystemSettings UNION ALL
SELECT "CustomerCompany", object_id FROM CustomerCompany UNION ALL
SELECT "Address", object_id FROM Address UNION ALL
SELECT "ContactInformation", object_id FROM ContactInformation UNION ALL
SELECT "Person", object_id FROM Person UNION ALL
SELECT "CustomerPerson", object_id FROM CustomerPerson UNION ALL
SELECT "Employee", object_id FROM Employee UNION ALL
SELECT "Sale", object_id FROM Sale UNION ALL
SELECT "Purchase", object_id FROM Purchase UNION ALL
SELECT "PurchaseTransaction", object_id FROM PurchaseTransaction UNION ALL
SELECT "PaymentMethod", object_id FROM PaymentMethod UNION ALL
SELECT "FreePaymentMethod", object_id FROM FreePaymentMethod UNION ALL
SELECT "PaidPaymentMethod", object_id FROM PaidPaymentMethod UNION ALL
SELECT "CreditNotePayment", object_id FROM CreditNotePayment UNION ALL
SELECT "CashPayment", object_id FROM CashPayment UNION ALL
SELECT "GiftCertificatePayment", object_id FROM GiftCertificatePayment UNION ALL
SELECT "CheckPayment", object_id FROM CheckPayment UNION ALL
SELECT "PostDatedCheckPayment", object_id FROM PostDatedCheckPayment UNION ALL
SELECT "CardPayment", object_id FROM CardPayment UNION ALL
SELECT "PaypalPayment", object_id FROM PaypalPayment UNION ALL
SELECT "BankTransferPayment", object_id FROM BankTransferPayment UNION ALL
SELECT "CreditPaymentMethod", object_id FROM CreditPaymentMethod UNION ALL
SELECT "Document", object_id FROM Document UNION ALL
SELECT "Receipt", object_id FROM Receipt UNION ALL
SELECT "MoneySaleSlip", object_id FROM MoneySaleSlip UNION ALL
SELECT "TransportationSlip", object_id FROM TransportationSlip UNION ALL
SELECT "ProformaInvoice", object_id FROM ProformaInvoice UNION ALL
SELECT "ExpeditionSlip", object_id FROM ExpeditionSlip UNION ALL
SELECT "WarrantyCertificate", object_id FROM WarrantyCertificate UNION ALL
SELECT "AuthenticityCertificate", object_id FROM AuthenticityCertificate UNION ALL
SELECT "DebitNote", object_id FROM DebitNote UNION ALL
SELECT "AdvancedShipmentNotification", object_id FROM AdvancedShipmentNotification UNION ALL
SELECT "DuttyFreeSlip", object_id FROM DuttyFreeSlip UNION ALL
SELECT "ReturnToVendorSlip", object_id FROM ReturnToVendorSlip UNION ALL
SELECT "ConsignmentSlip", object_id FROM ConsignmentSlip UNION ALL
SELECT "Invoice", object_id FROM Invoice UNION ALL
SELECT "CreditNote", object_id FROM CreditNote UNION ALL
SELECT "GiftCertificate", object_id FROM GiftCertificate UNION ALL
SELECT "MoneyCertificate", object_id FROM MoneyCertificate UNION ALL
SELECT "DiscountCertificate", object_id FROM DiscountCertificate UNION ALL
SELECT "BonusCertificate", object_id FROM BonusCertificate UNION ALL
SELECT "Return", object_id FROM Return UNION ALL
SELECT "CustomerReturn", object_id FROM CustomerReturn UNION ALL
SELECT "SupplierReturn", object_id FROM SupplierReturn UNION ALL
SELECT "ConsignmentReturn", object_id FROM ConsignmentReturn UNION ALL
SELECT "MerchandiseHierarchyTreeNodeReturn", object_id FROM MerchandiseHierarchyTreeNodeReturn UNION ALL
SELECT "PaymentReturn", object_id FROM PaymentReturn UNION ALL
SELECT "Reservation", object_id FROM Reservation UNION ALL
SELECT "MerchandiseHierarchyTreeNodeReservation", object_id FROM MerchandiseHierarchyTreeNodeReservation UNION ALL
SELECT "CustomerReservation", object_id FROM CustomerReservation UNION ALL
SELECT "PrepaidCustomerReservation", object_id FROM PrepaidCustomerReservation UNION ALL
SELECT "InitialEntranceCustomerReservation", object_id FROM InitialEntranceCustomerReservation UNION ALL
SELECT "NormalCustomerReservation", object_id FROM NormalCustomerReservation UNION ALL
SELECT "StoreReservation", object_id FROM StoreReservation UNION ALL
SELECT "Consignment", object_id FROM Consignment UNION ALL
SELECT "ConsignmentMerchandiseHierarchyTreeNode", object_id FROM ConsignmentMerchandiseHierarchyTreeNode UNION ALL
SELECT "Payment", object_id FROM Payment UNION ALL
SELECT "CreditPayment", object_id FROM CreditPayment UNION ALL
SELECT "CompanyCreditPaymentMethod", object_id FROM CompanyCreditPaymentMethod UNION ALL
SELECT "BankCreditPaymentMethod", object_id FROM BankCreditPaymentMethod UNION ALL
SELECT "PaymentPaymentMethod", object_id FROM PaymentPaymentMethod UNION ALL
SELECT "User", object_id FROM User UNION ALL
SELECT "UserGroup", object_id FROM UserGroup UNION ALL
SELECT "Profile", object_id FROM Profile UNION ALL
SELECT "AccessControlList", object_id FROM AccessControlList UNION ALL
SELECT "AccessControlListItem", object_id FROM AccessControlListItem UNION ALL
SELECT "Bank", object_id FROM Bank UNION ALL
SELECT "BankBranch", object_id FROM BankBranch UNION ALL
SELECT "TransactionalMerchandise", object_id FROM TransactionalMerchandise UNION ALL
SELECT "Service", object_id FROM Service UNION ALL
SELECT "Insurance", object_id FROM Insurance UNION ALL
SELECT "Repair", object_id FROM Repair UNION ALL
SELECT "ProductSet", object_id FROM ProductSet UNION ALL
SELECT "SaleTransaction", object_id FROM SaleTransaction UNION ALL
SELECT "SaleQuote", object_id FROM SaleQuote UNION ALL
SELECT "ShipmentMethod", object_id FROM ShipmentMethod UNION ALL
SELECT "Shipment", object_id FROM Shipment UNION ALL
SELECT "Transfer", object_id FROM Transfer UNION ALL
SELECT "ShipmentMethodSale", object_id FROM ShipmentMethodSale UNION ALL
SELECT "ShipmentMethodPurchase", object_id FROM ShipmentMethodPurchase UNION ALL
SELECT "FinancialAccount", object_id FROM FinancialAccount UNION ALL
SELECT "BankAccount", object_id FROM BankAccount UNION ALL
SELECT "PaypalAccount", object_id FROM PaypalAccount UNION ALL
SELECT "CreditContract", object_id FROM CreditContract UNION ALL
SELECT "Brand", object_id FROM Brand UNION ALL
SELECT "Collection", object_id FROM Collection UNION ALL
SELECT "Category", object_id FROM Category UNION ALL
SELECT "Material", object_id FROM Material UNION ALL
SELECT "Product", object_id FROM Product UNION ALL
SELECT "SubProduct", object_id FROM SubProduct UNION ALL
SELECT "OrganizationalHierarchyMerchandiseSupplier", object_id FROM OrganizationalHierarchyMerchandiseSupplier UNION ALL
SELECT "PointOfSale", object_id FROM PointOfSale UNION ALL
SELECT "RootEntity", object_id FROM RootEntity UNION ALL
SELECT "Media", object_id FROM Media)

where object_id in (


select object_id from
(
SELECT object_id FROM Tree UNION ALL
SELECT object_id FROM OrganizationalHierarchyTree UNION ALL
SELECT object_id FROM SupplierHierarchyTree UNION ALL
SELECT object_id FROM CustomerHierarchyTree UNION ALL
SELECT object_id FROM MerchandiseHierarchyTree UNION ALL
SELECT object_id FROM TreeNode UNION ALL
SELECT object_id FROM ValueTreeNode UNION ALL
SELECT object_id FROM Price UNION ALL
SELECT object_id FROM Cost UNION ALL
SELECT object_id FROM Margin UNION ALL
SELECT object_id FROM AbsoluteMargin UNION ALL
SELECT object_id FROM RelativeMargin UNION ALL
SELECT object_id FROM OrganizationalHierarchyTreeNode UNION ALL
SELECT object_id FROM ContactableOrganizationalHierarchyTreeNode UNION ALL
SELECT object_id FROM MerchandiseHierarchyTreeNode UNION ALL
SELECT object_id FROM MerchandiseContactableOrganizationalHierarchyTreeNode UNION ALL
SELECT object_id FROM SaleMerchandiseHierarchyTreeNode UNION ALL
SELECT object_id FROM RepairMerchandiseHierarchyTreeNode UNION ALL
SELECT object_id FROM PurchaseMerchandiseHierarchyTreeNode UNION ALL
SELECT object_id FROM ShipmentMerchandiseHierarchyTreeNode UNION ALL
SELECT object_id FROM TransferMerchandiseHierarchyTreeNode UNION ALL
SELECT object_id FROM StockAdjustmentMerchandiseHierarchyTreeNode UNION ALL
SELECT object_id FROM FunctionalUnit UNION ALL
SELECT object_id FROM Store UNION ALL
SELECT object_id FROM Warehouse UNION ALL
SELECT object_id FROM Factory UNION ALL
SELECT object_id FROM Department UNION ALL
SELECT object_id FROM PurchaseOrder UNION ALL
SELECT object_id FROM PurchaseOrderMerchandiseOrganizationalHierarchyTreeNode UNION ALL
SELECT object_id FROM Location UNION ALL
SELECT object_id FROM OrganizationalMerchandiseHierarchyTreeNodeVatClass UNION ALL
SELECT object_id FROM VatClass UNION ALL
SELECT object_id FROM Reason UNION ALL
SELECT object_id FROM StockAdjustmentReason UNION ALL
SELECT object_id FROM PriceChangeReason UNION ALL
SELECT object_id FROM StockAdjustment UNION ALL
SELECT object_id FROM Language UNION ALL
SELECT object_id FROM Currency UNION ALL
SELECT object_id FROM Company UNION ALL
SELECT object_id FROM SupplierCompany UNION ALL
SELECT object_id FROM PartnerCompany UNION ALL
SELECT object_id FROM SystemCompany UNION ALL
SELECT object_id FROM SystemSettings UNION ALL
SELECT object_id FROM CustomerCompany UNION ALL
SELECT object_id FROM Address UNION ALL
SELECT object_id FROM ContactInformation UNION ALL
SELECT object_id FROM Person UNION ALL
SELECT object_id FROM CustomerPerson UNION ALL
SELECT object_id FROM Employee UNION ALL
SELECT object_id FROM Sale UNION ALL
SELECT object_id FROM Purchase UNION ALL
SELECT object_id FROM PurchaseTransaction UNION ALL
SELECT object_id FROM PaymentMethod UNION ALL
SELECT object_id FROM FreePaymentMethod UNION ALL
SELECT object_id FROM PaidPaymentMethod UNION ALL
SELECT object_id FROM CreditNotePayment UNION ALL
SELECT object_id FROM CashPayment UNION ALL
SELECT object_id FROM GiftCertificatePayment UNION ALL
SELECT object_id FROM CheckPayment UNION ALL
SELECT object_id FROM PostDatedCheckPayment UNION ALL
SELECT object_id FROM CardPayment UNION ALL
SELECT object_id FROM PaypalPayment UNION ALL
SELECT object_id FROM BankTransferPayment UNION ALL
SELECT object_id FROM CreditPaymentMethod UNION ALL
SELECT object_id FROM Document UNION ALL
SELECT object_id FROM Receipt UNION ALL
SELECT object_id FROM MoneySaleSlip UNION ALL
SELECT object_id FROM TransportationSlip UNION ALL
SELECT object_id FROM ProformaInvoice UNION ALL
SELECT object_id FROM ExpeditionSlip UNION ALL
SELECT object_id FROM WarrantyCertificate UNION ALL
SELECT object_id FROM AuthenticityCertificate UNION ALL
SELECT object_id FROM DebitNote UNION ALL
SELECT object_id FROM AdvancedShipmentNotification UNION ALL
SELECT object_id FROM DuttyFreeSlip UNION ALL
SELECT object_id FROM ReturnToVendorSlip UNION ALL
SELECT object_id FROM ConsignmentSlip UNION ALL
SELECT object_id FROM Invoice UNION ALL
SELECT object_id FROM CreditNote UNION ALL
SELECT object_id FROM GiftCertificate UNION ALL
SELECT object_id FROM MoneyCertificate UNION ALL
SELECT object_id FROM DiscountCertificate UNION ALL
SELECT object_id FROM BonusCertificate UNION ALL
SELECT object_id FROM Return UNION ALL
SELECT object_id FROM CustomerReturn UNION ALL
SELECT object_id FROM SupplierReturn UNION ALL
SELECT object_id FROM ConsignmentReturn UNION ALL
SELECT object_id FROM MerchandiseHierarchyTreeNodeReturn UNION ALL
SELECT object_id FROM PaymentReturn UNION ALL
SELECT object_id FROM Reservation UNION ALL
SELECT object_id FROM MerchandiseHierarchyTreeNodeReservation UNION ALL
SELECT object_id FROM CustomerReservation UNION ALL
SELECT object_id FROM PrepaidCustomerReservation UNION ALL
SELECT object_id FROM InitialEntranceCustomerReservation UNION ALL
SELECT object_id FROM NormalCustomerReservation UNION ALL
SELECT object_id FROM StoreReservation UNION ALL
SELECT object_id FROM Consignment UNION ALL
SELECT object_id FROM ConsignmentMerchandiseHierarchyTreeNode UNION ALL
SELECT object_id FROM Payment UNION ALL
SELECT object_id FROM CreditPayment UNION ALL
SELECT object_id FROM CompanyCreditPaymentMethod UNION ALL
SELECT object_id FROM BankCreditPaymentMethod UNION ALL
SELECT object_id FROM PaymentPaymentMethod UNION ALL
SELECT object_id FROM User UNION ALL
SELECT object_id FROM UserGroup UNION ALL
SELECT object_id FROM Profile UNION ALL
SELECT object_id FROM AccessControlList UNION ALL
SELECT object_id FROM AccessControlListItem UNION ALL
SELECT object_id FROM Bank UNION ALL
SELECT object_id FROM BankBranch UNION ALL
SELECT object_id FROM TransactionalMerchandise UNION ALL
SELECT object_id FROM Service UNION ALL
SELECT object_id FROM Insurance UNION ALL
SELECT object_id FROM Repair UNION ALL
SELECT object_id FROM ProductSet UNION ALL
SELECT object_id FROM SaleTransaction UNION ALL
SELECT object_id FROM SaleQuote UNION ALL
SELECT object_id FROM ShipmentMethod UNION ALL
SELECT object_id FROM Shipment UNION ALL
SELECT object_id FROM Transfer UNION ALL
SELECT object_id FROM ShipmentMethodSale UNION ALL
SELECT object_id FROM ShipmentMethodPurchase UNION ALL
SELECT object_id FROM FinancialAccount UNION ALL
SELECT object_id FROM BankAccount UNION ALL
SELECT object_id FROM PaypalAccount UNION ALL
SELECT object_id FROM CreditContract UNION ALL
SELECT object_id FROM Brand UNION ALL
SELECT object_id FROM Collection UNION ALL
SELECT object_id FROM Category UNION ALL
SELECT object_id FROM Material UNION ALL
SELECT object_id FROM Product UNION ALL
SELECT object_id FROM SubProduct UNION ALL
SELECT object_id FROM OrganizationalHierarchyMerchandiseSupplier UNION ALL
SELECT object_id FROM PointOfSale UNION ALL
SELECT object_id FROM RootEntity UNION ALL
SELECT object_id FROM Media UNION ALL
SELECT object_id FROM PersonRelation
)
group by object_id
having count(1) > 1)




select * from (
SELECT "Tree", object_id FROM Tree UNION ALL
SELECT "OrganizationalHierarchyTree", object_id FROM OrganizationalHierarchyTree UNION ALL
SELECT "SupplierHierarchyTree", object_id FROM SupplierHierarchyTree UNION ALL
SELECT "CustomerHierarchyTree", object_id FROM CustomerHierarchyTree UNION ALL
SELECT "MerchandiseHierarchyTree", object_id FROM MerchandiseHierarchyTree UNION ALL
SELECT "TreeNode", object_id FROM TreeNode UNION ALL
SELECT "ValueTreeNode", object_id FROM ValueTreeNode UNION ALL
SELECT "Price", object_id FROM Price UNION ALL
SELECT "Cost", object_id FROM Cost UNION ALL
SELECT "Margin", object_id FROM Margin UNION ALL
SELECT "AbsoluteMargin", object_id FROM AbsoluteMargin UNION ALL
SELECT "RelativeMargin", object_id FROM RelativeMargin UNION ALL
SELECT "OrganizationalHierarchyTreeNode", object_id FROM OrganizationalHierarchyTreeNode UNION ALL
SELECT "ContactableOrganizationalHierarchyTreeNode", object_id FROM ContactableOrganizationalHierarchyTreeNode UNION ALL
SELECT "MerchandiseHierarchyTreeNode", object_id FROM MerchandiseHierarchyTreeNode UNION ALL
SELECT "MerchandiseContactableOrganizationalHierarchyTreeNode", object_id FROM MerchandiseContactableOrganizationalHierarchyTreeNode UNION ALL
SELECT "SaleMerchandiseHierarchyTreeNode", object_id FROM SaleMerchandiseHierarchyTreeNode UNION ALL
SELECT "RepairMerchandiseHierarchyTreeNode", object_id FROM RepairMerchandiseHierarchyTreeNode UNION ALL
SELECT "PurchaseMerchandiseHierarchyTreeNode", object_id FROM PurchaseMerchandiseHierarchyTreeNode UNION ALL
SELECT "ShipmentMerchandiseHierarchyTreeNode", object_id FROM ShipmentMerchandiseHierarchyTreeNode UNION ALL
SELECT "TransferMerchandiseHierarchyTreeNode", object_id FROM TransferMerchandiseHierarchyTreeNode UNION ALL
SELECT "StockAdjustmentMerchandiseHierarchyTreeNode", object_id FROM StockAdjustmentMerchandiseHierarchyTreeNode UNION ALL
SELECT "FunctionalUnit", object_id FROM FunctionalUnit UNION ALL
SELECT "Store", object_id FROM Store UNION ALL
SELECT "Warehouse", object_id FROM Warehouse UNION ALL
SELECT "Factory", object_id FROM Factory UNION ALL
SELECT "Department", object_id FROM Department UNION ALL
SELECT "PurchaseOrder", object_id FROM PurchaseOrder UNION ALL
SELECT "PurchaseOrderMerchandiseOrganizationalHierarchyTreeNode", object_id FROM PurchaseOrderMerchandiseOrganizationalHierarchyTreeNode UNION ALL
SELECT "Location", object_id FROM Location UNION ALL
SELECT "OrganizationalMerchandiseHierarchyTreeNodeVatClass", object_id FROM OrganizationalMerchandiseHierarchyTreeNodeVatClass UNION ALL
SELECT "VatClass", object_id FROM VatClass UNION ALL
SELECT "Reason", object_id FROM Reason UNION ALL
SELECT "StockAdjustmentReason", object_id FROM StockAdjustmentReason UNION ALL
SELECT "PriceChangeReason", object_id FROM PriceChangeReason UNION ALL
SELECT "StockAdjustment", object_id FROM StockAdjustment UNION ALL
SELECT "Language", object_id FROM Language UNION ALL
SELECT "Currency", object_id FROM Currency UNION ALL
SELECT "Company", object_id FROM Company UNION ALL
SELECT "SupplierCompany", object_id FROM SupplierCompany UNION ALL
SELECT "PartnerCompany", object_id FROM PartnerCompany UNION ALL
SELECT "SystemCompany", object_id FROM SystemCompany UNION ALL
SELECT "SystemSettings", object_id FROM SystemSettings UNION ALL
SELECT "CustomerCompany", object_id FROM CustomerCompany UNION ALL
SELECT "Address", object_id FROM Address UNION ALL
SELECT "ContactInformation", object_id FROM ContactInformation UNION ALL
SELECT "Person", object_id FROM Person UNION ALL
SELECT "CustomerPerson", object_id FROM CustomerPerson UNION ALL
SELECT "Employee", object_id FROM Employee UNION ALL
SELECT "Sale", object_id FROM Sale UNION ALL
SELECT "Purchase", object_id FROM Purchase UNION ALL
SELECT "PurchaseTransaction", object_id FROM PurchaseTransaction UNION ALL
SELECT "PaymentMethod", object_id FROM PaymentMethod UNION ALL
SELECT "FreePaymentMethod", object_id FROM FreePaymentMethod UNION ALL
SELECT "PaidPaymentMethod", object_id FROM PaidPaymentMethod UNION ALL
SELECT "CreditNotePayment", object_id FROM CreditNotePayment UNION ALL
SELECT "CashPayment", object_id FROM CashPayment UNION ALL
SELECT "GiftCertificatePayment", object_id FROM GiftCertificatePayment UNION ALL
SELECT "CheckPayment", object_id FROM CheckPayment UNION ALL
SELECT "PostDatedCheckPayment", object_id FROM PostDatedCheckPayment UNION ALL
SELECT "CardPayment", object_id FROM CardPayment UNION ALL
SELECT "PaypalPayment", object_id FROM PaypalPayment UNION ALL
SELECT "BankTransferPayment", object_id FROM BankTransferPayment UNION ALL
SELECT "CreditPaymentMethod", object_id FROM CreditPaymentMethod UNION ALL
SELECT "Document", object_id FROM Document UNION ALL
SELECT "Receipt", object_id FROM Receipt UNION ALL
SELECT "MoneySaleSlip", object_id FROM MoneySaleSlip UNION ALL
SELECT "TransportationSlip", object_id FROM TransportationSlip UNION ALL
SELECT "ProformaInvoice", object_id FROM ProformaInvoice UNION ALL
SELECT "ExpeditionSlip", object_id FROM ExpeditionSlip UNION ALL
SELECT "WarrantyCertificate", object_id FROM WarrantyCertificate UNION ALL
SELECT "AuthenticityCertificate", object_id FROM AuthenticityCertificate UNION ALL
SELECT "DebitNote", object_id FROM DebitNote UNION ALL
SELECT "AdvancedShipmentNotification", object_id FROM AdvancedShipmentNotification UNION ALL
SELECT "DuttyFreeSlip", object_id FROM DuttyFreeSlip UNION ALL
SELECT "ReturnToVendorSlip", object_id FROM ReturnToVendorSlip UNION ALL
SELECT "ConsignmentSlip", object_id FROM ConsignmentSlip UNION ALL
SELECT "Invoice", object_id FROM Invoice UNION ALL
SELECT "CreditNote", object_id FROM CreditNote UNION ALL
SELECT "GiftCertificate", object_id FROM GiftCertificate UNION ALL
SELECT "MoneyCertificate", object_id FROM MoneyCertificate UNION ALL
SELECT "DiscountCertificate", object_id FROM DiscountCertificate UNION ALL
SELECT "BonusCertificate", object_id FROM BonusCertificate UNION ALL
SELECT "Return", object_id FROM Return UNION ALL
SELECT "CustomerReturn", object_id FROM CustomerReturn UNION ALL
SELECT "SupplierReturn", object_id FROM SupplierReturn UNION ALL
SELECT "ConsignmentReturn", object_id FROM ConsignmentReturn UNION ALL
SELECT "MerchandiseHierarchyTreeNodeReturn", object_id FROM MerchandiseHierarchyTreeNodeReturn UNION ALL
SELECT "PaymentReturn", object_id FROM PaymentReturn UNION ALL
SELECT "Reservation", object_id FROM Reservation UNION ALL
SELECT "MerchandiseHierarchyTreeNodeReservation", object_id FROM MerchandiseHierarchyTreeNodeReservation UNION ALL
SELECT "CustomerReservation", object_id FROM CustomerReservation UNION ALL
SELECT "PrepaidCustomerReservation", object_id FROM PrepaidCustomerReservation UNION ALL
SELECT "InitialEntranceCustomerReservation", object_id FROM InitialEntranceCustomerReservation UNION ALL
SELECT "NormalCustomerReservation", object_id FROM NormalCustomerReservation UNION ALL
SELECT "StoreReservation", object_id FROM StoreReservation UNION ALL
SELECT "Consignment", object_id FROM Consignment UNION ALL
SELECT "ConsignmentMerchandiseHierarchyTreeNode", object_id FROM ConsignmentMerchandiseHierarchyTreeNode UNION ALL
SELECT "Payment", object_id FROM Payment UNION ALL
SELECT "CreditPayment", object_id FROM CreditPayment UNION ALL
SELECT "CompanyCreditPaymentMethod", object_id FROM CompanyCreditPaymentMethod UNION ALL
SELECT "BankCreditPaymentMethod", object_id FROM BankCreditPaymentMethod UNION ALL
SELECT "PaymentPaymentMethod", object_id FROM PaymentPaymentMethod UNION ALL
SELECT "User", object_id FROM User UNION ALL
SELECT "UserGroup", object_id FROM UserGroup UNION ALL
SELECT "Profile", object_id FROM Profile UNION ALL
SELECT "AccessControlList", object_id FROM AccessControlList UNION ALL
SELECT "AccessControlListItem", object_id FROM AccessControlListItem UNION ALL
SELECT "Bank", object_id FROM Bank UNION ALL
SELECT "BankBranch", object_id FROM BankBranch UNION ALL
SELECT "TransactionalMerchandise", object_id FROM TransactionalMerchandise UNION ALL
SELECT "Service", object_id FROM Service UNION ALL
SELECT "Insurance", object_id FROM Insurance UNION ALL
SELECT "Repair", object_id FROM Repair UNION ALL
SELECT "ProductSet", object_id FROM ProductSet UNION ALL
SELECT "SaleTransaction", object_id FROM SaleTransaction UNION ALL
SELECT "SaleQuote", object_id FROM SaleQuote UNION ALL
SELECT "ShipmentMethod", object_id FROM ShipmentMethod UNION ALL
SELECT "Shipment", object_id FROM Shipment UNION ALL
SELECT "Transfer", object_id FROM Transfer UNION ALL
SELECT "ShipmentMethodSale", object_id FROM ShipmentMethodSale UNION ALL
SELECT "ShipmentMethodPurchase", object_id FROM ShipmentMethodPurchase UNION ALL
SELECT "FinancialAccount", object_id FROM FinancialAccount UNION ALL
SELECT "BankAccount", object_id FROM BankAccount UNION ALL
SELECT "PaypalAccount", object_id FROM PaypalAccount UNION ALL
SELECT "CreditContract", object_id FROM CreditContract UNION ALL
SELECT "Brand", object_id FROM Brand UNION ALL
SELECT "Collection", object_id FROM Collection UNION ALL
SELECT "Category", object_id FROM Category UNION ALL
SELECT "Material", object_id FROM Material UNION ALL
SELECT "Product", object_id FROM Product UNION ALL
SELECT "SubProduct", object_id FROM SubProduct UNION ALL
SELECT "OrganizationalHierarchyMerchandiseSupplier", object_id FROM OrganizationalHierarchyMerchandiseSupplier UNION ALL
SELECT "PointOfSale", object_id FROM PointOfSale UNION ALL
SELECT "RootEntity", object_id FROM RootEntity UNION ALL
SELECT "Media", object_id FROM Media) t

where t.object_id in (


select object_id from
(
SELECT object_id FROM Tree UNION ALL
SELECT object_id FROM OrganizationalHierarchyTree UNION ALL
SELECT object_id FROM SupplierHierarchyTree UNION ALL
SELECT object_id FROM CustomerHierarchyTree UNION ALL
SELECT object_id FROM MerchandiseHierarchyTree UNION ALL
SELECT object_id FROM TreeNode UNION ALL
SELECT object_id FROM ValueTreeNode UNION ALL
SELECT object_id FROM Price UNION ALL
SELECT object_id FROM Cost UNION ALL
SELECT object_id FROM Margin UNION ALL
SELECT object_id FROM AbsoluteMargin UNION ALL
SELECT object_id FROM RelativeMargin UNION ALL
SELECT object_id FROM OrganizationalHierarchyTreeNode UNION ALL
SELECT object_id FROM ContactableOrganizationalHierarchyTreeNode UNION ALL
SELECT object_id FROM MerchandiseHierarchyTreeNode UNION ALL
SELECT object_id FROM MerchandiseContactableOrganizationalHierarchyTreeNode UNION ALL
SELECT object_id FROM SaleMerchandiseHierarchyTreeNode UNION ALL
SELECT object_id FROM RepairMerchandiseHierarchyTreeNode UNION ALL
SELECT object_id FROM PurchaseMerchandiseHierarchyTreeNode UNION ALL
SELECT object_id FROM ShipmentMerchandiseHierarchyTreeNode UNION ALL
SELECT object_id FROM TransferMerchandiseHierarchyTreeNode UNION ALL
SELECT object_id FROM StockAdjustmentMerchandiseHierarchyTreeNode UNION ALL
SELECT object_id FROM FunctionalUnit UNION ALL
SELECT object_id FROM Store UNION ALL
SELECT object_id FROM Warehouse UNION ALL
SELECT object_id FROM Factory UNION ALL
SELECT object_id FROM Department UNION ALL
SELECT object_id FROM PurchaseOrder UNION ALL
SELECT object_id FROM PurchaseOrderMerchandiseOrganizationalHierarchyTreeNode UNION ALL
SELECT object_id FROM Location UNION ALL
SELECT object_id FROM OrganizationalMerchandiseHierarchyTreeNodeVatClass UNION ALL
SELECT object_id FROM VatClass UNION ALL
SELECT object_id FROM Reason UNION ALL
SELECT object_id FROM StockAdjustmentReason UNION ALL
SELECT object_id FROM PriceChangeReason UNION ALL
SELECT object_id FROM StockAdjustment UNION ALL
SELECT object_id FROM Language UNION ALL
SELECT object_id FROM Currency UNION ALL
SELECT object_id FROM Company UNION ALL
SELECT object_id FROM SupplierCompany UNION ALL
SELECT object_id FROM PartnerCompany UNION ALL
SELECT object_id FROM SystemCompany UNION ALL
SELECT object_id FROM SystemSettings UNION ALL
SELECT object_id FROM CustomerCompany UNION ALL
SELECT object_id FROM Address UNION ALL
SELECT object_id FROM ContactInformation UNION ALL
SELECT object_id FROM Person UNION ALL
SELECT object_id FROM CustomerPerson UNION ALL
SELECT object_id FROM Employee UNION ALL
SELECT object_id FROM Sale UNION ALL
SELECT object_id FROM Purchase UNION ALL
SELECT object_id FROM PurchaseTransaction UNION ALL
SELECT object_id FROM PaymentMethod UNION ALL
SELECT object_id FROM FreePaymentMethod UNION ALL
SELECT object_id FROM PaidPaymentMethod UNION ALL
SELECT object_id FROM CreditNotePayment UNION ALL
SELECT object_id FROM CashPayment UNION ALL
SELECT object_id FROM GiftCertificatePayment UNION ALL
SELECT object_id FROM CheckPayment UNION ALL
SELECT object_id FROM PostDatedCheckPayment UNION ALL
SELECT object_id FROM CardPayment UNION ALL
SELECT object_id FROM PaypalPayment UNION ALL
SELECT object_id FROM BankTransferPayment UNION ALL
SELECT object_id FROM CreditPaymentMethod UNION ALL
SELECT object_id FROM Document UNION ALL
SELECT object_id FROM Receipt UNION ALL
SELECT object_id FROM MoneySaleSlip UNION ALL
SELECT object_id FROM TransportationSlip UNION ALL
SELECT object_id FROM ProformaInvoice UNION ALL
SELECT object_id FROM ExpeditionSlip UNION ALL
SELECT object_id FROM WarrantyCertificate UNION ALL
SELECT object_id FROM AuthenticityCertificate UNION ALL
SELECT object_id FROM DebitNote UNION ALL
SELECT object_id FROM AdvancedShipmentNotification UNION ALL
SELECT object_id FROM DuttyFreeSlip UNION ALL
SELECT object_id FROM ReturnToVendorSlip UNION ALL
SELECT object_id FROM ConsignmentSlip UNION ALL
SELECT object_id FROM Invoice UNION ALL
SELECT object_id FROM CreditNote UNION ALL
SELECT object_id FROM GiftCertificate UNION ALL
SELECT object_id FROM MoneyCertificate UNION ALL
SELECT object_id FROM DiscountCertificate UNION ALL
SELECT object_id FROM BonusCertificate UNION ALL
SELECT object_id FROM Return UNION ALL
SELECT object_id FROM CustomerReturn UNION ALL
SELECT object_id FROM SupplierReturn UNION ALL
SELECT object_id FROM ConsignmentReturn UNION ALL
SELECT object_id FROM MerchandiseHierarchyTreeNodeReturn UNION ALL
SELECT object_id FROM PaymentReturn UNION ALL
SELECT object_id FROM Reservation UNION ALL
SELECT object_id FROM MerchandiseHierarchyTreeNodeReservation UNION ALL
SELECT object_id FROM CustomerReservation UNION ALL
SELECT object_id FROM PrepaidCustomerReservation UNION ALL
SELECT object_id FROM InitialEntranceCustomerReservation UNION ALL
SELECT object_id FROM NormalCustomerReservation UNION ALL
SELECT object_id FROM StoreReservation UNION ALL
SELECT object_id FROM Consignment UNION ALL
SELECT object_id FROM ConsignmentMerchandiseHierarchyTreeNode UNION ALL
SELECT object_id FROM Payment UNION ALL
SELECT object_id FROM CreditPayment UNION ALL
SELECT object_id FROM CompanyCreditPaymentMethod UNION ALL
SELECT object_id FROM BankCreditPaymentMethod UNION ALL
SELECT object_id FROM PaymentPaymentMethod UNION ALL
SELECT object_id FROM User UNION ALL
SELECT object_id FROM UserGroup UNION ALL
SELECT object_id FROM Profile UNION ALL
SELECT object_id FROM AccessControlList UNION ALL
SELECT object_id FROM AccessControlListItem UNION ALL
SELECT object_id FROM Bank UNION ALL
SELECT object_id FROM BankBranch UNION ALL
SELECT object_id FROM TransactionalMerchandise UNION ALL
SELECT object_id FROM Service UNION ALL
SELECT object_id FROM Insurance UNION ALL
SELECT object_id FROM Repair UNION ALL
SELECT object_id FROM ProductSet UNION ALL
SELECT object_id FROM SaleTransaction UNION ALL
SELECT object_id FROM SaleQuote UNION ALL
SELECT object_id FROM ShipmentMethod UNION ALL
SELECT object_id FROM Shipment UNION ALL
SELECT object_id FROM Transfer UNION ALL
SELECT object_id FROM ShipmentMethodSale UNION ALL
SELECT object_id FROM ShipmentMethodPurchase UNION ALL
SELECT object_id FROM FinancialAccount UNION ALL
SELECT object_id FROM BankAccount UNION ALL
SELECT object_id FROM PaypalAccount UNION ALL
SELECT object_id FROM CreditContract UNION ALL
SELECT object_id FROM Brand UNION ALL
SELECT object_id FROM Collection UNION ALL
SELECT object_id FROM Category UNION ALL
SELECT object_id FROM Material UNION ALL
SELECT object_id FROM Product UNION ALL
SELECT object_id FROM SubProduct UNION ALL
SELECT object_id FROM OrganizationalHierarchyMerchandiseSupplier UNION ALL
SELECT object_id FROM PointOfSale UNION ALL
SELECT object_id FROM RootEntity UNION ALL
SELECT object_id FROM Media UNION ALL
SELECT object_id FROM PersonRelation
)
GROUP BY object_id
HAVING count(1) > 1)
