jsondata
========

This package is aimed for the management of modular data structures based on JSON.
Therefore it is based on and supports JSON patch and JSON pointer standards, in 
addition extended features are provided.
The data is represented by an in-memory main data tree with
dynamically added and/or removed branches and values. The logical branches of data 
structures in particular provide for the ease of custom data sets.
The in-memory data could be serialized as JSON files for persistent storage and reuse. 

The 'jsondata' package provides a standards conform layer for the processing of JSON
based data with emphasis on in-memory performance and low resource consume.
The implementation integrates seamless into the standard interfaces of Python(>=2.7),
whereas higher level features of additional standards are introduced on top.

The main interface classes are:

* **JSONData** - Core for RFC7159 based data structures. Provides modular data components.

* **JSONDataSerializer** - Core for RFC7159 based data persistence. Provides modular data serialization.

* **JSONPointer** - RFC6901 for addressing by pointer paths. Provides pointer arithmetics.

* **JSONPatch** - RFC6902 for modification by patch lists. Provides the assembly of modular patch entries and the serialization of resulting patch lists.

* **JSONCompute** - Lightweight DSL interpreter and compiler for JSON data and basic syntax components.

The syntax primitives of underlying layers are provided 
by the imported packages '**json**' or the package ultra-json '**ujson**', and '**jsonschema**' in conformance to related ECMA and RFC 
standards and proposals. Here ECMA-262, ECMA-404, RFC7159/RFC4627, 
draft-zyp-json-schema-04, and others.

The architecture is based on the packages 'json' or 'ujson', and
'jsonschema'::

                   +-------------------------+
    Applications   |    application-layer    |
                   +-------------------------+  
    .   .  .  .  .  . | .  .  . | .  .  .  | .  .  .  .  .  .  .  .  .
                   + - - - - - - - - - - - - +
    Process JSON   |         JSON-DSL        |
                   + - - - - - - - - - - - - +
    .   .  .  .  .  . | .  .  . | .  .  .  | .  .  .  .  .  .  .  .  .
                      |         V          |     
                      |   +----------+     |         RFC6901
    Data              |   | jsondata |     |         RFC6902
    Structures        |   +----------+     |         +others +extensions
                      |      |    |        |
    .  .  .  .  .  .  | .  . | .  | .  .  .| .  .  .  .  .  .  .  .  .
                      +---+--+    +---+----+           
                          |           |                           
                          V           V                            
                   +------------+------------+       RFC7159/RFC4267
    JSON           |    json,   | jsonschema |       ECMA-262/ECMA-404    
    Syntax         |    ujson   |            |       draft-zyp-json-schema-04   
                   +------------+------------+

The examples from the standards with some extensions, are included in order to 
verify implementation details for the recommendations.
This serves also as a first introduction to JSON processing with the
package 'jsondata'.
For the compliance tests extracted from IETF and ECMA standards refer to the directories:

* UseCases
 
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

After successful installation the 'selftest' verifies basic checks by:

  *jsondatacheck --selftest*

with the exit value '0' when OK.

The option '-v' raises the degree of verbosity for inspection

  *jsondatacheck --selftest -v -v -v -v*
 

Project Data
------------

* PROJECT: 'jsondata'

* MISSION: Provide and extend JSONPointer and JSONPatch - RFC6901, RFC6902

* VERSION: 00.02.003

* RELEASE: 00.02.003

* STATUS: alpha

* AUTHOR: Arno-Can Uestuensoez

* COPYRIGHT: Copyright (C) 2010,2011,2015-2016 Arno-Can Uestuensoez @Ingenieurbuero Arno-Can Uestuensoez

* LICENSE: Artistic-License-2.0 + Forced-Fairplay-Constraints
  Refer to enclose documents:
  
  *  ArtisticLicense20.html - for base license: Artistic-License-2.0 

  *  licenses-amendments.txt - for amendments: Forced-Fairplay-Constraints

VERSIONS and RELEASES
---------------------

**Planned Releases:**

* RELEASE: 00.00.00x - Pre-Alpha: Extraction of the features from hard-coded application into a reusable package.

* RELEASE: 00.01.00x - Alpha: Completion of basic features. 

* RELEASE: 00.02.00x - Alpha: Completion of features, stable interface. 

* RELEASE: 00.03.00x - Beta: Accomplish test cases for medium to high complexity.

* RELEASE: 00.04.00x - Production: First production release. Estimated number of UnitTests := 1000.

* RELEASE: 00.05.00x - Production: Various performance enhancements.


**Current Release: 00.02.004 - Alpha:**

Major Changes:

* General fixes and enhancements .

* Split UnitTests

* Split Use-Cases as UnitTests

* Added JSONCompute, a first version of a lightweight JSON DSL. This module is pre-alpha.

* Introduced test for Use-Cases of JSON processing with 'jsondata' by 'tests.05_jsondata_use_cases'.

* Added generic class methods for tree diff and tree pointer evaluation. Works on raw data from 'json' and 'ujson'.

* Added some first operators on JSONPatch and JSONPatchItem for RFC6902.

Current test status:

* UnitTests: >553

* Use-Cases as UnitTests: >301

**Total**: >864


**REMARK**: Due to a bug within the PyPi-Hosting software the daily0 counter is broken, just ignore it. For further information refer to::

* [pypi:support-requests] #615 Doenload counter partially broken since about 7days  (including additional comments)

       https://sourceforge.net/p/pypi/support-requests/615/

Before about the 1.4.2016 it was between about 100/day sustained up to 800/day after updates. Thus the counters do not reflect the actual amount of distribution until the fix of the bug.
