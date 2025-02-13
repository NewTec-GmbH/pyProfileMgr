.. pyProfileMgr documentation master file.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.
   This file is written in ``reStructuredText`` syntax. Dor documentation see:
   `reStructuredText <https://www.sphinx-doc.org/en/master/usage/restructuredtext/index.html>`_

   ATTENTION!! If you want to edit "User Editable" sections, change `update_doc_from_src.py`
   otherwise they will be overwritten by intputs from the project during sphinx generation
 
.. <User editable section introduction>
.. role:: raw-html-m2r(raw)
   :format: html


pyProfileMgr :raw-html-m2r:`<!-- omit in toc -->`
=====================================================

Overview
--------


.. image:: https://www.plantuml.com/plantuml/proxy?cache=no&src=https://raw.githubusercontent.com/NewTec-GmbH/pyProfileMgr/main/doc/uml/overview.puml
   :target: https://www.plantuml.com/plantuml/proxy?cache=no&src=https://raw.githubusercontent.com/NewTec-GmbH/pyProfileMgr/main/doc/uml/overview.puml
   :alt: overview


More information on the deployment and architecture can be found in the `doc <./doc/README.md>`_ folder.

Usage
-----

.. code-block:: cmd

   pyProfileMgr [-h] [--version] [-v] {command} ...

.. </User editable section introduction>

.. <User editable section architecture>

Software Architecture
---------------------
.. toctree::
   :maxdepth: 2

   _sw-architecture/README.md
.. </User editable section architecture>

.. <User editable section source>

Software Detailed Design
------------------------
.. autosummary::
   :toctree: _autosummary
   :template: custom-module-template.rst
   :recursive:

   cmd_profile
   file_helper
   profile_mgr
   ret
   __main__
.. </User editable section source> 

Testing
-------
.. <User editable section unittest>

Software Detailed Design
------------------------
.. autosummary::
   :toctree: _autosummary
   :template: custom-module-template.rst
   :recursive:

   test_empty

.. </User editable section unittest> 

PyLint
^^^^^^
.. toctree::
   :maxdepth: 2
   
   pylint.rst

Indices and tables
------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

License information
-------------------
.. toctree::
   :maxdepth: 2

   license_include
