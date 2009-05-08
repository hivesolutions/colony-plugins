select count(1) from price p, saletransaction s where p.object_id = s.price;
-- 5543
select count(1) from saletransaction where price is not null;
-- 5543
update saletransaction set price = null;
select count(1) from saletransaction where price is not null;
-- 0

select count(1) from purchasetransaction where cost is not null;
-- 733
update purchasetransaction set cost = null;
select count(1) from purchasetransaction where cost is not null;
-- 0
