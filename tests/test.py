import unittest
import pycorda
import sys
import os.path
import json

def tests_dir():
	return os.path.dirname(sys.argv[1])

def get_config():
	config_path = os.path.join(tests_dir(), 'config.json')
	
	with open(config_path) as config_file:
		return json.load(config_file)

class TestQueries(unittest.TestCase):
	@classmethod
	def setUpClass(cls):
		config = get_config()
		db_url = config['db_url']
		default_driver_path = os.path.join(tests_dir(), 'h2-1.4.200.jar')
		client_driver_path = config.get('client_driver_path', default_driver_path)
		cls.node = pycorda.Node(db_url, "sa", "", client_driver_path)	

	def test_single_table_query(self):
		df = self.node.get_node_attachments()
		table_value = df[df.ATT_ID == 'some_id'].iloc[0]['UPLOADER']
		self.assertEqual(table_value, 'app')

	def test_single_row_query(self):
		single_row = self.node.find_vault_states_by_transaction_id('1')
		no_row = self.node.find_vault_states_by_transaction_id('2')
		self.assertEqual(single_row.iloc[0]['TRANSACTION_ID'], '1')
		self.assertTrue(no_row.empty)
