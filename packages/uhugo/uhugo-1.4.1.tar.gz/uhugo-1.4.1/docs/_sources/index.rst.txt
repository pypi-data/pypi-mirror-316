.. uHugo documentation master file, created by
   sphinx-quickstart on Thu Jul  1 10:43:20 2021.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to uHugo's documentation!
=================================

uHugo is a helper tool for `Hugo <https://gohugo.org>`_ that automates the instillation and updating of the application. 
It also updates static site cloud provider's configurations if exists.

Instillation
------------

Make sure you are on Python 3.6+. In your terminal, type in:

.. code-block:: sh

   > pip install uhugo

You can test it by 

.. code-block:: sh

   > uhugo --help

   Usage: uhugo [OPTIONS] COMMAND [ARGS]...

   uhugo is a Hugo binary helper that downloads and set ups the environment.

   Options:
   --debug    Use debug mode
   --version  Show the version and exit.
   --help     Show this message and exit.

   Commands:
   install  Install latest Hugo binary files
   update   Updates Hugo binary files and any associated configurations

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   commands
   providers/index
   reference/index


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
