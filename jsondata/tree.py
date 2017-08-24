# -*- coding:utf-8   -*-
"""The JSONTree module provides features for in-memory JSON structures.

The provided features comprise:

* The construction and printout of tree formatted 
  structures for screen analysis.
* Comparison of JSON strings as tree structures.


"""
import logging
from enum import Enum

try:
    import ujson as myjson
except ImportError:
    import json as myjson

__author__ = 'Arno-Can Uestuensoez'
__author_email__ = 'acue_sf2@sourceforge.net'
__maintainer__ = 'Vladimir Bolshakov'
__maintainer_email__ = 'vovanbo@gmail.com'
__license__ = "Artistic-License-2.0 + Forced-Fairplay-Constraints"
__copyright__ = "Copyright (C) 2015-2016 Arno-Can Uestuensoez " \
                "@Ingenieurbuero Arno-Can Uestuensoez"
__version__ = '0.2.18'
__uuid__ = '63b597d6-4ada-4880-9f99-f5e0961351fb'

logger = logging.getLogger(__name__)


class Diff(Enum):
    FIRST = 'first'  # break display of diff after first
    ALL = 'all'      # list all diffs


class Charset(Enum):
    RAW = 'raw'  # display character set as raw
    STR = 'str'  # display character set as str
    UTF = 'utf'  # display character set as utf


class LineFit(Enum):
    CUT = 'cut'     # force line fit
    WRAP = 'wrap'   # wrap line in order to fit to length


