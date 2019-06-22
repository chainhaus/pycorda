# PyCorda

Access node and vault data for analytics.

To get started using the PyCorda library, install it with

```
pip install pycorda
```

If there is a H2 server running with tcp connections allowed,
then you can connect to a database located at the JDBC url with

```
from pycorda import Node
node = Node(url, username, password)
```

Accepted JDBC urls are in the format jdbc:h2:tcp://hostname:portnumber/path_to_database.

Currently only support 64-bit versions of Python 3 and JVM
