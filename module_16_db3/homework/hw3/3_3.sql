SELECT class AS head_ship
FROM Classes
WHERE class IN (SELECT name FROM Ships
	        UNION
	        SELECT ship FROM Outcomes);
