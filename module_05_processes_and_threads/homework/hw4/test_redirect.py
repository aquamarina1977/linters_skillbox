import io
import sys
import unittest
from redirect import Redirect

class TestRedirect(unittest.TestCase):
    def test_redirect_stdout(self):
        out_stream = io.StringIO()
        with Redirect(stdout=out_stream):
            print("Redirecting stdout test")
        self.assertEqual(out_stream.getvalue(), "Redirecting stdout test\n")

    def test_redirect_stderr(self):
        err_stream = io.StringIO()
        with Redirect(stderr=err_stream):
            print("Redirecting stderr test", file=sys.stderr)
        self.assertEqual(err_stream.getvalue(), "Redirecting stderr test\n")

    def test_redirect_both(self):
        out_stream = io.StringIO()
        err_stream = io.StringIO()
        with Redirect(stdout=out_stream, stderr=err_stream):
            print("Redirecting both test")
            print("Error on both streams", file=sys.stderr)
        self.assertEqual(out_stream.getvalue(), "Redirecting both test\n")
        self.assertEqual(err_stream.getvalue(), "Error on both streams\n")

if __name__ == '__main__':
    unittest.main()