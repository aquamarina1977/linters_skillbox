import unittest
from datetime import datetime

from hello_word_with_day import app, GREETINGS


class AppTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_weekday_greeting(self):
        with app.test_request_context():
            weekday = datetime.today().weekday()
            greeting = GREETINGS[weekday]

            response = self.app.get('/hello-world/John')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.data.decode(), f'Привет, John. {greeting}!')

    def test_invalid_username(self):
        response = self.app.get('/hello-world/Хорошей среды')
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()