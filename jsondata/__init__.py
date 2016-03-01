""" Basic features for modular JSON based in-memory data and their persistency.

This package is aimed for the management of modular data structures based on JSON.
The data is foreseen to be represented by an in-memory main data tree with
dynamically added and/or removed branches. The branches of data structures in
particular provide for custom data. The data could either be related to a module,
and/or to specific classes. A typical application for branch data is the persistent
storage of GUI models for dynamically loaded and released user elements.

The main class JSONDataSerializer provides for the serialization and incremental
load.

"""
__author__ = 'Arno-Can Uestuensoez'
__license__ = "Apache-2.0 + Forced-Fairplay-Constraints"
__copyright__ = "Copyright (C) 2015-2016 Arno-Can Uestuensoez @Ingenieurbuero Arno-Can Uestuensoez"
__version__ = '0.0.3'
__uuid__='63b597d6-4ada-4880-9f99-f5e0961351fb'

__package__ = 'jsondata'
#__import__('pkg_resources').declare_namespace(__name__)


# import os
# import sys
# import warnings
# import ConfigParser # ConfigParser is not a virtualenv module, so we can use it to find the stdlib
#
# dirname = os.path.dirname
#
# distutils_path = os.path.join(os.path.dirname(ConfigParser.__file__), 'distutils')
# if os.path.normpath(distutils_path) == os.path.dirname(os.path.normpath(__file__)):
#     warnings.warn("The virtualenv distutils package at %s appears to be in the same location as the system distutils?")
# else:
#     __path__.insert(0, distutils_path)
