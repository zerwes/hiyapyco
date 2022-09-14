.. image:: https://badgen.net/badge/stand%20with/UKRAINE/?color=0057B8&labelColor=FFD700

.. image:: https://github.com/zerwes/hiyapyco/actions/workflows/pylint.yml/badge.svg?branch=master
    :target: https://github.com/zerwes/hiyapyco/actions/workflows/pylint.yml

.. image:: https://github.com/zerwes/hiyapyco/actions/workflows/test.yml/badge.svg
     :target: https://github.com/zerwes/hiyapyco/actions/workflows/test.yml

hiyapyco
========

HiYaPyCo - A Hierarchical Yaml Python Config

Description
-----------

A simple python lib allowing hierarchical overlay of config files in
YAML syntax, offering different merge methods and variable interpolation
based on jinja2.

The goal was to have something similar to puppets hiera
``merge_behavior: deeper`` for python.

Key Features
------------

-  hierarchical overlay of multiple YAML files
-  multiple merge methods for hierarchical YAML files
-  variable interpolation using jinja2

Requirements
------------

-  PyYAML aka. python3-yaml
-  Jinja2 aka. python3-jinja2

Python Version
~~~~~~~~~~~~~~

HiYaPyCo was designed to run on current major python versions
without changes. Tested versions:

-  3.9

Usage
-----

A simple example:

::

    import hiyapyco
    conf = hiyapyco.load('yamlfile1' [,'yamlfile2' [,'yamlfile3' [...]]] [,kwargs])
    print(hiyapyco.dump(conf, default_flow_style=False))

real life example:
~~~~~~~~~~~~~~~~~~

``yaml1.yaml``:

::

    ---
    first: first element
    second: xxx
    deep:
        k1:
            - 1
            - 2

``yaml2.yaml``:

::

    ---
    second: again {{ first }}
    deep:
        k1:
            - 4 
            - 6
        k2:
            - 3
            - 6

load ...

::

    >>> import pprint
    >>> import hiyapyco
    >>> conf = hiyapyco.load('yaml1.yaml', 'yaml2.yaml', method=hiyapyco.METHOD_MERGE, interpolate=True, failonmissingfiles=True)
    >>> pprint.PrettyPrinter(indent=4).pprint(conf)
    {   'deep': {   'k1': [1, 2, 4, 6], 'k2': [3, 6]},
        'first': u'first element',
        'ma': {   'ones': u'12', 'sum': u'22'},
        'second': u'again first element'}

real life example using yaml documents as strings
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

    >>> import hiyapyco
    >>> y1="""
    ... yaml: 1
    ... y:
    ...   y1: abc
    ...   y2: xyz
    ... """
    >>> y2="""
    ... yaml: 2
    ... y:
    ...   y2: def
    ...   y3: XYZ
    ... """
    >>> conf = hiyapyco.load([y1, y2], method=hiyapyco.METHOD_MERGE)
    >>> print (conf)
    OrderedDict([('yaml', 2), ('y', OrderedDict([('y1', 'abc'), ('y2', 'def'), ('y3', 'XYZ')]))])
    >>> hiyapyco.dump(conf, default_flow_style=True)
    '{yaml: 2, y: {y1: abc, y2: def, y3: XYZ}}\n'

args
~~~~

All ``args`` are handled as *file names* or *yaml documents*. They may
be strings or list of strings.

kwargs
~~~~~~

-  ``method``: bit (one of the listed below):

   -  ``hiyapyco.METHOD_SIMPLE``: replace values (except for lists a
      simple merge is performed) (default method)
   -  ``hiyapyco.METHOD_MERGE``: perform a deep merge
   -  ``hiyapyco.METHOD_SUBSTITUTE``: perform a merge w/ lists substituted (unsupported)

- ``mergelists``: boolean try to merge lists of dict (default: ``True``)

-  ``interpolate``: boolean : perform interpolation after the merge
   (default: ``False``)

-  ``castinterpolated``: boolean : try to perform a *best possible
   match* cast for interpolated strings (default: ``False``)

-  ``usedefaultyamlloader``: boolean : force the usage of the default
   *PyYAML* loader/dumper instead of *HiYaPyCo*\ s implementation of a
   OrderedDict loader/dumper (see: Ordered Dict Yaml Loader / Dumper
   aka. ODYLDo) (default: ``False``)

- ``encoding``: string : encoding used to read yaml files (default: ``utf-8``)

-  ``failonmissingfiles``: boolean : fail if a supplied YAML file can
   not be found (default: ``True``)

-  ``loglevel``: int : loglevel for the hiyapyco logger; should be one
   of the valid levels from ``logging``: 'WARN', 'ERROR', 'DEBUG', 'I
   NFO', 'WARNING', 'CRITICAL', 'NOTSET' (default: default of
   ``logging``)

-  ``loglevelmissingfiles``: int : one of the valid levels from
   ``logging``: 'WARN', 'ERROR', 'DEBUG', 'INFO', 'WARNING', 'CRITICAL',
   'NOTSET' (default: ``logging.ERROR`` if
   ``failonmissingfiles = True``, else ``logging.WARN``)

interpolation
~~~~~~~~~~~~~

For using interpolation, I strongly recomend *not* to use the default
PyYAML loader, as it sorts the dict entrys alphabetically, a fact that
may break interpolation in some cases (see ``test/odict.yaml`` and
``test/test_odict.py`` for an example). See Ordered Dict Yaml Loader /
Dumper aka. ODYLDo

default
^^^^^^^

The default jinja2.Environment for the interpolation is

::

    hiyapyco.jinja2env = Environment(undefined=Undefined)

This means that undefined vars will be ignored and replaced with a empty
string.

change the jinja2 Environment
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If you like to change the jinja2 Environment used for the interpolation,
set ``hiyapyco.jinja2env`` **before** calling ``hiyapyco.load``!

use jinja2 DebugUndefined
^^^^^^^^^^^^^^^^^^^^^^^^^

If you like to keep the undefined var as string but raise no error, use

::

    from jinja2 import Environment, Undefined, DebugUndefined, StrictUndefined
    hiyapyco.jinja2env = Environment(undefined=DebugUndefined)

use jinja2 StrictUndefined
^^^^^^^^^^^^^^^^^^^^^^^^^^

If you like to raise a error on undefined vars, use

::

    from jinja2 import Environment, Undefined, DebugUndefined, StrictUndefined
    hiyapyco.jinja2env = Environment(undefined=StrictUndefined)

This will raise a ``hiyapyco.HiYaPyCoImplementationException`` wrapped
arround the ``jinja2.UndefinedError`` pointing at the string causing the
error.

more informations
^^^^^^^^^^^^^^^^^

See:
`jinja2.Environment <http://jinja.pocoo.org/docs/dev/api/#jinja2.Environment>`_

cast interpolated strings
~~~~~~~~~~~~~~~~~~~~~~~~~

