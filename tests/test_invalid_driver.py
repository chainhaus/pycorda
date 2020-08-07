from tests.test import get_config
import unittest
import pycorda

class TestInvalidDriver(unittest.TestCase):
	def test_invalid_driver(self):
		config = get_config()
		with self.assertRaises(OSError):
			pycorda.Node(config['db_url'], 'sa', '', 'fake_driver_path.jar')