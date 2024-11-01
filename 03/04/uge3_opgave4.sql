


select * from products 
    order by UnitPrice;



select * from customers 
    where country = 'UK' 
        or country = 'spain';


select * from products 
    where UnitsInStock > 100 
        and UnitPrice >= 25;


select distinct ShipCountry from orders;


select * from orders 
    where month(OrderDate) = 10 
        and year(OrderDate) = 1996;


select * from orders  
    where ShipRegion is null 
        and ShipCountry = 'germany' 
        and Freight >= 100 
        and EmployeeID = 1 
        and year(OrderDate) = 1996; 


select * from orders 
    where ShippedDate > RequiredDate;


select * from orders
    where year(OrderDate) = 1997
        and month(OrderDate) <= 4
        and ShipCountry = 'canada';


select * from orders 
    where EmployeeID in (2,5,8)
        and ShipRegion is not null
        and ShipVia in (1,3)
    order by EmployeeID asc, ShipVia asc;


select * from employees
    where Region is null
        and year(BirthDate) <= 1960;