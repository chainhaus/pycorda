import unittest
import pycorda
import sys
import os.path
import json

class TestQueries(unittest.TestCase):
	@classmethod
	def load_config(cls):
		tests_dir = os.path.dirname(sys.argv[1])
		config_path = os.path.join(tests_dir, 'config.json')
		default_driver_path = os.path.join(tests_dir, 'h2-1.4.200.jar')
		with open(config_path) as config_file:
			config = json.load(config_file)
		cls.db_url = config['db_url']
		cls.client_driver_path = config.get('client_driver_path', default_driver_path)

	@classmethod
	def setUpClass(cls):
		cls.load_config()
		cls.node = pycorda.Node(cls.db_url, "sa", "", cls.client_driver_path)	

	def test_single_table_query(self):
		df = self.node.get_node_attachments()
		table_value = df[df.ATT_ID == 'some_id'].iloc[0]['UPLOADER']
		self.assertEqual(table_value, 'app')

	def test_single_row_query(self):
		single_row = self.node.find_vault_states_by_transaction_id('1')
		no_row = self.node.find_vault_states_by_transaction_id('2')
		self.assertEqual(single_row.iloc[0]['TRANSACTION_ID'], '1')
		self.assertTrue(no_row.empty)
