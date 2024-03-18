import unittest
from block_errors import BlockErrors

err_types = {ZeroDivisionError}
outer_err_types = {TypeError}

class TestBlockErrors(unittest.TestCase):

    def test_error_passes_through(self):
        with self.assertRaises(TypeError):
            with BlockErrors(err_types):
                a = 1 / '0'

    def test_nested_blocks(self):
        with BlockErrors(outer_err_types):
            with BlockErrors(err_types):
                with self.assertRaises(TypeError):
                    a = 1 / '0'

    def test_child_errors_ignored(self):
        with BlockErrors(err_types):
            with self.assertRaises(ZeroDivisionError):
                a = 1 / 0

if __name__ == '__main__':
    unittest.main()
