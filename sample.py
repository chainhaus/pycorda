from pycorda import Node

url = 'jdbc:h2:tcp://localhost:52504/node'
username = 'sa'
password = ''
node = Node(url, username, password)
print(node.get_node_infos())
node.close()
