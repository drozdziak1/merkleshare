===============================
MerkleShare
===============================

.. image:: https://img.shields.io/travis/drozdziak1/merkleshare.svg
        :target: https://travis-ci.org/drozdziak1/merkleshare

.. image:: https://img.shields.io/pypi/v/merkleshare.svg
        :target: https://pypi.python.org/pypi/merkleshare


A no-brainer pastebin on IPFS - think distributed sprunge.us

* Documentation: (COMING SOON!) https://merkleshare.readthedocs.org.

Why this if there's ``ipfs add``?
---------------------------------
Good question! ``ipfs add`` currently doesn't support showing a full link, let alone
``xclip``-compatible output - the user has to select the hash, paste it in a browser
and manually add the rest of their preferred IPFS link format.

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