class JSONTree(object):
    def __init__(self, scope=Diff.ALL, line_fit=LineFit.WRAP, line_width=60,
                 charset=Charset.RAW, indent=4):
        """Create an object for the tree representation.

        Args:
            scope:

                * all: Display all diffs.
                * first: Display first diff only.

                default:=first

            charset:

                * raw: Use 'raw'.
                * str: Use 'str'.
                * utf: Use 'utf'.

                default:=raw

            debug:

                Add developer information.

            line_fit:

                * cut: Cut lines to length.
                * wrap: Split lines to length.

                default:=wrap

            indent=#numchars:

                Number of characters for indentation.

            line_width=#numchars:

                Length of lines.

        Returns:
            When successful returns 'True', else raises an exception.

        Raises:
            passed through exceptions:
            
        """
        self.diff_list = []

        assert isinstance(scope, Diff), \
            'Enumeration of Diff is required.'
        assert isinstance(charset, Charset), \
            'Enumeration of Charset is required.'
        assert isinstance(line_fit, LineFit), \
            'Enumeration of LineFit is required.'

        self.scope = scope
        self.line_fit = line_fit
        self.line_width = line_width
        self.charset = charset
        self.indent = indent

        self.level_top = None
        self.level_bottom = None
        self.delta = None
        self.path_only = None

    def print_diff(self):
        """
        Prints out the resulting list of differences.

        Args:
             ffs.

        Returns:
            When successful returns tree represantation.

        Raises:
            passed through exceptions:

        """
        ret = ""
        _i = " " * self.indent
        w = self.line_width

        for d in self.diff_list:
            if w and self.line_fit is LineFit.CUT:
                ret += "path=%s\n" % d['p']
                line = "%sn0%s = %s" % (_i, d['p'], d['n0'])
                ret += '%s\n' % line[:w]
                line = "%sn1%s = %s" % (_i, d['p'], d['n1'])
                ret += '%s\n' % line[:w]
            elif w and self.line_fit is LineFit.WRAP:
                ret += "path=%s\n" % d['p']
                line = "%sn0%s = %s" % (_i, d['p'], d['n0'])
                while line:
                    ret += '%s\n' % line[:w]
                    line = line[w:]
                    if line:
                        ret += _i * 2
                line = "%sn1%s = %s" % (_i, d['p'], d['n1'])
                while line:
                    ret += '%s\n' % line[:w]
                    line = line[w:]
                    if line:
                        ret += _i * 2
            else:
                ret += "path=%s\n" % d['p']
                ret += "  n0%s = %s\n" % (d['p'], d['n0'])
                ret += "  n1%s = %s\n" % (d['p'], d['n1'])

        return ret

    def fetch_diff(self, n0, n1, p=None, dl=0):
        """Recursive tree compare for Python trees as used for the package 'json'.
        
        Finds diff in native Python trees assembled by the standard package 'json'
        and compatible, e.g. 'ujson'.
        
        
        * level_top
        * level_bottom
        * delta (for containers)
        * scope(all, first)
        * line_width
        * displaycharset (str,utf)
        * path_only
        
        Args:

            n0:

                JSON string of type 'str', or 'unicode'

            n1:

                JSON string of type 'str', or 'unicode'

            p=[]:


                Result entries for each difference:
                    ::

                        {'n0':n0,'n1':n1,'dl':dl,'p':p[:]}

                    #. first JSON data
                    #. second JSON data
                    #. diff count increment value
                    #. current diff including path

                List of differences as of:
                
                #. non equal types are different: type(n0) != type(n1)
                #. equal types, both list: type(n0) is list

                    #. length is different: len(n0.keys()) != len(n1.keys())
                    #. at leats one item is different: n1.get(ni) and v != n1[ni]

                #. equal types, both dict: type(n0) is dict and type(n1) is dict 

                    #. length is different: len(n0.keys()) != len(n1.keys())
                    #. at leats one item is different: n1.get(ni) and v != n1[ni]

                default:=0

        Returns:
            When no diffs returns True, else False or raises an exception.
            The resulting differences are contained in the provided 
            list parameter 'p'. When not provided the resulting list 
            is suppressed. 

        Raises:
            passed through exceptions:
            
        """
        ret = True

        self.level_top = -1
        self.level_bottom = -1
        self.delta = False
        self.path_only = False

        # assure JSON strings
        if isinstance(n0, str):
            n0 = str(n0)
        if isinstance(n1, str):
            n1 = str(n1)

        dl += 1
        p = p if p is not None else []

        if type(n0) is not type(n1):  # non equal types are different
            logger.debug('type: %s != %s', type(n0), type(n1))
            self.diff_list.append({
                'n0': n0,
                'n1': n1,
                'dl': dl,
                'p': p[:]
            })
            ret &= False

        elif isinstance(n0, list):  # equal types, both list
            if len(n0) != len(n1):
                logger.debug('len: %s != %s', len(n0), len(n1))
                self.diff_list.append({
                    'n0': n0,
                    'n1': n1,
                    'dl': dl,
                    'p': p[:]
                })
                ret &= False
            else:
                for ni in range(0, len(n0)):
                    if not p:
                        pni = [ni]
                    else:
                        pni = p[:]
                        pni.append(ni)
                    ret &= self.fetch_diff(n0[ni], n1[ni], pni, dl)

                    if self.scope is Diff.FIRST:
                        if not ret:
                            break

        elif isinstance(n0, dict):
            if len(list(n0.keys())) != len(list(n1.keys())):
                logger.debug('len: %s != %s', len(n0.keys()), len(n1.keys()))
                self.diff_list.append({
                    'n0': n0,
                    'n1': n1,
                    'dl': dl,
                    'p': p[:]
                })
                ret &= False

            else:
                for ni, v in list(n0.items()):
                    if not p:
                        pni = [ni]
                    else:
                        pni = p[:]
                        pni.append(ni)
                    if n1.get(ni) and v != n1[ni]:
                        logger.debug('item(%s): %s != %s', ni, v, n1[ni])
                        if isinstance(v, (list, dict)):
                            ret &= self.fetch_diff(v, n1[ni], pni, dl)
                        else:
                            self.diff_list.append({
                                'ni': ni,
                                'n0': n0[ni],
                                'n1': n1[ni],
                                'dl': dl,
                                'p': p[:]
                            })
                            ret &= False

                        if self.scope is Diff.FIRST and not ret:
                            break

                    elif isinstance(v, (list, dict)):
                        ret &= self.fetch_diff(v, n1[ni], pni, dl)

        else:  # invalid types may have been eliminated already
            if n0 != n1:
                self.diff_list.append({
                    'n0': n0,
                    'n1': n1,
                    'dl': dl,
                    'p': p[:]
                })
                ret &= False

        return ret
