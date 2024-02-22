"""
Для каждого поля и валидатора в эндпоинте /registration напишите юнит-тест,
который проверит корректность работы валидатора. Таким образом, нужно проверить, что существуют наборы данных,
которые проходят валидацию, и такие, которые валидацию не проходят.
"""

import unittest
from hw1_registration import app

class RegistrationFormTest(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['DEBUG'] = False
        app.config['WTF_CSRF_ENABLED'] = False
        self.app = app.test_client()
        self.base_url = '/registration'

    def _login(self, name, email, phone, address, index, comment):
        return self.app.post(self.base_url, data=dict(
            name=name,
            email=email,
            phone=phone,
            address=address,
            index=index,
            comment=comment
        ))

    def test_register(self):
        response = self._login('Petrov V.V.',
                               'test@yandex.ru',
                               9999999999,
                               'Russia',
                               123,
                               'test')
        self.assertEqual(response.status_code, 200)

    def test_required_name(self):
        response = self._login(None,
                               'test@yandex.ru',
                               9999999999,
                               'Russia',
                               123,
                               'test')
        self.assertEqual(response.status_code, 400)

    def test_invalid_email(self):
        response = self._login('Petrov V.V.',
                               None,
                               9999999999,
                               'Russia',
                               123,
                               'test')
        self.assertEqual(response.status_code, 400)

    def test_invalid_phone(self):
        response = self._login('Petrov V.V.',
                               'test@yandex.ru',
                               None,
                               'Russia',
                               123,
                               'test')
        self.assertEqual(response.status_code, 400)

    def test_invalid_address(self):
        response = self._login('Petrov V.V.',
                               'test@yandex.ru',
                               9999999999,
                               None,
                               123,
                               'test')
        self.assertEqual(response.status_code, 400)

    def test_invalid_index(self):
        response = self._login('Petrov V.V.',
                               'test@yandex.ru',
                               9999999999,
                               'Russia',
                               None,
                               'test')
        self.assertEqual(response.status_code, 400)

if __name__ == '__main__':
    unittest.main()
