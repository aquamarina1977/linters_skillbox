import unittest
from remote_execution import app

class TestApp(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    def test_run_code_endpoint(self):
        response = self.app.post('/run_code', data=dict(code='print("Hello, World!")', timeout=5))
        data = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertIn('stdout', data)
        self.assertIn('stderr', data)
        self.assertIn('timeout', data)

        self.assertEqual(data['stdout'], b'Hello, World!\n')
        self.assertEqual(data['stderr'], b'')
        self.assertFalse(data['timeout'])

if __name__ == '__main__':
    unittest.main()
