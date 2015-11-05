.. Copyright (c) Moshe Zadka
   See LICENSE for details.

rfc7464
-------

.. image:: https://travis-ci.org/moshez/rfc7464.svg?branch=master
    :target: https://travis-ci.org/moshez/rfc7464

The firehose of your JSON

Introduction
============

RFC 7464 is a proposed standard for streaming JSON documents.
It is meant to be used for things like loggers,
which can use JSON to log structured data.
It is designed to recover gracefully from file truncation,
even in the middle -- such as what happens when a previous
run crashed badly, and the next run opens the existing
log file for appending.

Contributing
============

We welcome issues and PRs on GitHub!
Please adhere to the contributor covenant,
conveniently placed in the root of the repository.

.. code::

  $ tox

Should succeed on pull requests when rebased
against latest master for PRs before they
can be merged, but not before they can be submitted.
For your first PR, please add yourself to the list
of authors in the LICENSE file.

For issues, if the problem is non-compliance with the RFC,
please site the specific section, quote from the RFC,
and (ideally) give a concrete example.

Documentation
=============

Documentation is available on ReadTheDocs


.. _ReadTheDocs:
