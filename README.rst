===============================
MerkleShare
===============================

.. image:: https://img.shields.io/travis/drozdziak1/merkleshare.svg
        :target: https://travis-ci.org/drozdziak1/merkleshare

.. image:: https://img.shields.io/pypi/v/merkleshare.svg
        :target: https://pypi.python.org/pypi/merkleshare


A no-brainer pastebin on IPFS - think distributed http://sprunge.us

Why this if there's ``ipfs add``?
---------------------------------
Good question! ``ipfs add`` currently doesn't support showing a full link, let alone
``xclip``-compatible output - the user has to select the hash, paste it in a browser
and manually add the rest of their preferred IPFS link format.

Usage
-----

A typical stdin pipe situation:

.. code-block:: bash

   $ echo "Hello, world" | mersh -t gateway
   https://ipfs.io/ipfs/QmaMLRsvmDRCezZe2iebcKWtEzKNjBaQfwcu7mcpdm8eY2

How about some file input?

.. code-block:: bash

   $ echo "Hello, friends." > file.txt
   $ mersh file.txt
   /ipfs/QmZRyLRgWiXN2Zks6rjH5jPYQzbWj3BYTWERa9m7QQc3kW

Or maybe you only need the hash? No problem:

.. code-block:: bash

   $ echo "Rollin' with the hash\!" | mersh -t hash
   QmWjZ4dF4brEPqjtWx2EqZbeAmcpHiCVkhAxJyi51TPJzh

Features
--------
* Read from ``stdin`` or a specified file
* Only the link gets printed to ``stdout``, everything else is ``stderr`` - effortlessly pipe it to your favourite clipboard manager!
* Output the link in the format you need:

  * Regular: ``/ipfs/<hash>``
  * Gateway: ``https://ipfs.io/ipfs/<hash>`` - great for sharing links with non-IPFS friends
  * Local: ``http://localhost:8080/ipfs/<hash>``
  * Bare: ``<hash>``

Planned Features
----------------
* (optional) static WebUI
* Clipboard support
