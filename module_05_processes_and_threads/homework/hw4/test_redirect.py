import unittest
from redirect import Redirect
class TestRedirect(unittest.TestCase):

    def test_stdout_redirected_when_using_with_statement(self):
        with open('test.txt', 'w') as f:
            with Redirect(stdout=f):
                print("This is a test")

        with open('test.txt', 'r') as f:
            content = f.read()

        self.assertEqual(content, "This is a test\n")

    def test_stderr_redirected_when_using_with_statement(self):
        with open('test.txt', 'w') as f:
            with Redirect(stderr=f):
                raise ValueError("An error occurred")

        with open('test.txt', 'r') as f:
            content = f.read()

        self.assertEqual(content, "An error occurred\n")

    def test_stdout_and_stderr_redirected_when_using_with_statement(self):
        with open('test.txt', 'w') as f:
            with Redirect(stdout=f, stderr=f):
                print("Output to stdout")
                raise ValueError("An error occurred")

        with open('test.txt', 'r') as f:
            content = f.read()

        expected_output = """Output to stdout
An error occurred
"""
        self.assertEqual(content, expected_output)

if __name__ == '__main__':
    unittest.main()
    # with open('test_results.txt', 'a') as test_file_stream:
    #     runner = unittest.TextTestRunner(stream=test_file_stream)
    #     unittest.main(testRunner=runner)
