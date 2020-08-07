import unittest
import pycorda
import sys
import os.path
import json

def tests_dir():
	return os.path.dirname(os.path.realpath(__file__))

def get_config():
	config_path = os.path.join(tests_dir(), 'config.json')
	
	with open(config_path) as config_file:
		return json.load(config_file)

def new_node(config):
	db_url = config['db_url']
	default_driver_path = os.path.join(tests_dir(), 'h2-1.4.200.jar')
	client_driver_path = config.get('client_driver_path', default_driver_path)
	return pycorda.Node(db_url, "sa", "", client_driver_path)

class TestQueries(unittest.TestCase):
	@classmethod
	def setUpClass(cls):
		config = get_config()
		cls.node = new_node(config)	

	def test_single_table_query(self):
		df = self.node.get_node_attachments()
		table_value = df[df.ATT_ID == 'some_id'].iloc[0]['UPLOADER']
		self.assertEqual(table_value, 'app')

	def test_single_row_query(self):
		single_row = self.node.find_vault_states_by_transaction_id('1')
		no_row = self.node.find_vault_states_by_transaction_id('2')
		self.assertEqual(single_row.iloc[0]['TRANSACTION_ID'], '1')
		self.assertTrue(no_row.empty)

	@classmethod
	def tearDownClass(cls):
		cls.node.close()

class TestJolokia(unittest.TestCase):
	@classmethod
	def setUpClass(cls):
		config = get_config()
		cls.node = new_node(config)
		cls.node.set_node_root(config['jolokia_agent_url'])
		cls.node.set_web_server_url(config['proxy_url'])

	def test_single_read(self):
		data = self.node.memory()
		self.assertEqual(data['value']['ObjectName']['objectName'], 'java.lang:type=Memory')

	def test_single_execute(self):
		data = self.node.rpc_server_browse()
		self.assertEqual(data['status'], 200)

	@classmethod
	def tearDownClass(cls):
		cls.node.close()

class TestOSExceptions(unittest.TestCase):
	def test_database_not_found(self):
		config = get_config()
		default_driver_path = os.path.join(tests_dir(), 'h2-1.4.200.jar')
		self.client_driver_path = config.get('client_driver_path', default_driver_path)
		self.assertBadDbUrl('')
		self.assertBadDbUrl('jdbc:h2:tcp')
		self.assertBadDbUrl('jdbc:h2:tcp://localhost:55555/')	

	def test_proxy_not_found(self):
		config = get_config()
		self.node = new_node(config)
		self.node.set_node_root(config['jolokia_agent_url'])
		self.assertBadProxyUrl('')
		self.assertBadProxyUrl('http://localhost:55555/')
		self.assertBadProxyUrl('http://127.0.12.85:55555/')

	def test_jolokia_node_not_found(self):
		config = get_config()
		self.node = new_node(config)
		self.node.set_web_server_url(config['proxy_url'])
		self.assertBadJolokiaUrl('')
		self.assertBadJolokiaUrl('http://localhost:55555/')
		self.assertBadJolokiaUrl('http://127.0.12.85:55555/')

	def assertBadDbUrl(self, url):
		self.assertRaises(OSError, pycorda.Node, url, "sa", "", self.client_driver_path)

	def assertBadProxyUrl(self, url):
		self.node.set_web_server_url(url)
		self.assertRaises(OSError, self.node.memory)

	def assertBadJolokiaUrl(self, url):
		self.node.set_node_root(url)
		self.assertRaises(OSError, self.node.memory)

