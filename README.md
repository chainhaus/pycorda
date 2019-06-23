# PyCorda

## PyCorda.com
Access docs on PyCorda.com (coming soon)

## Usage
Access node and vault data for analytics. Currently only works with H2 database. I'll be adding other DBs shortly and possibly support for queryable states.

To get started using the PyCorda library, install it with

```
pip install pycorda
```


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

## Managing H2 Jars

An h2.jar file stored locally in the project folder is required. H2Tools allows you to pull
a jar programmatically. You'll need to do this once, so either manually or programmatically is fine
as long as the h2.jar file is there.

```
import pycorda as pyc
h2 = pyc.H2Tools()
ver = h2.get_latest_version()
print(ver)
h2.download_h2jar() # downloads latest h2 jar and stores in local folder as h2.jar
```

## Requirements

1. Currently supports 64-bit versions of Python 3 and JVMs only
2. Drop an H2 jar into your project file naming it h2.jar
