# -*- coding:utf-8   -*-
"""The JSONTree module provides features for in-memory JSON structures.

The provided features comprise:

* The construction and printout of tree formatted 
  structures for screen analysis.
* Comparison of JSON strings as tree structures.


"""
try:
    import ujson as myjson
except ImportError:
    import json as myjson

__author__ = 'Arno-Can Uestuensoez'
__maintainer__ = 'Arno-Can Uestuensoez'
__license__ = "Artistic-License-2.0 + Forced-Fairplay-Constraints"
__copyright__ = "Copyright (C) 2015-2016 Arno-Can Uestuensoez @Ingenieurbuero Arno-Can Uestuensoez"
__version__ = '0.2.18'
__uuid__ = '63b597d6-4ada-4880-9f99-f5e0961351fb'

DIFF_FIRST = 0
"""break display of diff after first"""

DIFF_ALL = 1
"""list all diffs"""

CHARS_RAW = 0
"""display character set as raw"""

CHARS_STR = 1
"""display character set as str"""

CHARS_UTF = 2
"""display character set as utf"""

LINE_CUT = 0
"""force line fit"""

LINE_WRAP = 1
"""wrap line in order to fit to length"""


class JSONTree(object):
    def __init__(self, **kwargs):
        """Create an object for the tree representation.

        Args:
            **kwargs: Parameter specific for the operation,

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

                linefit:
                    
                    * cut: Cut lines to length.
                    * wrap: Split lines to length.
    
                    default:=wrap
    
                indent=#numchars:

                    Number of characters for indentation.
    
                linewidth=#numchars:

                    Length of lines.

                verbose:

                    Add progress and status dialogue output.

        Returns:
            When successful returns 'True', else raises an exception.

        Raises:
            passed through exceptions:
            
        """
        self.verbose = False
        self.debug = False
        self.difflist = []

        self.scope = DIFF_ALL
        self.linefit = LINE_WRAP
        self.linewidth = 60
        self.charset = CHARS_RAW
        self.indent = 4

        for k, v in list(kwargs.items()):
            if k in ("scope"):
                if v in ('all', DIFF_ALL):
                    self.scope = DIFF_ALL
                elif v in ('first', DIFF_FIRST):
                    self.scope = DIFF_FIRST
                else:
                    self.scope = DIFF_FIRST

            elif k in ("charset"):
                if v in ('raw', CHARS_RAW):
                    self.charset = CHARS_RAW
                elif v in ('str', CHARS_STR):
                    self.charset = CHARS_STR
                elif v in ('utf', CHARS_UTF):
                    self.charset = CHARS_UTF
                else:
                    self.charset = CHARS_RAW

            elif k in ("linefit"):
                if v in ('cut', LINE_CUT):
                    self.linefit = LINE_CUT
                elif v in ('wrap', LINE_WRAP):
                    self.linefit = LINE_WRAP
                else:
                    self.linefit = LINE_WRAP

            elif k in ("indent"):
                if type(v) is int:
                    self.indent = v

            elif k in ("linewidth"):
                if type(v) is int:
                    self.linewidth = v

            elif k in ("verbose"):
                self.verbose = True

            elif k in ("debug"):
                self.debug = True

    def printDiff(self):
        """Prints out the resulting list of differences.

        Args:
             ffs.

        Returns:
            When successful returns tree represantation.

        Raises:
            passed through exceptions:

        """
        ret = ""
        _i = " " * self.indent
        w = self.linewidth

        for d in self.difflist:
            if w and self.linefit == LINE_CUT:
                ret += "path=" + str(d['p']) + "\n"
                line = _i + "n0" + str(d['p']) + " = " + str(d['n0'])
                ret += line[:w] + "\n"
                line = _i + "n1" + str(d['p']) + " = " + str(d['n1'])
                ret += line[:w] + "\n"
            elif w and self.linefit == LINE_WRAP:
                ret += "path=" + str(d['p']) + "\n"
                line = _i + "n0" + str(d['p']) + " = " + str(d['n0'])
                while line:
                    ret += line[:w] + "\n"
                    line = line[w:]
                    if line:
                        ret += _i * 2
                line = _i + "n1" + str(d['p']) + " = " + str(d['n1'])
                while line:
                    ret += line[:w] + "\n"
                    line = line[w:]
                    if line:
                        ret += _i * 2
            else:
                ret += "path=" + str(d['p']) + "\n"
                ret += "  n0" + str(d['p']) + " = " + str(d['n0']) + "\n"
                ret += "  n1" + str(d['p']) + " = " + str(d['n1']) + "\n"

        return ret

    def fetchDiff(self, n0, n1, p=[], dl=0):
        """Recursive tree compare for Python trees as used for the package 'json'.
        
        Finds diff in native Python trees assembled by the standard package 'json'
        and compatible, e.g. 'ujson'.
        
        
        * leveltop
        * levelbottom
        * delta (for containers)
        * scope(all, first)
        * linewidth
        * displaycharset (str,utf)
        * pathonly
        
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

        self.leveltop = -1
        self.levelbottom = -1
        self.delta = False
        self.pathonly = False

        # assure JSON strings
        if type(n0) is str:
            n0 = str(n0)
        if type(n1) is str:
            n1 = str(n1)

        dl += 1

        if type(n0) != type(n1):  # non equal types are different
            if self.verbose:
                print('type:' + str(type(n0)) + ' != ' + str(type(n1)))
            self.difflist.append({'n0': n0, 'n1': n1, 'dl': dl, 'p': p[:]})
            ret &= False

        elif type(n0) is list:  # equal types, both list
            if len(n0) != len(n1):
                if self.verbose:
                    print('len:' + str(len(n0)) + ' != ' + str(len(n1)))
                self.difflist.append({'n0': n0, 'n1': n1, 'dl': dl, 'p': p[:]})
                ret &= False
            else:
                for ni in range(0, len(n0)):
                    if not p:
                        pni = [ni]
                    else:
                        pni = p[:]
                        pni.append(ni)
                    ret &= self.fetchDiff(n0[ni], n1[ni], pni, dl)

                    if self.scope == DIFF_FIRST:
                        if not ret:
                            break

        elif type(n0) is dict:

            if len(list(n0.keys())) != len(list(n1.keys())):
                if self.verbose:
                    print('len:' + str(len(list(n0.keys()))) + ' != ' + str(
                        len(list(n1.keys()))))
                self.difflist.append({'n0': n0, 'n1': n1, 'dl': dl, 'p': p[:]})
                ret &= False

            else:
                for ni, v in list(n0.items()):
                    if not p:
                        pni = [ni]
                    else:
                        pni = p[:]
                        pni.append(ni)
                    if n1.get(ni) and v != n1[ni]:
                        if self.verbose:
                            print('item(' + str(ni) + '):' + str(
                                v) + ' != ' + str(n1[ni]))
                        if type(v) in (list, dict):
                            ret &= self.fetchDiff(v, n1[ni], pni, dl)
                        else:
                            self.difflist.append(
                                {'ni': ni, 'n0': n0[ni], 'n1': n1[ni], 'dl': dl,
                                 'p': p[:]})
                            ret &= False

                        if self.scope == DIFF_FIRST:
                            if not ret:
                                break

                    elif type(v) in (list, dict):
                        ret &= self.fetchDiff(v, n1[ni], pni, dl)

        else:  # invalid types may have been eliminated already
            if n0 != n1:
                self.difflist.append({'n0': n0, 'n1': n1, 'dl': dl, 'p': p[:]})
                ret &= False

        return ret
