PyUnit tests
============

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

10_selftest
-----------
Basic self test of PyUnit by the user tool option
'*jsondatacheck --selftest*'.

20_system
---------
System API calls for libraries and binaries.

30_libs
-------
Provided library modules of 'jsondata' for JSON data.

40_utils
--------
Utilities for the development of 'jsondata'.

Used for build only.

50_tools
--------
Tools of 'jsondata'.

Used for production and development for 'jsondata' itself,
and by the end user and application developers.

60_bins
-------
Official binaries of 'jsondata'.

70_datasets
-----------
Complex data sets for advanced functional test cases.

80_performance
--------------
Complex data sets for advanced performance test cases.

