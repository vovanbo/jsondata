"""Modular processing of JSON data by trees and branches, pointers and patches.

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

The integration of 'jsondata' into the JSON processing flow could be extended
by custom classes as required::

              +--------------------------------+
              |       application-layer        |    <= Application layer, e.g including 
              +-----------------+              |       REST-Middleware
              | JSONCompute     |              |    <= DSL for JSON see package 'jsoncompute'
              +--------------+--+--------------+       https://pypi.python.org/pypi/jsoncompute
                     |       |         |
            .  .  .  |  .  . | .  .  . | .  .  .  . <= combined API  
                     |       V         |
                     | +-----------+   | 
    RFC6902          | | JSONPatch |   |            <= modify JSON data 
                     | +-----------+   | 
                     |     |     |     |
                     V     V     |     |
                +-------------+  |     | 
    RFC6901     | JSONPointer |  |     |            <= address JSON data
                +-------------+  |     |
                       |         |     | 
                       V         V     V
    RFC7159         +---------------------+
       +            |      JSONData       |         <= integrate JSON+JSONschema
    DRAFT4          +----------o----------+
                               |
                    +---------------------+
                    | JSONDataSerializer  |         <= provide persistency for
                    +---------------------+            JSONData

                *         *          *        *
            .  .| .  .  . | .  .  .  | .  .  .| .  .<= common access to JSON data
                V         V          V        V
             +----------------+-----------------+ 
    RFC7159  |     json       |   jsonschema    |  <= provide JSON data and JSONschema
       &&    |     ujson      |                 |      
    DRAFT4   +----------------+-----------------+


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
"""
__author__ = 'Arno-Can Uestuensoez'
__license__ = "Artistic-License-2.0 + Forced-Fairplay-Constraints"
__copyright__ = "Copyright (C) 2015-2016 Arno-Can Uestuensoez @Ingenieurbuero Arno-Can Uestuensoez"
__version__ = '0.2.1'
__uuid__='63b597d6-4ada-4880-9f99-f5e0961351fb'

__package__ = 'jsondata'
__all__=[
    "JSONData",
    "JSONDataSerializer",
    "JSONDataException",
    "JSONDataKeyError",
    "JSONDataNodeType",
    "JSONDataSourceFile",
    "JSONDataTargetFile",
    "JSONDataValue",
    "JSONDataAmbiguity",
    "JSONPointer",
    "JSONPointerException",
    "JSONPatch",
    "JSONPatchException",
    "JSONTree"
]

