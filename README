jsondata
========

This package is aimed for the management of modular data structures based on JSON.
The data is represented by an in-memory main data tree with
dynamically added and/or removed branches and values. The logical branches of data 
structures in particular provide for the ease of custom data sets. 

The 'jsondata' package provides a standards conform layer for the processing of JSON
based data with emphasis on in-memory performance and low resource consume.
The implementation integrates seamless into the standard interfaces of Python(>=2.7),
whereas higher level features of additional standards are introduced on top.

The main interface classes are:

* **JSONDataSerializer** - Core for RFC7159 based data structures and persistency

* **JSONPointer** - RFC6901 for addressing

* **JSONPatch** - RFC6902 for modification

The syntax primitives of underlying layers are provided 
by the imported packages 'json' and 'jsonschema' in conformance to related ECMA and RFC 
standards and proposals. Here ECMA-262, ECMA-404, RFC7159/RFC4627, 
draft-zyp-json-schema-04, and others.

The architecture is based on the packages 'json' and
'jsonschema'::

                   +-------------------------+
    Applications   |    application-layer    |
                   +-------------------------+  
    .   .  .  .  .  . | .  .  . | .  .  .  | .  .  .  .  .  .  .  .  .
                      |         V          |     
                      |   +----------+     |      
    Data              |   | jsondata |     |         RFC6901
    Structures        |   +----------+     |         RFC6902      
    .  .  .  .  .  .  | .  . | .  | .  .  .| .  .  .  .  .  .  .  .  .
                      +---+--+    +---+----+           
                          |           |                           
                          V           V                            
                   +------------+------------+       RFC7159/RFC4267
    JSON           |    json    | jsonschema |       ECMA-262/ECMA-404    
    Syntax         +------------+------------+       draft-zyp-json-schema-04   

The examples from the standards with some extensions, are included in order to 
verify implementation details for the recommendations.
This serves also as a first introduction to JSON processing with the
package 'jsondata'.


**Downloads**:

* Sourceforge.net: https://sourceforge.net/projects/jsondata/files/

* Github: https://github.com/ArnoCan/jsondata/

**Online documentation**:

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

* VERSION: 00.01.003

* RELEASE: 00.01.003

* STATUS: alpha

* AUTHOR: Arno-Can Uestuensoez

* COPYRIGHT: Copyright (C) 2010,2011,2015-2016 Arno-Can Uestuensoez @Ingenieurbuero Arno-Can Uestuensoez

* LICENSE: Artistic-License-2.0 + Forced-Fairplay-Constraints
  Refer to enclose documents:
  
  *  ArtisticLicense20.html - for base license: Artistic-License-2.0 

  *  licenses-amendments.txt - for amendments: Forced-Fairplay-Constraints

VERSIONS and RELEASES
---------------------

**RELEASE: 00.00.00x - Pre-Alpha:**

Extraction of the features from hard-coded application into a reusable package.

**RELEASE: 00.01.002 - Alpha:**

Although stable to be used partially in production from now on, released as 'Alpha'.
Includes support of RFC7591 by the package 'json', JSONSchema drafts4 by 'jsonschema',
RFC6901 JSONPointer native, internal calls for RFC6902 JSONPatch.

**RELEASE: 00.01.003 - Alpha:**

Major Changes:

* General fixes and enhancements 

* First step of performance enhancements

* JSONPatch - RFC6902: introduced first release for now, STATE: Alpha

* added a considerable amount of Unit tests, now in total 498

