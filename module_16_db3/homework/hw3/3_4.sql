SELECT DISTINCT Battles.name
FROM Battles JOIN ON Battles.name = Outcomes.battle
JOIN Ships ON Ships.name = Outcomes.ship
WHERE Ships.class = 'Kongo';
