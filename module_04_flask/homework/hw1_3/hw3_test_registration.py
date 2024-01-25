"""
Для каждого поля и валидатора в эндпоинте /registration напишите юнит-тест,
который проверит корректность работы валидатора. Таким образом, нужно проверить, что существуют наборы данных,
которые проходят валидацию, и такие, которые валидацию не проходят.
"""

import unittest
from hw1_registration import app, RegistrationForm

class RegistrationFormTest(unittest.TestCase):
    def test_valid_email(self):
        with app.test_client() as client:
            response = client.post('/registration', data=dict(
                email='test@example.com',
                phone=1234567890,
                name='John Doe',
                address='123 Main St',
                index=12345,
                comment=''
            ))
            self.assertEqual(response.status_code, 200)

    def test_invalid_email(self):
        with app.test_client() as client:
            response = client.post('/registration', data=dict(
                email='test',
                phone=1234567890,
                name='John Doe',
                address='123 Main St',
                index=12345,
                comment=''
            ))
            self.assertEqual(response.status_code, 400)

    def test_valid_phone(self):
        with app.test_client() as client:
            response = client.post('/registration', data=dict(
                email='test@example.com',
                phone=1234567890,
                name='John Doe',
                address='123 Main St',
                index=12345,
                comment=''
            ))
            self.assertEqual(response.status_code, 200)

    def test_invalid_phone(self):
        with app.test_client() as client:
            response = client.post('/registration', data=dict(
                email='test@example.com',
                phone=1234,
                name='John Doe',
                address='123 Main St',
                index=12345,
                comment=''
            ))
            self.assertEqual(response.status_code, 400)

    def test_valid_name(self):
        with app.test_client() as client:
            response = client.post('/registration', data=dict(
                email='test@example.com',
                phone=1234567890,
                name='John Doe',
                address='123 Main St',
                index=12345,
                comment=''
            ))
            self.assertEqual(response.status_code, 200)

    def test_invalid_name(self):
        with app.test_client() as client:
            response = client.post('/registration', data=dict(
                email='test@example.com',
                phone=1234567890,
                name='',
                address='123 Main St',
                index=12345,
                comment=''
            ))
            self.assertEqual(response.status_code, 400)

    def test_valid_address(self):
        with app.test_client() as client:
            response = client.post('/registration', data=dict(
                email='test@example.com',
                phone=1234567890,
                name='John Doe',
                address='123 Main St',
                index=12345,
                comment=''
            ))
            self.assertEqual(response.status_code, 200)

    def test_invalid_address(self):
        with app.test_client() as client:
            response = client.post('/registration', data=dict(
                email='test@example.com',
                phone=1234567890,
                name='John Doe',
                address='',
                index=12345,
                comment=''
            ))
            self.assertEqual(response.status_code, 400)

    def test_valid_index(self):
        with app.test_client() as client:
            response = client.post('/registration', data=dict(
                email='test@example.com',
                phone=1234567890,
                name='John Doe',
                address='123 Main St',
                index=12345,
                comment=''
            ))
            self.assertEqual(response.status_code, 200)

    def test_invalid_index(self):
        with app.test_client() as client:
            response = client.post('/registration', data=dict(
                email='test@example.com',
                phone=1234567890,
                name='John Doe',
                address='123 Main St',
                index='',
                comment=''
            ))
            self.assertEqual(response.status_code, 400)

    def test_valid_comment(self):
        with app.test_client() as client:
            response = client.post('/registration', data=dict(
                email='test@example.com',
                phone=1234567890,
                name='John Doe',
                address='123 Main St',
                index=12345,
                comment='Test comment'
            ))
            self.assertEqual(response.status_code, 200)

    def test_invalid_comment(self):
        with app.test_client() as client:
            response = client.post('/registration', data=dict(
                email='test@example.com',
                phone=1234567890,
                name='John Doe',
                address='123 Main St',
                index=12345,
                comment=None
            ))
            self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
