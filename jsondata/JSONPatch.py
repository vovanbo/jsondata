# -*- coding:utf-8   -*-
"""JSONPatch based on RFC6902.

**REMARK**: This modules status is non-production - development-only release. Available soon!


- Manages one JSONPatch task
- Reads and writes Sources
- Creates JSONPatch from branch_diff
...
"""
__author__ = 'Arno-Can Uestuensoez'
__license__ = "Artistic-License-2.0 + Forced-Fairplay-Constraints"
__copyright__ = "Copyright (C) 2015-2016 Arno-Can Uestuensoez @Ingenieurbuero Arno-Can Uestuensoez"
__version__ = '0.1.0'
__uuid__='63b597d6-4ada-4880-9f99-f5e0961351fb'

import os,sys

version = '{0}.{1}'.format(*sys.version_info[:2])
if version < '2.7': # pragma: no cover
    raise Exception("Requires Python-2.7.* or higher")

import json, jsonschema
from StringIO import StringIO

# Sets display for inetractive JSON/JSONschema design.
_interactive = False

class JSONPatchItem(object):
    """
    
    Attributes:
        op: operations:
                add, copy, move, remove, replace, test
        target:
        value:
        src:
        
        
    """
    def __init__(self,op,target,param):
        """

        Args:
            op: Operation: add, copy, move, remove, replace, test

            target: Target node.        
            param: Parameter specific for the operation:
                value: add,replace, test
                src: copy, move, remove
        Returns:
            When successful returns 'True', else returns either 'False', or
            raises an exception.
            Success is the complete addition only, thus one failure returns
            False.

        Raises:
            JSONDataSerializerError:
        
        """
        pass
    
    def apply(self):
        pass

    def __repr__(self):
        pass
    
    def __str__(self):
        pass


class JSONPatch(object):
    """ Representation of a JSONPatch task.
    
    * add
    * remove
    * replace
    * move
    * copy
    * test
     
    Attributes:
        patch: List of patch items.
        
    """
    def __init__(self):
        self.patch = []
        
        pass

    #
    #--- RFC6902 JSON patch files
    #
    def patch_export(self):
        pass

    def patch_import(self):
        pass

    #
    #--- RFC6902 operations
    #
    def op_add(self,target,value):
        pass

    def op_copy(self,target,src):
        pass
    
    def op_move(self,target,src):
        pass
    
    def op_remove(self,target):
        pass
    
    def op_replace(self,target,value):
        pass
    
    def op_test(self,target,value):
        pass
    
    #
    #--- controller
    #
    
    def iterator_items(self):
        """
        """
        pass

    def apply(self):
        """Applies the JSONPatch task.
        """
        pass

    def __add__(self,x):
        """Adds items to the JSONPatch task.
        
        Adds a list of items to the current list of items.
        """
        pass

    def __iadd__(self,x):
        """Adds items to the JSONPatch task in place.
        
        Adds a list of items to the current list of items.
        """
        pass

    def __repr__(self):
        """Prints the representation format.
        """
        pass
    
    def __str__(self):
        """Prints the display format.
        """
        pass


    def task(self):
        pass

    def merge_patch(self):
        pass

