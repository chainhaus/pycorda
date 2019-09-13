import pycorda as pyc

url = 'jdbc:h2:tcp://localhost:52504/node'
username = 'sa'
password = ''
node = pyc.Node(url, username, password)
print(node.get_node_infos())
node.close()

h2 = pyc.H2Tools()
ver = h2.get_latest_version()
print(ver)
h2.download_h2jar() # downloads latest h2 jar and stores in local folder as h2.jar
