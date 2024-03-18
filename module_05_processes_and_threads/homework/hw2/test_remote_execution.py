import unittest
from remote_execution import run_python_code_in_subprocess

class TestRunPythonCodeInSubprocess(unittest.TestCase):

    def test_code_output(self):
        output, _, _ = run_python_code_in_subprocess("print('Hello, World!')", 5)
        self.assertEqual(output.strip(), "Hello, World!")

    def test_code_timeout(self):
        _, errors, was_killed_by_timeout = run_python_code_in_subprocess("import time\n\nwhile True:\n    pass", 3)
        self.assertTrue(was_killed_by_timeout)
        self.assertIn("", errors)

if __name__ == '__main__':
    unittest.main()
