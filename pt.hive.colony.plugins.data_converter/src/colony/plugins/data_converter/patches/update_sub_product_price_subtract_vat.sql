-- 200905070000

-- the subproduct price was including vat when it should not

begin transaction;

update Price
   set value = round(value / 1.20, 2)
 where object_id in(
-- get all the sub product prices
select p.object_id
  from SubProduct s,
       MerchandiseContactableOrganizationalHierarchyTreeNode m,
       Price p
 where s.object_id = m.merchandise
   and m.price = p.object_id);

commit;
