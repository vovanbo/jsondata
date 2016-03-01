"""Test PyUnit environment.
"""
from __future__ import absolute_import

import unittest
import doctest

import os
#import sys

#
#######################
#
class CallUnits(unittest.TestCase):
    name=os.path.curdir+__file__

    output=True
    output=False

    def testCase000(self):
        assert 0==0
        pass

    def testCase001(self):
        assert 0!=1
        pass


    def runTest( self ):
        try:
            import examp
        except ImportError, e:
            self.Fail( str( e ) )

#
#######################
#
#
#######################
#
if __name__ == '__main__':
    unittest.main()


# mport unittest
#    2 import doctest
#    3
#    4 class DeviceTest( unittest.TestCase ):
#    5     # This is a simple test that just tries to load the module
#    6     def runTest( self ):
#    7         try:
#    8             import examp
#    9         except ImportError, e:
#   10             self.Fail( str( e ) )
