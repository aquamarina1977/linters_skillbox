import datetime
import unittest
from person import Person

class TestPerson(unittest.TestCase):
    def setUp(self):
        self.person = Person('Ivan Petrov', 1990, 'Mira Street, 285')
    def test_get_age(self):
        now = datetime.datetime.now()
        expected_age = now.year - 1990

        actual_age = self.person.age()

        self.assertEqual(actual_age, expected_age)
    def test_get_name(self):
        name = self.person.name()
        self.assertEqual(name, 'Ivan Petrov')
    def test_set_name(self):
        self.person.name('Katya Rodnina')
        name = self.person.name()
        self.assertEqual(name, 'Katya Rodnina')
    def test_set_address(self):
        self.person.address('Lenina Street, 87')
        address = self.person.address()
        self.assertEqual(address, 'Lenina Street, 87')
    def test_is_homeless_true(self):
        homeless_person = Person('Homeless', 1985)
        self.assertTrue(homeless_person.is_homeless())
    def test_is_homeless_false(self):
        homeless_person = Person('Denis R.', 1985, 'Pushkina St., 25')
        self.assertFalse(homeless_person.is_homeless())


if __name__ == '__main__':
    unittest.main()