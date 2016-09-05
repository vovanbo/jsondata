Abstract
========

The 'jsondata' package provides the management of modular data structures based on JSON. 
The data is represented by in-memory tree structures with dynamically added
and/or removed branches. The data could be validated by JSON schemas, and stored 
for the later reuse.

The 'jsondata' package provides a standards conform layer for the processing
with emphasis on in-memory performance and low resource consume.
The implementation integrates seamless into the standard interfaces of Python(>=2.7),
whereas higher level features of additional standards and extensions are introduced
on top. 

REMARK - Platforms
==================

This version supports Linux only - The update for Windows and MacOS is going to follow soon.

Blueprint
=========

The architecture is based on the interfaces of the packages 'json' and
'jsonschema', and compatible packages such as 'ujson'::


                   +-------------------------+
    Applications   |    application-layer    |
                   +-------------------------+  
    .   .  .  .  .  . | .  .  . | .  .  .  | .  .  .  .  .  .  .  .  .
                   + - - - - - - - - - - - - +
    Process JSON   |         JSON/DSL        |    https://pypi.python.org/pypi/jsoncompute
                   + - - - - - - - - - - - - +
    .   .  .  .  .  . | .  .  . | .  .  .  | .  .  .  .  .  .  .  .  .
                      |         V          |     
    Data              |   +----------+     |      RFC6901
    Structures        |   | jsondata |     |      RFC6902
                      |   +----------+     |      +pointer arithmetics
                      |      |    |        |      +extensions
    .  .  .  .  .  .  | .  . | .  | .  .  .| .  .  .  .  .  .  .  .  .
                      +---+--+    +---+----+           
                          |           |                           
                          V           V                            
                   +------------+------------+    RFC7159/RFC4267
    JSON           |    json    | jsonschema |    ECMA-262/ECMA-404    
    Syntax         |    ujson   |            |    draft-zyp-json-schema-04   
                   +------------+------------+ 
                                                  Support/verified: json, ujson
                                                  simply import package 
                                                  before 'jsondata'


The provided features for the automation of 
JSON based operations and calculations comprise the following list, 
for code examples refer to 'jsondata.UseCases.examples'.

* `JSON Pointer <jsondata_pointer_operations.html>`_ : Access pointer paths and values - *jsondata.JSONPointer*.

* `JSON Patch <jsondata_patch_operations.html>`_ : Modify data structures and values - *jsondata.JSONPatch*.

* `JSON Data <jsondata_branch_operations.html>`_ : Manage branches of substructures - *jsondata.JSONData*.

* `JSON Serializer <jsondata_branch_serializer.html>`_ : Serialize JSON documents - *jsondata.JSONDataSerializer*.

* JSON DSL: The JSON-DSL is moved into the package 'jsoncompute'.


In addition the following main utilities are provided:
 
* `JSON Tree <jsondata_m_tree.html>`_ : Utilities for structure analysis and operations on JSON data structures, e.g. diff.

The syntax primitives of underlying layers are processed by the imported standard packages 'json' and 'jsonschema' 
in conformance to related standards.
Current supported compatible packages include: 'ujson'.

The examples from the standards with some extensions are included as Use-Cases in order to 
verify implementation details for the recommendations.
This serves also as a first introduction to JSON processing with the
package 'jsondata'.

This document provides the developer information for the API, Use-Cases, and the 
documentation of the PyUnit tests as examples and application patterns.

Install - HowTo - FAQ - Help
============================

* **Install**:

  Standard procedure online local install by sources::

    python setup.py install --user

  Custom procedure offline by::

    python setup.py install --user --offline

  Documents, requires Sphinx and Epydoc::

    python setup.py build_doc install_doc

* **Introduction**:

  For now refer to the listed API and subdocument collection in section 
  :ref:`'Shortcuts' <shortcs>`


Shortcuts
=========

Concepts and workflows:

* Selected Common UsesCases `[examples] <usecases.html>`_

Common Interfaces:

* Commandline Interface `[call-interface] <shortcuts.html#jsondata-cli>`_

* Programming Interface `[API-Selection] <shortcuts.html#>`_

Complete technical API:

* Interface in javadoc-style `[API] <epydoc/index.html>`_


Table of Contents
=================

.. toctree::
   :maxdepth: 3

   shortcuts
   usecases

   jsondata
   UseCases
   tests
   testdata

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

