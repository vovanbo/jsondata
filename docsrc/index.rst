
.. jsondata documentation master file, created by
   sphinx-quickstart on `date`.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

'jsondata' - Modular processing of JSON data by trees and branches, pointers and patches 
========================================================================================

The 'jsondata' package provides the management of modular data structures based on JSON. 
The data is represented by in-memory tree structures with dynamically added
and/or removed branches. The data could be validated by JSON schemas, and stored 
for the later reuse.

The 'jsondata' package provides a standards conform layer for the processing
with emphasis on in-memory performance and low resource consume.
The implementation integrates seamless into the standard interfaces of Python(>=2.7),
whereas higher level features of additional standards and extensions are introduced
on top. The main interface classes are:

* **JSONData** - Core for RFC7159/RFC4627 based data structures

* **JSONDataSerializer** - Persistency for **JSONData**

* **JSONPointer** - RFC6901 for addressing nodes and values

* **JSONPatch** - RFC6902 for modification of branches and values 

In addition the following main utility classes are provided:
 
* **JSONCompute** - Support of JSON DSL for basic computing operations.

* **JSONTree** - Utilities for structure analysis and operations on JSON data structures, e.g. diff.


The syntax primitives of underlying layers are provided 
by the imported packages 'json' and 'jsonschema' in conformance to related ECMA and RFC 
standards and proposals. Here ECMA-262, ECMA-404, RFC7159/RFC4627, 
draft-zyp-json-schema-04, and others.

Therefore the designed architecture is based on the interfaces of the packages 'json' and
'jsonschema', and compatible packages::


                   +-------------------------+
    Applications   |    application-layer    |
                   +-------------------------+  
    .   .  .  .  .  . | .  .  . | .  .  .  | .  .  .  .  .  .  .  .  .
                   + - - - - - - - - - - - - +
    Process JSON   |       JSON-DSL          |
                   + - - - - - - - - - - - - +
    .   .  .  .  .  . | .  .  . | .  .  .  | .  .  .  .  .  .  .  .  .
                      |         V          |     
    Data              |   +----------+     |         RFC6901
    Structures        |   | jsondata |     |         RFC6902
                      |   +----------+     |         +extensions
    .  .  .  .  .  .  | .  . | .  | .  .  .| .  .  .  .  .  .  .  .  .
                      +---+--+    +---+----+           
                          |           |                           
                          V           V                            
                   +------------+------------+       RFC7159/RFC4267
    JSON           |    json    | jsonschema |       ECMA-262/ECMA-404    
    Syntax         |    ujson   |            |       draft-zyp-json-schema-04   
                   +------------+------------+ 
                                                     Support/verified: json, ujson
                                                        simply import package 
                                                        before 'jsondata'


The examples from the standards with some extensions, are included in order to 
verify implementation details for the recommendations.
This serves also as a first introduction to JSON processing with the
package 'jsondata'.
The current version is verified at the JSON-Syntax layer for the packages 
'json' and 'ujson'.

Current state of main features:

* RFC7159/RFC4627: Wrapper for 'json' and 'jsonschema' with file management, Alpha.

* RFC6901: JSONPointer - JSON notation, Alpha.

* RFC6901: JSONPointer - HTTP-Fragments notation(RFC3986), Alpha.

* RFC6902: JSONPatch - dynamic JSON data modification, Alpha.

* Extensions for RFC6901: Extended pointer expressions - JSON notation, Alpha.

* Extensions for RFC6902: Extended branch management, Alpha.

* Interactive JSON data design, current min-cli only, Alpha.

This document provides the developer information for the API, and the 
documentation of the PyUnit tests as examples and application patterns.

* JSON-DSL - A minimalistic language for processing JSON data.
  The computing could be either performed on the defined input syntax,
  or by providing the meta-syntax.
  The meta-syntax input could be provided as a python 'list' by programming API,
  as a list of arguments at the command line interface of 'jsonproc'. 

  * `JSON Compute Language <jsondata_compute_syntax.html>`_ : Language definition.

  * `Examples <jsondata_compute_syntax_examples.html>`_ : Language examples.

* Commandline tools.
 
  * `jsondatacheck <jsondatacheck.html>`_ : validates and presents JSON data

  * `jsonproc <jsonproc.html>`_ : provides command line interface for JSON processing

  * jsondatadiff: displays the differences, similar to 'diff'

  * jsondatapatch: applies patches, similar to 'patch'

  For help on the command line tools call e.g.:: 

    jsondatacheck --help

  For quick verification of the setup and basic features call:: 

    jsondatacheck --selftest



.. toctree::
   :maxdepth: 3

   jsondata
   UseCases
   tests

* setup.py

  For help on extensions to standard options call onlinehelp:: 

    python setup.py --help-jsondata



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`


Resources
=========

For available downloads refer to:

* Python Package Index: https://pypi.python.org/pypi/jsondata

* Sourceforge.net: https://sourceforge.net/projects/jsondata/

* github.com: https://github.com/ArnoCan/jsondata/

For Licenses refer to enclosed documents:

* Artistic-License-2.0(base license): `ArtisticLicense20.html <_static/ArtisticLicense20.html>`_

* Forced-Fairplay-Constraints(amendments): `licenses-amendments.txt <_static/licenses-amendments.txt>`_ / `Protect OpenSource Authors <http://xkcd.com/1303/>`_

