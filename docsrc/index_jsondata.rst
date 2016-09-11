
'jsondata' - package
####################

.. toctree::
   :maxdepth: 4

The package 'jsondata' is aimed for the management of modular in-memory data 
structures based on JSON. The data is foreseen to be represented by a main data
tree with dynamically added and/or removed branches. The branches of data 
structures in particular provide for custom data. The data could either be 
related to a module, and/or to specific classes. The components provides by 
the package are:

* **JSONData**:
  The main class JSONData provides for the core interface of the
  integration of JSON based documents and sub-documents including the 
  validation by JSONschema - RFC7159/RFC4629 and DRAFT4schema.

  This provides for dynamic incremental construction of data and 
  the persistent storage of the modified tree. The data is organized 
  into trees and branches managed by the packages 'json' ad 'jsonschema'. 

* **JSONDataSerializer**:
  The class JSONDataSerializer derived from JSONData provides for 
  serialization and integration of documents and sub-documents. This 
  provides for the persistent storage of modified document trees.

* **JSONPointer**:
  The JSONPointer module provides for addressing of components within
  JSON based data structures in accordance to RCF7159 and RFC6901. 
  The integrated caching of the in-memory address of the pointed node
  provides for native speed in case of repetition, aimed for nested
  hierarchical loop constructs.
   
  The class JSONPointer in particular provides operators for pointer 
  arithmetics in order to simplify the application of navigation 
  and loop constructs.
  
* **JSONPatch**:
  The JSONPatch module provides features for the alteration of JSON based
  data structures in accordance to RFC6902. The close design enables the
  fast addressing by combined usage with the class JSONPointer. 

  The class JSONPatch in particular provides operators for patch arithmetics
  in order to simplify the modular patch management and loop constructs.
  The patch task lists could be assembled by modules, modified as required 
  and stored persistently for reuse. 

* **JSONCompute**:
  Moved to a seperate package 'jsoncompute'. 

* **Selftest** / **'jsondatacheck --selftest'**:
  Last but not least, the selftest feature provides for a quick verification
  of the package itself.
 
The close design to the presented in-memory interface by the packages 'json'
and 'jsonschema' provides for reliable and fast access based on the standard 
Python packages, while the 'jsondata' package adds high-level abstractions
provided by standards for addressing and data assembly. The native Python 
access to the data entries remains compatible, while due to the collaborative
caching of in-memory addresses of the nodes the access by the 'jsondata' 
add-ons is close to native Python. 


The package 'jsondata' supports the standards RFC6901, RFC6902, and the
integration of RFC7159 with DRAFT4Schema, while relying for the syntax
primitives of underlying layers presented by the packages 'json' and
'jsonschema'. The JSON language primitives for JSON are conform with
related ECMA and RFC standards and proposals. Here ECMA-262, ECMA-404, 
RFC7159/RFC4627, 'draft-zyp-json-schema-04', and others.

JSON based data provides for low resource data structure descriptions, 
thus fits in general quite good to distributed interface APIs, beneath 
JavaScript itself to protocols like those based on REST. But it also is 
applicable in case of numerous other requirements, a typical application
for branch data and VV is the persistent storage of GUI models for 
dynamically loaded and released user elements.

.. automodule:: jsondata

**Sources**

* `jsondata.JSONData [source] <_modules/jsondata/JSONData.html#JSONData>`_

* `jsondata.JSONDataExceptions [source] <_modules/jsondata/JSONDataExceptions.html#>`_

* `jsondata.JSONDataSerializer [source] <_modules/jsondata/JSONDataSerializer.html#JSONDataSerializer>`_

* `jsondata.JSONPatch [source] <_modules/jsondata/JSONPatch.html#JSONPatch>`_

* `jsondata.JSONTree [source] <_modules/jsondata/JSONTree.html#JSONTree>`_

* `jsondata.JSONPointer [source] <_modules/jsondata/JSONPointer.html#JSONPointer>`_

* `jsondata.Selftest [source] <_modules/jsondata/Selftest.html#>`_


.. include:: jsondata_m_data.rst
.. include:: jsondata_m_serializer.rst
.. include:: jsondata_m_pointer.rst
.. include:: jsondata_m_patch.rst
.. include:: jsondata_m_tree.rst
.. include:: jsondata_m_exceptions.rst
.. include:: jsondata_m_selftest.rst

