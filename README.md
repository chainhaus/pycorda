# PyCorda

Access node and vault data for analytics.

To get started using the PyCorda library, install it with

```
pip install pycorda
```
And drop an H2 jar into your project file naming it h2.jar

If there is a H2 server running with tcp connections allowed,
then you can connect to a database located at the JDBC url with:

```
from pycorda import Node
node = Node(url, username, password)
```

If your H2 jar file is elsewhere in your filesystem, try this:

```
from pycorda import Node
node = Node(url, username, password, path_to_jar)
```


Accepted JDBC urls are in the format jdbc:h2:tcp://hostname:portnumber/path_to_database.

## Requirements

Currently supports 64-bit versions of Python 3 and JVMs only
