import unittest
from finance import app, storage
class AppTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        storage[2024] = {1: {17: 150}}

    def test_add_endpoint(self):
        with app.test_client() as client:
            response = client.get("/add/20220501/50")
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.data.decode(), "Expense added successfully!")

            self.assertEqual(storage[2024][1][17], 150)

    def test_calculate_year_endpoint(self):
        with app.test_client() as client:
            response = client.get("/calculate/2022")
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.data.decode(), "No expenses found for 2022")

    def test_calculate_month_endpoint(self):
        with app.test_client() as client:
            response = client.get("/calculate/2022/2")
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.data.decode(), "No expenses found for 2022/2")

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