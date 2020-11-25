# PyCorda
PyCorda is a framework for accessing data on the Corda DLT using Python. It includes the ability to quickly generate charts and graphs and will soon have machine learning capabilities. PyCorda is covered in-depth in the book **[Mastering Corda](https://www.amazon.com/Mastering-Corda-Building-Distributed-Applications/dp/149204718X/)**. The official website for PyCorda is **[PyCorda.com](http://PyCorda.com)**.

## Getting Involved
If you would like to be involved in PyCorda shoot an email to hello@chainhaus.com


# Using PyCorda

Access node and vault data for analytics using pandas DataFrames. Currently only works with H2 database. 
We'll be adding other DBs shortly and possibly support for queryable states.

## Example

```
import pycorda as pyc

url = 'jdbc:h2:tcp://localhost:52504/node'
username = 'sa'
password = ''
node = pyc.Node(url, username, password)
print(node.get_node_infos())
node.close()
```

## Installation

To get started using the PyCorda library, install it with

```
pip install pycorda
```

Note that you may need to install other required software, depending on your platform. See the platform specific instructions.

If there is a H2 server running with tcp connections allowed,
then you can connect to a database located at the JDBC url with:

```
from pycorda import Node
node = Node(url, username, password)
```

An h2.jar file is required in your projects local folder. If your H2 jar file is elsewhere in your filesystem, try this. This needs to be done only once:

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

## Testing

To run the tests, ensure the testing environment is properly configured and place the correct urls at tests/config.json.
You can then execute the following commands from the project directory:

```
python -m unittest tests.test
python -m unittest tests.test_invalid_driver
```

## Requirements

1. Currently supports 64-bit versions of Python 3 and JVMs only
2. Drop an H2 jar into your project file naming it h2.jar

## Windows

You will need to install the Microsoft C++ build tools downloaded from https://visualstudio.microsoft.com/visual-cpp-build-tools/.

## Ubuntu

Note that for Ubuntu, you may need to install wheel with

```
pip install wheel
python setup.py bdist_wheel
```

Also ensure you have gcc installed:

```
sudo apt-get update
sudo apt-get install gcc
```
