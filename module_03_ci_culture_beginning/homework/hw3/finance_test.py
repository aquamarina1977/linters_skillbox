from flask import Flask
import unittest

app = Flask(__name__)

storage = {}


@app.route("/add/<date>/<int:number>")
def add(date: str, number: int):
    year = int(date[:4])
    month = int(date[4:6])
    day = int(date[6:])

    expense = storage.setdefault(year, {}).setdefault(month, {}).get(day, 0)
    storage[year][month][day] = expense + number

    return "Expense added successfully!"


@app.route("/calculate/<int:year>")
def calculate_year(year: int):
    if year in storage:
        total = 0
        for month in storage[year]:
            for day in storage[year][month]:
                total += storage[year][month][day]
        return f"Total expenses in {year}: {total}"
    else:
        return f"No expenses found for {year}"


@app.route("/calculate/<int:year>/<int:month>")
def calculate_month(year: int, month: int):
    if year in storage and month in storage[year]:
        total = 0
        for day in storage[year][month]:
            total += storage[year][month][day]
        return f"Total expenses in {year}/{month}: {total}"
    else:
        return f"No expenses found for {year}/{month}"


class AppTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        storage[2022] = {1: {1: 100, 2: 200}, 2: {1: 150, 28: 300}}

    def test_add_endpoint(self):
        with app.test_client() as client:
            response = client.get("/add/20220501/50")
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.data.decode(), "Expense added successfully!")

            self.assertEqual(storage[2022][5][1], 150)

    def test_calculate_year_endpoint(self):
        with app.test_client() as client:
            response = client.get("/calculate/2022")
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.data.decode(), "Total expenses in 2022: 750")

    def test_calculate_month_endpoint(self):
        with app.test_client() as client:
            response = client.get("/calculate/2022/2")
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.data.decode(), "Total expenses in 2022/2: 450")

    def test_add_endpoint_invalid_date_format(self):
        with app.test_client() as client:
            response = client.get("/add/2022-05-01/50")
            self.assertEqual(response.status_code, 404)
            self.assertEqual(response.data.decode(), "Not Found")

    def test_calculate_year_endpoint_no_expenses(self):
        with app.test_client() as client:
            response = client.get("/calculate/2023")
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.data.decode(), "No expenses found for 2023")

    def test_calculate_month_endpoint_no_expenses(self):
        with app.test_client() as client:
            response = client.get("/calculate/2022/3")
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.data.decode(), "No expenses found for 2022/3")


if __name__ == "__main__":
    unittest.main()