# -*- coding:utf-8   -*-
"""Common exceptions for the package 'jsondata'.
"""
__author__ = 'Arno-Can Uestuensoez'
__license__ = "Artistic-License-2.0 + Forced-Fairplay-Constraints"
__copyright__ = "Copyright (C) 2015-2016 Arno-Can Uestuensoez @Ingenieurbuero Arno-Can Uestuensoez"
__version__ = '0.2.12'
__uuid__='63b597d6-4ada-4880-9f99-f5e0961351fb'

import sys
version = '{0}.{1}'.format(*sys.version_info[:2])
if version < '2.7': # pragma: no cover
    raise Exception("Requires Python-2.7.* or higher")

# Sets display for inetractive JSON/JSONschema design.
_interactive = False

class JSONDataException(Exception):
    """ base Exception."""
    
    def __init__(self,*arg):
        """To be replaced by derived Exceptions.
        
        Fetch standard parameters and forward message to base class 'Exception'.
        """
        self.fetch(*arg)
        Exception.__init__(self,self.s)

    def fetch(self,*arg):
        """Fetch arguments.

        Args:
            *args: The following order is expected:
            
            0. Reason of exception.
            
            1. Name of object that caused the exception.
            
            2. Value of the object.

        Returns:
            None.

        Raises:
            None.
        """
        self.s=""
        for a in arg:
            self.s+=":"+str(a)
        self.s=self.s[1:]
        
    def __repr__(self):
        """Cause: <reason>:<object>:<value>"""
        return self.s

    def __str__(self):
        """Cause with additional header text."""
        return "ERROR::"+self.s

#
# generic exceptions
#

class JSONDataKeyError(JSONDataException,KeyError):
    """ Error on key."""
    
    def __init__(self,*arg):
        JSONDataException.fetch(self,*arg)
        KeyError.__init__(self,self.s)
    
    def __str__(self):
        return "JSONDataKeyError:"+self.s
        
class JSONDataNodeType(JSONDataException):
    """ Error on NodeTypes."""
    def __str__(self):
        return "JSONDataNodeType:"+self.s

class JSONDataParameter(JSONDataException):
    """ Erroneous parameters."""
    def __str__(self):
        return "JSONDataParameter:"+self.s

class JSONDataSourceFile(JSONDataException):
    """ Error on read of a source file."""
    def __str__(self):
        return "JSONDataSourceFile:"+self.s

class JSONDataTargetFile(JSONDataException):
    """ Error on writing a file."""
    def __str__(self):
        return "JSONDataTargetFile:"+self.s

class JSONDataValue(JSONDataException):
    """ Error on a value."""
    def __str__(self):
        return "JSONDataValue:"+self.s



