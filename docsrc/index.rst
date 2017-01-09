Abstract
########

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
##################

This version supports Linux and Windows7 - The update for MacOS, BSD, and Solaris is going to follow soon.

Blueprint
#########

The architecture is based on the interfaces of the packages 'json' and
'jsonschema', and compatible packages such as `'ujson' [online] <https://pypi.python.org/pypi/ujson>`_
::


                   +-------------------------+
    Applications   |    application-layer    |
                   +-------------------------+  
    .   .  .  .  .  . | .  .  . | .  .  .  | .  .  .  .  .  .  .  .  .
                   + - - - - - - - - - - - - +    see e.g. jsoncompute, 
    Process JSON   |    processing tools     |    jsoncliopts,  
                   + - - - - - - - - - - - - +    jsondataunit
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


The provided features comprise:

* `JSON Data <jsondata_branch_operations.html>`_ : Manage branches of substructures - jsondata.JSONData 
  `[API] <jsondata_m_data.html#>`_
  `[source] <_modules/jsondata/JSONData.html#JSONData>`_

* `JSON Serializer <jsondata_branch_serializer.html>`_ : Serialize JSON documents - jsondata.JSONDataSerializer 
  `[API] <jsondata_m_serializer.html#>`_
  `[source] <_modules/jsondata/JSONDataSerializer.html#JSONDataSerializer>`_


* `JSON Pointer <jsondata_pointer_operations.html>`_ : Access pointer paths and values - jsondata.JSONPointer 
  `[API] <jsondata_m_pointer.html#>`_
  `[source] <_modules/jsondata/JSONPointer.html#JSONPointer>`_

* `JSON Patch <jsondata_patch_operations.html>`_ : Modify data structures and values - jsondata.JSONPatch 
  `[API] <jsondata_m_patch.html#>`_
  `[source] <_modules/jsondata/JSONPatch.html#JSONPatch>`_

Including the utilities:
 
* JSON Tree: Utilities for structure analysis and operations on JSON data structures, e.g. diff 
  `[API] <jsondata_m_tree.html>`_
  `[source] <_modules/jsondata/JSONTree.html#JSONTree>`_

The syntax primitives of underlying layers are processed by the imported standard packages 'json' and 'jsonschema' 
in conformance to related standards.
Current supported compatible packages include:  `'ujson' [online] <https://pypi.python.org/pypi/ujson>`_.

The examples from the standards with some extensions are included as 
`Use-Cases <usecases.html#>`_ 
in order to 
verify implementation details for the recommendations
`[see] <usecases.html#>`_ 
.
This serves also as a first introduction to JSON processing with the
package 'jsondata'.

For the implementation and architecture refer to

* `Software design <software_design.html>`_ 

Install - HowTo - FAQ - Help
############################

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
#########

Concepts and workflows:

* Selected Common UsesCases `[examples] <usecases.html>`_

Common Interfaces:

* Commandline Interface `[call-interface] <shortcuts.html#jsondata-cli>`_

* Programming Interface `[API-Selection] <shortcuts.html#>`_

* Test data `[testdata] <shortcuts.html#test-data>`_

Complete technical API:

* Interface in javadoc-style `[API] <epydoc/index.html>`_


Table of Contents
#################

.. toctree::
   :maxdepth: 3

   index_shortcuts
   index_jsondata
   index_testdata

   UseCases
   tests

* setup.py

  For help on extensions to standard options call onlinehelp:: 

    python setup.py --help-jsondata



Indices and tables
##################

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`


Resources
#########

For available downloads refer to:

* Python Package Index: https://pypi.python.org/pypi/jsondata

* Sourceforge.net: https://sourceforge.net/projects/jsondata/

* github.com: https://github.com/ArnoCan/jsondata/

For JSON processing references:

* JSONDataUnit: https://pypi.python.org/pypi/jsondataunit

* JSONCompute: https://pypi.python.org/pypi/jsoncompute

* JSONCLIOpts: https://pypi.python.org/pypi/jsoncliopts

* ujson: https://pypi.python.org/pypi/ujson

* json: https://docs.python.org/2/library/json.html


For Licenses refer to enclosed documents:

* Artistic-License-2.0(base license): `ArtisticLicense20.html <_static/ArtisticLicense20.html>`_

* Forced-Fairplay-Constraints(amendments): `licenses-amendments.txt <_static/licenses-amendments.txt>`_ / `Protect OpenSource Authors <http://xkcd.com/1303/>`_

