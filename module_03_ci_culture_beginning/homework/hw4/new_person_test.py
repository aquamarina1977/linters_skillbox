import unittest
import datetime
from person import Person

class PersonTestCase(unittest.TestCase):
    def setUp(self):
        self.person = Person("John", 1990, "123 Main St")

    def test_age(self):
        self.assertEqual(self.person.age, datetime.datetime.now().year - 1990)

    def test_name(self):
        self.assertEqual(self.person.name, "John")
        self.person.name = "Alice"
        self.assertEqual(self.person.name, "Alice")

    def test_address(self):
        self.assertEqual(self.person.address, "123 Main St")
        self.person.address = "456 Elm St"
        self.assertEqual(self.person.address, "456 Elm St")

    def test_is_homeless(self):
        self.assertFalse(self.person.is_homeless())
        self.person.address = ""
        self.assertTrue(self.person.is_homeless())


if __name__ == "__main__":
    unittest.main()