import unittest
from decrypt import decrypt

class DecryptTest(unittest.TestCase):

    def test_one_dot(self):
        encryption = "абра-кадабра."
        expected = "абра-кадабра"
        self.assertEqual(decrypt(encryption), expected)

    def test_two_dots(self):
        encryption = "абраа..-кадабра"
        expected = "абра-кадабра"
        self.assertEqual(decrypt(encryption), expected)

    def test_dot_in_between(self):
        encryption = "абраа..-.кадабра"
        expected = "абра-кадабра"
        self.assertEqual(decrypt(encryption), expected)

    def test_multiple_dashes(self):
        encryption = "абра--..кадабра"
        expected = "абра-кадабра"
        self.assertEqual(decrypt(encryption), expected)

    def test_dot_at_start(self):
        encryption = "абрау...-кадабра"
        expected = "абра-кадабра"
        self.assertEqual(decrypt(encryption), expected)

    def test_only_dots(self):
        encryption = "абра........"
        expected = ""
        self.assertEqual(decrypt(encryption), expected)

    def test_dot_with_other_symbols(self):
        encryption = "абр......a."
        expected = "a"
        self.assertEqual(decrypt(encryption), expected)

    def test_multiple_digits(self):
        encryption = "1..2.3"
        expected = "23"
        self.assertEqual(decrypt(encryption), expected)

    def test_only_dot(self):
        encryption = "."
        expected = ""
        self.assertEqual(decrypt(encryption), expected)

    def test_long_string_of_dots(self):
        encryption = "1......................."
        expected = ""
        self.assertEqual(decrypt(encryption), expected)


if __name__ == '__main__':
    unittest.main()