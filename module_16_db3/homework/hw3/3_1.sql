SELECT PC.model, price
FROM PC
JOIN Product ON PC.model = Product.model
WHERE Product.maker = "B"

UNION

SELECT Laptop.model, price
FROM Laptop
JOIN Product ON Laptop.model = Product.model
WHERE Product.maker = "B"

UNION

SELECT Printer.model, price
FROM Printer
JOIN Product ON Printer.model = Product.model
WHERE Product.maker = "B";
