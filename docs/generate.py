import os
import sys

sys.path.insert(0, os.path.abspath("../.."))

src_path = os.path.join("..", "src", "millenniumdb_driver_python")

index_content = """\
.. include:: ../README.rst

Welcome to the MillenniumDB Python Driver documentation!
=========================================================

.. note::

   This project is under active development.

Installation
------------

First install it using pip:

.. code-block:: console

   $ pip install millenniumdb_driver_python

Usage
-----

Creating a Driver instance:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

First you must create a ``Driver`` instance:

.. code-block:: console

   url = 'URL for the MillenniumDB server'
   driver = millenniumdb_driver_python.driver(url)

When you are done with the driver, you should close it before exiting the application.

.. code-block:: console

   driver.close()

Acquiring a Session:
~~~~~~~~~~~~~~~~~~~~~

For sending queries to the MillenniumDB server, you must acquire a session instance:

.. code-block:: console

   session = driver.session()

Then you can send queries through your session

.. code-block:: console

   query = 'MATCH (?from)-[:?type]->(?to) RETURN * LIMIT 10'
   result = session.run(query)

"""

for filename in os.listdir(src_path):
    if filename.endswith(".py") and filename != "__init__.py":
        module_name = filename[:-3]
        index_content += f"""
{module_name.capitalize()} Module
===============================
.. automodule:: millenniumdb_driver_python.{module_name}
   :members:
   :undoc-members:
   :show-inheritance:
"""

with open("index.rst", "w") as f:
    f.write(index_content)
