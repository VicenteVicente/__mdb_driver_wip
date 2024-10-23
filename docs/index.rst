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


Catalog Module
===============================
.. automodule:: millenniumdb_driver_python.catalog
   :members:
   :undoc-members:
   :show-inheritance:

Chunk_decoder Module
===============================
.. automodule:: millenniumdb_driver_python.chunk_decoder
   :members:
   :undoc-members:
   :show-inheritance:

Driver Module
===============================
.. automodule:: millenniumdb_driver_python.driver
   :members:
   :undoc-members:
   :show-inheritance:

Graph_objects Module
===============================
.. automodule:: millenniumdb_driver_python.graph_objects
   :members:
   :undoc-members:
   :show-inheritance:

Iobuffer Module
===============================
.. automodule:: millenniumdb_driver_python.iobuffer
   :members:
   :undoc-members:
   :show-inheritance:

Message_decoder Module
===============================
.. automodule:: millenniumdb_driver_python.message_decoder
   :members:
   :undoc-members:
   :show-inheritance:

Message_receiver Module
===============================
.. automodule:: millenniumdb_driver_python.message_receiver
   :members:
   :undoc-members:
   :show-inheritance:

Millenniumdb_error Module
===============================
.. automodule:: millenniumdb_driver_python.millenniumdb_error
   :members:
   :undoc-members:
   :show-inheritance:

Protocol Module
===============================
.. automodule:: millenniumdb_driver_python.protocol
   :members:
   :undoc-members:
   :show-inheritance:

Record Module
===============================
.. automodule:: millenniumdb_driver_python.record
   :members:
   :undoc-members:
   :show-inheritance:

Request_builder Module
===============================
.. automodule:: millenniumdb_driver_python.request_builder
   :members:
   :undoc-members:
   :show-inheritance:

Response_handler Module
===============================
.. automodule:: millenniumdb_driver_python.response_handler
   :members:
   :undoc-members:
   :show-inheritance:

Result Module
===============================
.. automodule:: millenniumdb_driver_python.result
   :members:
   :undoc-members:
   :show-inheritance:

Session Module
===============================
.. automodule:: millenniumdb_driver_python.session
   :members:
   :undoc-members:
   :show-inheritance:

Socket_connection Module
===============================
.. automodule:: millenniumdb_driver_python.socket_connection
   :members:
   :undoc-members:
   :show-inheritance:
