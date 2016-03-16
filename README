jsondata
========

This package is aimed for the management of modular data structures based on JSON.
The data is foreseen to be represented by an in-memory main data tree with
dynamically added and/or removed branches. The branches of data structures in
particular provide for the ease of custom data sets. 

The main class JSONDataSerializer provides for the serialization and incremental
load. Due to the complex scenarios of search and match for modular JSON data in trees
and branches a number of distinctive exceptions are defined in addition.

Current version supports for first features of JSONPointer and JSONPatch. 
The following versions are going to support the full scope in accordance 
RFC6901, and RFC6902. For syntax primitives of underlying layers the packages
'json' and 'jsonschema' are applied for conformance to related ECMA and RFC 
standards and proposals. Here ECMA-262, ECMA-404, RFC7159/RFC4627, 
draft-zyp-json-schema-04, and others.

The documents provides the developer information for the API, and the 
PyUnit tests as examples and application patterns.

Available from:

* Sourceforge.net: https://sourceforge.net/projects/jsondata/files/

* Github: https://github.com/ArnoCan/jsondata/

Documents
---------

Online documentation:

* https://pypi.python.org/pypi/jsondata/
* https://pythonhosted.org/jsondata/

setup.py
--------

The installer adds a few options to the standard setuptools options.

* *build_sphinx*: Creates documentation for runtime system by Sphinx, html only. Calls 'callDocSphinx.sh'.

* *build_epydoc*: Creates documentation for runtime system by Epydoc, html only. Calls 'callDocEpydoc.sh'.

* *test*: Runs PyUnit tests by discovery.

* *--help-jsondata*: Displays this help.

* *--no-install-required*: Suppresses installation dependency checks, requires appropriate PYTHONPATH.

* *--offline*: Sets online dependencies to offline, or ignores online dependencies.

* *--exit*: Exit 'setup.py'.


Project Data
------------

* PROJECT: 'jsondata'

* MISSION: Provide and extend JSONPointer and JSONPatch - RFC6901, RFC6902

* VERSION: 00.01.002

* RELEASE: 00.01.002

* STATUS: alpha

* AUTHOR: Arno-Can Uestuensoez

* COPYRIGHT: Copyright (C) 2010,2011,2015-2016 Arno-Can Uestuensoez @Ingenieurbuero Arno-Can Uestuensoez

* LICENSE: Artistic-License-2.0 + Forced-Fairplay-Constraints
  Refer to enclose documents:
  
  *  ArtisticLicense20.html - for base license: Artistic-License-2.0 

  *  licenses-amendments.txt - for amendments: Forced-Fairplay-Constraints

VERSIONS and RELEASES
---------------------

**RELEASE: 00.01.002 - Alpha:**

Although stable to be used partially in production from now on, released as 'Alpha'.
This is mainly due to the ongoing tests and the included fragment parts for the
RFC6902/JSONPatch - support.

The growing number of unit test base has to reach a slightly bigger number too.

Major Changes:

* JSON - RFC7159 / RFC4627: STATE: Alpha: 

  * Adapted JSONDataSerializer for RFC6901, RFC6902 refer to the methods named by the prefix pattern 'rfc6902'. 

  * Cleared interfaces, another almost final round still required.

* JSONPointer - RFC6901: added, STATE: Alpha

  * adapted JSONDataSerializer
  
  * added JSONPointer

  * adapted operators for pointer manipulation::
    +(LHS), +(RHS), ==, >=, >, +=, <, <=, !=

  * defined an extendible set of type mappings from altered
    'json' data trees onto standard JSON types 

  * Fragments notation of RFC6901/RFC3986 implemented.

* JSONPatch - RFC6902: fragments for now, STATE: Pre-Alpha

  *  adapted JSONDataSerializer
     refer to the methods named by the prefix pattern
     'rfc6902'.
  
  *  added JSONPatch

* added a considerable amount of Unit tests

* performance enhancements


