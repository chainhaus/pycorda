import os
import pandas
import jaydebeapi

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

	def __init__(self, url, username, password, path_to_jar='./h2.jar'):
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

		self._conn = jaydebeapi.connect(
			"org.h2.Driver",
			url,
			[username, password],
			path_to_jar,
		)

		self._curs = self._conn.cursor()

	def _get_df(self, table_name):
		"""Gets pandas dataframe from a table

		Parameters
        ----------
        table_name : str
            name of table in database
		"""
		self._curs.execute("SELECT * FROM " + table_name)
		columns = [desc[0] for desc in self._curs.description] # column names
		return pandas.DataFrame(self._curs.fetchall(), columns=columns)

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

	def get_node_names_identities(self):
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

	def close(self):
		"""Closes the connection to the database"""
		self._curs.close()
		self._conn.close()