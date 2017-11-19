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

Installation
------------
``merkleshare`` is available through PyPI:

.. code-block:: bash

   $ pip install merkleshare

But if you want, you can install it directly from the repo:

.. code-block:: bash

   $ pip install git+https://github.com/drozdziak1/merkleshare

Requirements
------------
In order for MerkleShare to work, you need to bring up a local IPFS node using
``ipfs daemon``.

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

Got security needs? You'll be happy to know that MerkleShare supports Fernet
encryption (via the ``cryptography`` module):

.. code-block:: bash

   $ echo "Lizard people live at the edge of flat earth" | mersh -e
   /ipfs/QmcXM8gCqeJA2qjnVmFYkFFc2sMjDvT21p8UwGBwzWxva8/#fT7jn4eDJLgHcM3wva4KS4eUMyJ19zuxRJhy5Lp5xwZsVzA4Q6AzoEEEZxUt
                                                        # `----------------------------------------------------------'
                                                        #        Your data is guarded by a disposable secret

It's not possible to reach your data without the secret, which is only present
in the link...

.. code-block:: bash

   $ ipfs cat /ipfs/QmcXM8gCqeJA2qjnVmFYkFFc2sMjDvT21p8UwGBwzWxva8
   gAAAAABaAMt-gZCub5HYjOXvGbNZP7GaBDJL1ViYFSX9LiWAZAVLK6_o5I2lO3Bq86yHEvmuq-iI179Ficnzwvxug--9_xKFwfXzmv6NUm9tIFf64ukMETuwhWKJJJh9ytmsPJZaRPyA

...but if you do have it then retrieving your stuff with MerkleShare becomes
about as easy as it gets:

.. code-block:: bash

   $ mersh -d /ipfs/QmcXM8gCqeJA2qjnVmFYkFFc2sMjDvT21p8UwGBwzWxva8/#fT7jn4eDJLgHcM3wva4KS4eUMyJ19zuxRJhy5Lp5xwZsVzA4Q6AzoEEEZxUt
   Lizard people live at the edge of flat Earth

Features
--------
* Read from ``stdin`` or a specified file
* Only the link gets printed to ``stdout``, everything else is ``stderr`` -
  effortlessly pipe it to your favourite clipboard manager!
* Seamless data encryption
* Output the link in the format you need:

  * Regular: ``/ipfs/<hash>``
  * Gateway: ``https://ipfs.io/ipfs/<hash>`` - great for sharing links with non-IPFS friends
  * Local: ``http://localhost:8080/ipfs/<hash>``
  * Bare: ``<hash>``
* Optional static WebUI (Enabled with the ``-g`` flag)

Planned Features
----------------
* Built-in clipboard support
* Pure Python IPFS backend (once ``py-ipfs`` is ready)
* Binary blob support for WebUI uploads