As you must use interpolation as strings (PyYAML will weep if you try to
start a value with ``{{``), you can set ``castinterpolated`` to *True*
in order to try to get a ``best match`` cast for the interpolated
values. **The ``best match`` cast is currently only a q&d implementation
and may not give you the expected results!**

Ordered Dict Yaml Loader / Dumper aka. ODYLDo
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This is a simple implementation of a PyYAML loader / dumper using
``OrderedDict`` from collections.
**Because chaos is fun but order matters on loading dicts from a yaml
file.**


Install
-------

From Source
~~~~~~~~~~~

GitHub
^^^^^^

`https://github.com/zerwes/hiyapyco <https://github.com/zerwes/hiyapyco>`_

::

    git clone https://github.com/zerwes/hiyapyco
    cd hiyapyco
    sudo python setup.py install

PyPi
^^^^

Download the latest or desired version of the source package from
`https://pypi.python.org/pypi/HiYaPyCo <https://pypi.python.org/pypi/HiYaPyCo>`_.
Unpack the archive and install by executing:

::

    sudo python setup.py install

pip
~~~

Install the latest wheel package using:

::

    pip install HiYaPyCo

debian packages
~~~~~~~~~~~~~~~

install the latest debian packages from http://repo.zero-sys.net/hiyapyco::

    echo "deb http://repo.zero-sys.net/hiyapyco/deb ./" > /etc/apt/sources.list.d/hiyapyco.list
    gpg --keyserver keys.gnupg.net --recv-key 77DE7FB4
    # or use:
    wget https://repo.zero-sys.net/77DE7FB4.asc -O - | gpg --import -
    gpg --armor --export 77DE7FB4 | apt-key add -
    apt-get update
    apt-get install python3-hiyapyco

rpm packages
~~~~~~~~~~~~

use
`http://repo.zero-sys.net/hiyapyco/rpm <http://repo.zero-sys.net/hiyapyco/rpm>`_
as URL for the yum repo and
`https://repo.zero-sys.net/77DE7FB4.asc <https://repo.zero-sys.net/77DE7FB4.asc>`_
as the URL for the key.

Arch Linux
~~~~~~~~~~

An `AUR package <https://aur.archlinux.org/packages/python-hiyapyco/>`_
is available (provided by `Pete Crighton <https://github.com/PeteCrighton>`_ and not always up to date).

License
-------

Copyright |copy| 2014 - 2022 Klaus Zerwes `zero-sys.net <https://zero-sys.net>`_

.. |copy| unicode:: 0xA9 .. copyright sign

This package is free software.
This software is licensed under the terms of the GNU GENERAL PUBLIC
LICENSE version 3 or later, as published by the Free Software
Foundation.
See
`https://www.gnu.org/licenses/gpl.html <https://www.gnu.org/licenses/gpl.html>`_

Changelog
---------

0.5.1
~~~~~~

MERGED: #52 by ryanfaircloth

0.5.0
~~~~~~

MERGED: #41 Jinja2 dependency increased to include Jinja2 3.x.x

REMOVED: Support for Python 2

0.4.16
~~~~~~

MERGED: #37 alex-ber

0.4.15
~~~~~~

MERGED: #30 lesiak:issue-30-utf

MERGED: #28 lesiak:issue-28

0.4.14
~~~~~~

FIXED: issue #33

MERGED: issue #32

0.4.13
~~~~~~

IMPLEMENTED: [issue #27] support multiple yaml documents in one file

0.4.12
~~~~~~

FIXED: logging by Regev Golan

0.4.11
~~~~~~

IMPLEMENTED: mergelists (see issue #25)

0.4.10
~~~~~~

FIXED: issue #24 repo signing

0.4.9
~~~~~

FIXED: issue #23 loglevelonmissingfiles

0.4.8
~~~~~

Fixed pypi doc

0.4.7
~~~~~

Reverted: logger settings to initial state

Improved: dump

Merged:

- flatten mapping from Chris Petersen geek@ex-nerd.com
- arch linux package info from Peter Crighton git@petercrighton.de

0.4.6
~~~~~

MERGED: fixes from mmariani

0.4.5
~~~~~

FIXED: issues #9 and #11

0.4.4
~~~~~

deb packages:

- removed support for python 2.6
- include examples as doc

0.4.3
~~~~~

FIXED: issue #6 *import of hiyapyco **version** in setup.py causes pip
install failures*

0.4.2
~~~~~

Changed: moved to GPL

Improvements: missing files handling, doc

0.4.1
~~~~~

Implemented: ``castinterpolated``

0.4.0
~~~~~

Implemented: loading yaml docs from string

0.3.2
~~~~~

Improved tests and bool args checks

0.3.0 / 0.3.1
~~~~~~~~~~~~~

Implemented a Ordered Dict Yaml Loader

0.2.0
~~~~~

Fixed unicode handling

0.1.0 / 0.1.1
~~~~~~~~~~~~~

Initial release
