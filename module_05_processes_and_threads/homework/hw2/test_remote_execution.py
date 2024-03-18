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

# import unittest
# from remote_execution import app
#
#
# class TestRemoteExecution(unittest.TestCase):
#     @classmethod
#     def setUpClass(cls) -> None:
#         app.config['TESTING'] = True
#         app.config['DEBUG'] = False
#         cls.app = app.test_client()
#         cls.base_url = '/run_code'
#
#     def test_hello_world(self):
#         response = self.app.post(self.base_url, data=dict(
#             code="print('Hello world')"
#         ))
#         self.assertEqual(response.status_code, 200)
#
#         result: dict = response.json
#         self.assertFalse(result['timelimit'])
#         self.assertEqual(result['stdout'], 'Hello world\n')
#         self.assertEqual(result['stderr'], '')
#
#     def test_timelimit(self):
#         response = self.app.post(self.base_url, data=dict(
#             code="import time; time.sleep(5)",
#             timeout=5
#         ))
#         self.assertEqual(response.status_code, 200)
#
#         result: dict = response.json
#         self.assertTrue(result['timelimit'])
#
#     def test_invalid_data(self):
#         _INVALID = (
#             ('Empty data', dict()),
#             ('Code as number', dict(code=1)),
#             ('Negative timeout', dict(code="Code", timeout=-1)),
#             ('Timeout as string', dict(code="Code", timeout="1"))
#         )
#         for title, data in _INVALID:
#             with self.subTest(title):
#                 response = self.app.post(self.base_url)
#                 self.assertEqual( response.status_code, 400)
#
#     def test_code_unsafe(self):
#         response = self.app.post(self.base_url, data=dict(
#             code='print()"; echo "hacked'
#         ))
#         result: dict = response.json
#         self.assertNotEqual(result['stderr'], '')
#         self.assertEqual(result['stdout'], '')
#
#
# if __name__ == '__main__':
#     unittest.main()