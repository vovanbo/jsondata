PyUnit tests
============

These tests could either be called from the command line,
or within Eclipse by the plugin PyDev / PyUnit.

* CLI: Python setup.py test 

* Eclipse: Install PyDev, open the view PyUnit and proceed.

a_selftest
----------
Basic self test of PyUnit.

b_system
--------
System API calls for libraries and binaries.

c_libs
------
Provided library modules of 'jsondata' for JSON data.

d_utils
-------
Utilities for the development of 'jsondata'.

Used for build only.

e_tools
-------
Tools of 'jsondata'.

Used for production and development for 'jsondata' itself,
and by the end user and application developers.

f_bins
------
Official binaries of 'jsondata'.

g_datasets
----------
Complex data sets for advanced test cases.

These comprising tests involve sophisticated and exotic
test cases, and large loads for performance validation.
The failure of these tests may not permit the release at
all, but may question the applicability high-end 
environments.
