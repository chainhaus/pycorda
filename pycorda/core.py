import os
import pandas as pd
import jaydebeapi
import sys
import requests
import jks
import base64, textwrap
import time
from jpype import JException
from xml.etree import ElementTree
from jolokia import JolokiaClient

class H2Tools(object):
	def get_latest_version(self):
		"""Returns the latest version string for the h2 database"""
		r = requests.get('http://central.maven.org/maven2/com/h2database/h2/maven-metadata.xml')
		tree = ElementTree.fromstring(r.content)
		return tree.find('versioning').find('latest').text

	def get_h2jar_url(self,version):
		url = "http://central.maven.org/maven2/com/h2database/h2/"
		url += version + "/h2-" + version + ".jar"
		return url

	def download_h2jar(self,filepath='./h2.jar', version=None):
		"""Downloads h2 jar and copies it to a file in filepath"""
		if version is None:
			version = self.get_latest_version()
		r = requests.get(self.get_h2jar_url(version))
		with open(filepath, 'wb') as jarfile:
			jarfile.write(r.content)

class Node(object):
	"""Node object for connecting to H2 database and getting table dataframes

	Use get_tbname methods to get dataframe for table TBNAME. For example,
	calling node.get_vault_states() will return the dataframe for VAULT_STATES.
	After using the node, call the close() method to close the connection.
	"""

	# --- Notes for future support of PostgreSQL clients ---
	# To support pg clients, url must be parsed into psycopg2.connect arguments
	# and the password must not be empty
	# After parsing, use "self._conn = psycopg2.connect(...)"

	# --- Notes regarding get methods ---
	# If table names will change often, it may be worth to
	# dynamically generate methods with some careful metaprogramming

	def __init__(self, url, username, password, path_to_jar='./h2.jar',node_root=None,web_server_url=None,name=''):
		"""
        Parameters
        ----------
        url : str
            JDBC url to be connected
        username : str
            username of database user
        passowrd : str
            password of database user
        path_to_jar : str
        	path to h2 jar file
        """

		self.set_name(name)
		self._conn = jaydebeapi.connect(
			"org.h2.Driver",
			url,
			[username, password],
			path_to_jar,
		)

		self._curs = self._conn.cursor()
		if  node_root != None:
			self.set_node_root(node_root)
		if web_server_url != None:
			self.set_web_server_url(web_server_url)

		self.rpc_server_nid = 'org.apache.activemq.artemis:broker="RPC",component=addresses,address="rpc.server",subcomponent=queues,routing-type="multicast",queue="rpc.server"'
	
	def set_name(self,name):
		self._name = name
	def send_api_get_request(self, api_path):
		if self._web_server_url != None:
			request_url = self._web_server_url + api_path
			resp = requests.get(request_url)
			return resp.text
		else:
			return "No web_server set i.e. http://localhost:10007. Call set_web_server_url()"

	def send_api_post_request(self, api_path, data):
		if self._web_server_url != None:
			request_url = self._web_server_url + api_path
			resp = requests.post(request_url, json=data)
			return resp.json()
		else:
			return "No web_server set i.e. http://localhost:10007. Call set_web_server_url()"
	
	def set_web_server_url(self,web_server_url):
		self._web_server_url = web_server_url

	def set_node_root(self,node_root):
		self._node_root = node_root
		self._node_cert = node_root + '/certificates'
		self._node_cert_jks = self._node_cert + '/nodekeystore.jks'

	def display_keys_from_jks(self,password='cordacadevpass'):
		ks = jks.KeyStore.load(self._node_cert_jks,password)
		columns = ['ALIAS','PRIVATE_KEY']
		keys = pd.DataFrame([],columns=columns)
		for alias, pk in ks.private_keys.items():
			#keys = keys.append([[alias,pk.pkey_pkcs8,'PK']])
			df = pd.DataFrame([[alias,base64.b64encode(pk.pkey_pkcs8).decode('ascii')]],columns=columns)
			keys = keys.append(df,ignore_index=True)
		return keys

	def _get_df(self, table_name):
		"""Gets pandas dataframe from a table

		Parameters
        ----------
        table_name : str
            name of table in database
		"""
		self._curs.execute("SELECT * FROM " + table_name)
		columns = [desc[0] for desc in self._curs.description] # column names
		return pd.DataFrame(self._curs.fetchall(), columns=columns)

	def get_node_attachments(self):
		return self._get_df("NODE_ATTACHMENTS")

	def get_node_attachments_contracts(self):
		return self._get_df("NODE_ATTACHMENTS_CONTRACTS")

	def get_node_checkpoints(self):
		return self._get_df("NODE_CHECKPOINTS")

	def get_node_contract_upgrades(self):
		return self._get_df("NODE_CONTRACT_UPGRADES")

	def get_node_indentities(self):
		return self._get_df("NODE_IDENTITIES")

	def get_node_infos(self):
		return self._get_df("NODE_INFOS")

	def get_node_info_hosts(self):
		return self._get_df("NODE_INFO_HOSTS")

	def get_node_info_party_cert(self):
		return self._get_df("NODE_INFO_PARTY_CERT")

	def get_node_link_nodeinfo_party(self):
		return self._get_df("NODE_LINK_NODEINFO_PARTY")

	def get_node_message_ids(self):
		return self._get_df("NODE_MESSAGE_IDS")

	def get_node_message_retry(self):
		return self._get_df("NODE_MESSAGE_RETRY")

	def get_node_named_identities(self):
		return self._get_df("NODE_NAMED_IDENTITIES")

	def get_node_our_key_pairs(self):
		return self._get_df("NODE_OUR_KEY_PAIRS")

	def get_node_properties(self):
		return self._get_df("NODE_PROPERTIES")

	def get_node_scheduled_states(self):
		return self._get_df("NODE_SCHEDULED_STATES")

	def get_node_transactions(self):
		return self._get_df("NODE_TRANSACTIONS")

	def get_node_transaction_mappings(self):
		return self._get_df("NODE_TRANSACTION_MAPPINGS")

	def get_vault_fungible_states(self):
		return self._get_df("VAULT_FUNGIBLE_STATES")

	def get_vault_fungible_states_parts(self):
		return self._get_df("VAULT_FUNGIBLE_STATES_PARTS")

	def get_vault_linear_states(self):
		return self._get_df("VAULT_LINEAR_STATES")

	def get_vault_linear_states_parts(self):
		return self._get_df("VAULT_LINEAR_STATES_PARTS")

	def get_vault_states(self):
		return self._get_df("VAULT_STATES")

	def get_vault_transaction_notes(self):
		return self._get_df("VAULT_TRANSACTION_NOTES")

	def get_state_party(self):
		return self._get_df("STATE_PARTY")

	def _snapshot_headers(self,header):
		return '\r\n\r\n -----------------  ' + header + ' \r\n'

	def find_transactions_by_linear_id(self,linear_id):
		linear_states = self.get_vault_linear_states()
		return linear_states[linear_states.UUID==linear_id]
	
	def find_vault_states_by_transaction_id(self,tx_id):
		vault_states = self.get_vault_states()
		return vault_states[vault_states.TRANSACTION_ID==tx_id]

	def find_vault_fungible_states_by_transaction_id(self,tx_id):
		vault_states = self.get_vault_fungible_states()
		return vault_states[vault_states.TRANSACTION_ID==tx_id]

	def find_vault_fungible_states_by_issuer(self,issuer):
		vault_states = self.get_vault_fungible_states()
		return vault_states[vault_states.ISSUER_NAME==issuer]


	def find_unconsumed_states_by_contract_state(self,contract_state_class_name):
		unconsumed_states = self.get_vault_states()
		return unconsumed_states[unconsumed_states.CONSUMED_TIMESTAMP.isnull()][unconsumed_states.CONTRACT_STATE_CLASS_NAME==contract_state_class_name]

	def find_linear_id_by_transaction_id(self,tx_id):
		linear_states = self.get_vault_linear_states()
		linear = linear_states[linear_states.TRANSACTION_ID==tx_id]
		return linear.iloc[0]['LINEAR_ID']

	def jolokia_read(self, nid):
		payload = {'url': self._node_root + "jolokia/", 'nid': nid}
		return self.send_api_post_request("jolokia/read", payload)

	def jolokia_execute(self, nid, operation):
		payload = {'url': self._node_root + "jolokia/", 'nid': nid, 'operation': operation}
		return self.send_api_post_request("jolokia/execute", payload)

	def memory(self):
		return self.jolokia_read("java.lang:type=Memory")

	def operating_system(self):
		return self.jolokia_read("java.lang:type=OperatingSystem")

	def runtime(self):
		return self.jolokia_read("java.lang:type=Runtime")

	def mbean_servers_info(self):
		return self.jolokia_execute("jolokia:type=ServerHandler", "mBeanServersInfo()")

	def attachments(self):
		return self.jolokia_read("net.corda:name=Attachments")

	def flows_started(self):
		return self.jolokia_read("net.corda:type=Flows,name=Started")

	def flows_in_flight(self):
		return self.jolokia_read("net.corda:type=Flows,name=InFlight")

	def flows_finished(slef):
		return self.jolokia_read("net.corda:type=Flows,name=Finished")

	def flows_checkpointing_rate(self):
		return self.jolokia_read("net.corda:type=Flows,name=Checkpointing Rate")

	def flows_checkpoint_volume_bytes_per_second_hist(self):
		return self.jolokia_read("net.corda:type=Flows,name=CheckpointVolumeBytesPerSecondHist")

	def flows_checkpoint_volume_bytes_per_second_current(self):
		return self.jolokia_read("net.corda:type=Flows,name=CheckpointVolumeBytesPerSecondCurrent")

	def hikari_pool_usage(self):
		return self.jolokia_read("net.corda:type=HikariPool-1,name=pool.Usage")

	def rpc_server(slef):
		return self.jolokia_read(self.rpc_server_nid)

	def rpc_server_browse(self):
		return self.jolokia_execute(self.rpc_server_nid, "browse()")

	def rpc_server_pause(self):
		return self.jolokia_execute(self.rpc_server_nid, "pause()")

	def rpc_server_resume(self):
		return self.jolokia_execute(self.rpc_server_nid, "resume()")

	def rpc_server_count_messages(self):
		return self.jolokia_execute(self.rpc_server_nid, "countMessages()")

	def log4j2(self):
		return self.jolokia_read("org.apache.logging.log4j2:type=*")

	def generate_snapshot(self,filename=None):
		if filename == None:
			filename = time.strftime(self._name+'-pycorda-snapshot-%Y%m%d-%H%M%S.log')
		f = open(filename,"w+")

		f.write(self._snapshot_headers('STATE_PARTY'))
		self.get_state_party().to_string(buf=f)
		
		f.write(self._snapshot_headers('NODE_ATTACHMENT'))
		self.get_node_attachments().to_string(buf=f)

		f.write(self._snapshot_headers('NODE_ATTACHMENT_CONTRACTS'))
		self.get_node_attachments_contracts().to_string(buf=f)

		f.write(self._snapshot_headers('NODE_CHECKPOINTS'))
		self.get_node_checkpoints().to_string(buf=f)
	
		f.write(self._snapshot_headers('NODE_CONTRACT_UPGRADES'))
		self.get_node_contract_upgrades().to_string(buf=f)
		
		f.write(self._snapshot_headers('NODE_IDENTITIES'))		
		self.get_node_indentities().to_string(buf=f)
		
		f.write(self._snapshot_headers('NODE_INFOS'))
		self.get_node_infos().to_string(buf=f)
		
		f.write(self._snapshot_headers('NODE_INFO_HOSTS'))
		self.get_node_info_hosts().to_string(buf=f)
		
		f.write(self._snapshot_headers('NODE_INFO_PARTY_CERT'))
		self.get_node_info_party_cert().to_string(buf=f)
		
		f.write(self._snapshot_headers('NODE_LINK_NODEINFO_PARTY'))
		self.get_node_link_nodeinfo_party().to_string(buf=f)
		
		f.write(self._snapshot_headers('NODE_MESSAGE_IDS'))
		self.get_node_message_ids().to_string(buf=f)
		
		#f.write(self._snapshot_headers('NODE_IDENTITIES'))
		#self.get_node_message_retry()) - NEEDS TO BE REMOVED?
		
		f.write(self._snapshot_headers('NODE_NAMED_IDENTITIES'))
		self.get_node_named_identities().to_string(buf=f)
		
		f.write(self._snapshot_headers('NODE_OUR_KEY_PAIRS'))
		self.get_node_our_key_pairs().to_string(buf=f)
		
		f.write(self._snapshot_headers('NODE_PROPERTIES'))
		self.get_node_properties().to_string(buf=f)
		
		f.write(self._snapshot_headers('NODE_SCHEDULED_STATES'))
		self.get_node_scheduled_states().to_string(buf=f)
		
		f.write(self._snapshot_headers('NODE_TRANSACTIONS'))
		self.get_node_transactions().to_string(buf=f)
		
		#f.write(self._snapshot_headers('NODE_IDENTITIES'))
		#self.get_node_transaction_mappings()) - ??

		f.write(self._snapshot_headers('VAULT_FUNGIBLE_STATES'))
		self.get_vault_fungible_states().to_string(buf=f)
		
		f.write(self._snapshot_headers('VAULT_FUNGIBLE_STATES_PARTS'))
		self.get_vault_fungible_states_parts().to_string(buf=f)
		
		f.write(self._snapshot_headers('VAULT_LINEAR_STATES'))
		self.get_vault_linear_states().to_string(buf=f)
		
		f.write(self._snapshot_headers('VAULT_LINEAR_STATES_PARTS'))
		self.get_vault_linear_states_parts().to_string(buf=f)
		
		f.write(self._snapshot_headers('VAULT_STATES'))
		self.get_vault_states().to_string(buf=f)
		
		f.write(self._snapshot_headers('VAULT_TRANSACTION_NOTES'))
		self.get_vault_transaction_notes().to_string(buf=f)
		
		
		f.close()

	def close(self):
		"""Closes the connection to the database"""
		self._curs.close()
		self._conn.close()

def print_pem(der_bytes, type):
	print("-----BEGIN %s-----" % type)
	print("\r\n".join(textwrap.wrap(base64.b64encode(der_bytes).decode('ascii'), 64)))
	print("-----END %s-----" % type)