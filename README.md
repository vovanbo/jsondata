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
    Process JSON   |         JSON-DSL        |    see package 'jsoncompute'
                   + - - - - - - - - - - - - +    https://pypi.python.org/pypi/jsoncompute
    .   .  .  .  .  . | .  .  . | .  .  .  | .  .  .  .  .  .  .  .  .
                      |         V          |     
                      |   +----------+     |      RFC6901
    Data              |   | jsondata |     |      RFC6902
    Structures        |   +----------+     |      +others +extensions
                      |      |    |        |
    .  .  .  .  .  .  | .  . | .  | .  .  .| .  .  .  .  .  .  .  .  .
                      +---+--+    +---+----+           
                          |           |                           
                          V           V                            
                   +------------+------------+    RFC7159/RFC4267
    JSON           |    json,   | jsonschema |    ECMA-262/ECMA-404    
    Syntax         |    ujson   |            |    draft-zyp-json-schema-04   
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

* VERSION: 00.02

* RELEASE: 00.02

* NICKNAME: 'Mafumo'

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


**Current Release: 00.02.010 - Alpha:**

**Last Alpha release**,following is planned as Beta.

**REMARK**: An intermediate release with support for Linux only.

Major Changes:

* General fixes and enhancements .

* Enhancement of documents by included javadoc like API documentation with Epydoc.

* Platforms: Currently tested on Fedora-Linux only, remaining are going to follow soon.

* Added 'bin/jsondatacheck.py' for Windows support by PATHEXT.
 
Current test status:

* UnitTests: >510

* Use-Cases as UnitTests: >378

**Total**: >888

