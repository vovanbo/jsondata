Use-Cases as PyUnit tests
=========================

These tests could either be called from the command line,
or within Eclipse by the plugin PyDev / PyUnit.

* CLI: '*python setup.py test*' 

* Eclipse: Install PyDev, open the view PyUnit and proceed.

Choose a JSON package, current 'json', or 'ujson':

* Eclipse: set parameters for PyDev testrunner, 
  e.g.: '*--verbosity 0 -- --ujson*'

The tests involve standard, sophisticated and exotic
test cases

The test also include large loads for performance validation.
The failure of the performance tests may not prohibit the release at
all, but may question the applicability for high-end environments.

IETF\_RFC\_compliance
----------------------
Compliance tests of various IETF standards.
Examples and reference cases extracted from 
the standards texts. 

ECMA\_compliance
------------------
Compliance tests of various ECMA standards extracted from 
the standards texts. 

jsondata
---------------------
The most typical use cases for provided classes.

binaries
--------
Official binaries of 'jsondata'.

