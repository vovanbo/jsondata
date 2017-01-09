"""Modular processing of JSON data by trees and branches, pointers and patches.

The data represented as in-memory 'json' compatible structure, 
with dynamically added and/or removed branches. 
The components provides by  the package are:

* **JSONData**:
  The main class JSONData provides for the core interface.

* **JSONDataSerializer**:
  Derived from JSONData provides for serialization and integration
  of documents and sub-documents.

* **JSONPointer**:
  The JSONPointer module provides for addressing in accordance 
  to RCF7159 and RFC6901. 
  
* **JSONPatch**:
  The JSONPatch module provides features in accordance to RFC6902.

* **JSONCompute**:
  Moved to a seperate package 'http://pypi.python.org/pypi/jsoncompute/'. 

* **Selftest** / **'jsondc --selftest'**:
  Last but not least, the selftest feature provides for a quick verification
  of the package itself.
 
For additional information refer to the documentation
http://pythonhosted.org/jsondata/.
"""
__author__ = 'Arno-Can Uestuensoez'
__maintainer__ = 'Arno-Can Uestuensoez'
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

