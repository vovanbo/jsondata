# -*- coding:utf-8   -*-
"""Provides classes for computing of JSON data.

"""
__author__ = 'Arno-Can Uestuensoez'
__license__ = "Artistic-License-2.0 + Forced-Fairplay-Constraints"
__copyright__ = "Copyright (C) 2015-2016 Arno-Can Uestuensoez @Ingenieurbuero Arno-Can Uestuensoez"
__version__ = '0.2.2'
__uuid__='63b597d6-4ada-4880-9f99-f5e0961351fb'

import sys,os

version = '{0}.{1}'.format(*sys.version_info[:2])
if version < '2.7': # pragma: no cover
    raise Exception("Requires Python-2.7.* or higher")

from types import StringTypes,NoneType
import re
try:
    from urllib import unquote
    from itertools import izip
    # str = unicode
except ImportError: # Python 3
    from urllib.parse import unquote
    izip = zip


# Sets display for inetractive JSON/JSONschema design.
_interactive = False

# Notation a the API - in/out.
NOTATION_JSON = 0 # this is the default
"""JSON notation in accordance to RFC7159
"""

NOTATION_HTTP_FRAGMENT = 1
"""JSON notation in accordance to RFC7159 with RFC3986.
"""

VALID_NODE_TYPE = (dict, list, str, unicode, int, float, bool, NoneType,)
"""Valid types of in-memory JSON node types."""


CHARSET_UTF = 0
"""Unicode."""

CHARSET_STR = 1
"""Python string."""


POINTER_JSON = re.compile('[/]([^/]*)')
"""A pointer presentation as RFC6901 string."""

POINTER_PYTHON = re.compile('[\[]([^\]]*)\]')
"""A pointer presentation as Python syntax."""

#
# Stored result
RESULT_RFC6901 = 0
RESULT_PATHLIST = 1
RESULT_PATHLIST_KEY = 2
RESULT_OBJECT = 3

# tokens
_GROUPBEG = '('
_GROUPEND = ')'
_STR = '"'

_ASSIGN = '='

# keyword tokens
_PTR='ptr'
_PTRSTART='ptr('
_CALC='calc'
_CALCSTART='calc('
_COPY = 'copy'
_COPYSTART = 'copy('
_DEL = 'del'
_DELSTART = 'del('
_EVAL = 'eval'
_EVALSTART = 'eval('
_DATA = 'data'
_DATASTART = 'data('
_DATAFILE = 'datafile'
_DATAFILESTART = 'datafile('
_SCHEMA = 'schema'
_SCHEMASTART = 'schema('
_SCHEMAFILE = 'schemafile'
_SCHEMAFILESTART = 'schemafile('
_STRBEG = 'str('

# keywords
_keywords = (
    _ASSIGN, 
    _PTR,    
    _PTRSTART,    
    _STRBEG,    
#     _GROUPBEG, 
#     _GROUPEND, 
    _CALC,
    _CALCSTART,
    _COPY,
    _COPYSTART,
    _DEL,
    _DELSTART,
    _EVAL, 
    _EVALSTART, 
    _DATA, 
    _DATASTART, 
    _DATAFILE, 
    _DATAFILESTART, 
    _SCHEMA, 
    _SCHEMASTART, 
    _SCHEMAFILE, 
    _SCHEMAFILESTART,
)

# solo
_keyssolo = (
    _ASSIGN, 
)

# begin keywords
_groups = (
    _PTR,
    _CALC,
    _EVAL,
    _STR,
    _COPY,
    _DEL,
)

from jsondata.JSONDataExceptions import JSONDataException
class JSONComputeException(JSONDataException):
    """ Error on a value."""
    def __str__(self):
        return "JSONDataException:"+self.s

class JSONCompute(list):
    """Computing of simple JSONPointer syntax string based on RFC6901.

    For additional information refer to the documentation.

    """

    def __init__(self,pjson,**kargs):
        """Creates a computing object and performs the syntax string 'pjson'.
        
        Args:
            pjson: A list with JSON pointer values and supported 
                operations.
                
            **kargs: 
                'jsondata': When present evaluates the value of
                    the pointer. When 'None', pointer operations only.
                
                'debug': Display developer information.
                
                'verbose': Display user processing information.

        Returns:
            Returns an object containing the result.
            
        Raises:
            JSONPointerException:
            forwarded from json

        """
        self.debug = False
        self.values = False
        self.appname = 'default'
        self.result = None

        _ka = {}
        for k,v in kargs.items():
            if k == 'appname':
                self.appname = v
            elif k == 'values':
                self.values = True
            elif k == 'debug':
                self.debug = True
                _ka['debug'] = True
            elif k == 'verbose':
                self.verbose = True
                _ka['verbose'] = True

        self.charset = CHARSET_UTF
        output = RESULT_RFC6901 # RFC6901
        
        if pjson:
            if pjson[0] == 'json':
                output = RESULT_RFC6901
                pjson = pjson[1:]
            elif pjson[0] == 'python':
                output = RESULT_PATHLIST
                pjson = pjson[1:]
            elif pjson[0] == 'pythonkey':
                output = RESULT_PATHLIST_KEY
                pjson = pjson[1:]
            elif pjson[0] == 'object':
                output = RESULT_OBJECT
                pjson = pjson[1:]
        
        #
        # For now a simplified approach...
        #
        smin0 = [] # mini stack - stage0
        smin1 = [] # mini stack - stage1
        smin2 = [] # mini stack - stage2
        self.resolveSyn(pjson,smin0,0) # resolve non-logical ops on pointers
        if self.values:
            self.resolveSyn(smin0,smin1,1) # resolve pointed document values
            res = self.resolveSyn(smin1,smin2,2) # resolve logical ops
        else:
            res = self.resolveSyn(smin0,smin2,2) # resolve logical ops
            
        # for later recall
        if output == RESULT_RFC6901: #default
            self.result = res 
        elif output == RESULT_PATHLIST:
            self.result = JSONPointer(res,**_ka).get_path_list()
        elif output == RESULT_PATHLIST_KEY:
            self.result = JSONPointer(res).get_path_list_and_key()
        else:
            self.result = JSONPointer(res)

        if __debug__:
            if self.debug:
                print "result="+str(res)

    #
    # operators
    #

    def __add__(self,x):
        return self.result + x

    def __eq__(self,x):
        return self.result == x

    def __ge__(self,x):
        return self.result >= x

    def __gt__(self,x):
        return self.result > x

    def __iadd__(self,x):
        self.result += x
        return self

    def __le__(self,x):
        return self.result <= x

    def __lt__(self,x):
        return self.result < x

    def __ne__(self,x):
        return self.result != x

    def __radd__(self,x):
        if x == '': # whole document, RFC6901
            return u'/'+u'/'.join(map(unicode,self.result))
        elif x == u'/': # empty tag
            return x+u'/'+u'/'.join(map(unicode,self.result))
        elif type(x) is int:
            return u'/'+unicode(x)+u'/'+u'/'.join(map(unicode,self.result))
        elif type(x) in (str,unicode):
            return x+u'/'+u'/'.join(map(unicode,self.result))
        elif type(x) == list:
            return x.extend(self.result)
        else:
            raise JSONComputeException()
        return x

    def __repr__(self):
        if self.charset == CHARSET_STR:
            return str(self.result)
        else:
            return unicode(self.result)

    def __str__(self):
        """Print either UTF, or Python string.
        """
        if self.charset == CHARSET_STR:
            return str(self.result)
        else:
            return unicode(self.result)


    #
    # methods
    #
    def resolveSyn(self,instack,outstack,*args):
        """Syntax resolver for parsed tokens in an array.
        
        Expects a list of tokens contained in an array. The tokens
        could be processed in multiple stages appropriate for the 
        requested stage:
            0: Tokens to be canonized.
            1: Canonized tokens to be calculated.
            2: Calculated tokens and logic operations

        Args:
            instack: A list with extended JSON tokens to 
                be processed.
        
            outstack: A list with processed JSON tokens.
                
            *args:
                args[0]:=stage: The stage of processing.
                    The current parsing is designed as simplified
                    staged processing.
                        0: Calculate pointer operations.
                        
                        1: Resolve requested document values.
                        
                        2: Process logical operators.
 
                    default:=0
                    
                args[1]:=startindex: The index in 'intstack' to begin.
                    
                    default:=0
                    
                args[2]:=data: The default JSON document.
                    
                    default:=None
                    
                args[3]:=schema: The default JSON schema.
                    
                    default:=None
   
        Returns:
            Returns an object containing the result.
            
        Raises:
            JSONPointerException:
            forwarded from json
    
        """
        
        _ineval = 0 #FIXME:
        
        res = None # result
        ops = None # current operations
        grp = None

        stage = 0 # processing stage
        data=None # data
        schema=None # schema for validation

        ingroup = False # is in group
        _ingroup = 0
        
        cnt = [0] # start index
        gcall = 0 # is in single group call
        
        i = 0
        for a in args:
            if i == 0:
                stage = a
            elif i == 1:
                cnt = a
                _first = a[0]
            elif i == 2:
                gcall = a
            elif i == 3:
                data = a
            elif i == 4:
                schema = a
            i += 1

        if __debug__:
            if self.debug:
                print "\n#***\n#\nstage="+str(stage)
                print "instack="+str(instack)

        cntmax = len(instack) #FIXME: for recursion
        _first = cnt[0]
        
        while cnt[0] < cntmax:
            syn = instack[cnt[0]]
            if __debug__:
                if self.debug:
                    print "\n#---\nsyn("+str(stage)+"."+str(cnt[0])+")="+str(syn)
            
            #
            # mapped methods on operators
            #    
            if syn == '==':
                ops = JSONPointer.__eq__
            elif syn == '!=':
                ops = JSONPointer.__ne__
            elif syn == '>': 
                ops = JSONPointer.__gt__
            elif syn == '>=':
                ops = JSONPointer.__ge__
            elif syn == '<':
                ops = JSONPointer.__lt__
            elif syn == '<=':
                ops = JSONPointer.__le__
            elif syn == '+':
                ops = JSONPointer.__add__


            #
            # group defining keywords - include parameter lists
            #
            elif syn in _groups:
                grp = syn
                ops = syn
                if _first == cnt[0] and instack[cnt[0]+1] is _GROUPBEG:
                    cnt[0] += 1
                    ops += _GROUPBEG
                


            #
            # braces
            #
            elif syn is _GROUPBEG: # '(' - currently no error checks in tokens
                
                if ingroup: # open nested subgroup by recursion
                    if not ops: # no operations defined
                        res += self.resolveSyn(instack,outstack,stage,cnt,True)
                    elif not type(ops) is str: # operations is a function pointer
                        cnt[0] += 1
                        res += self.resolveSyn(instack,outstack,stage,cnt,True)
                    elif ops in _keyssolo: # operations is a stadalone-key, e.g. '='
                        cnt[0] += 1
                        res += self.resolveSyn(instack,outstack,stage,cnt,True)
                    else: # operations is a common function call, e.g. 'calc'
                        if grp:
                            cnt[0] -= 1
                        res += self.resolveSyn(instack,outstack,stage,cnt,True)

                else: # opens a new group
                    if ops and type(ops) is str:
                        if not ops in _keyssolo: # key with parameters, transform ops to start key
                            ops += syn # combine group and keyword
#                     if grp:
#                         ops = grp+syn # combine group and keyword
                    ingroup = True
                    cnt[0] += 1
                
                continue

            elif syn is _GROUPEND: # ')' - current level group finished 
                if gcall: # resolve one group only
                    cnt[0] += 1
                    return res
                grp = None
                ingroup = False # group on current level finished

            #
            # keyword operators
            #
            elif syn in _keywords:
                ops = syn # keyword known

            #
            # Values
            #
            elif type(JSONPointer.__init__) == type(syn): # pointer value
                ops = syn

    
            #                   
            # computing stages
            #
            else:
                
                if stage == 0: # canonize pointer, reduce pointer ops

                    #
                    # canonize
                    #           
                    if type(syn) is list: # internal list
                        #syn = JSONPointer(syn)
                        if type(res) != NoneType and not ops:
                            res = syn # missing operator, just replace the last 
                        pass

                    elif isinstance(syn,JSONPointer): # pointer object
                        if type(res) != NoneType and not ops:
                            res = syn # missing operator, just replace the last
                        pass

                    else: # string or int
                        if type(syn) in (int,float,): # integer
                            if type(res) != NoneType and not ops:
                                res = '/'+unicode(syn) # missing operator, just replace the last
                            pass

                        elif type(syn) in (str, unicode,): # string
                            if syn[0] != '/':
                                syn = '/' + syn
                            pointer = re.findall(POINTER_PYTHON,syn)
                            if not pointer:
                                pointer = re.findall(POINTER_JSON,syn)
                            if not pointer:
                                raise JSONComputeException("pointer:invalid:"+str(syn))
                            else:
                                syn = pointer

                            if __debug__:
                                if self.debug:
                                    print "pointer-list:"+str(pointer)

                        if __debug__:
                            if self.debug:
                                print "pointer-rfc6901:"+str(syn)
                                print "ops:"+str(ops)
                                print "res:"+str(res)

                    if not res: # initial
                        #res = JSONPointer(prfc)
                        if not isinstance(syn,JSONPointer): # pointer object
                            res = JSONPointer(syn)
                        else:
                            res = syn
    
                    else: # stages when defined
                        if ops:
                            if ops == JSONPointer.__add__: # calculate sub-results with higher precedence
                                res = ops(res,syn)
                                ops = None
                                
                            elif ops in (_CALCSTART,): 
                                outstack.append(res)
                                outstack.append(ops)
                                ops = None
                                _ingroup +=1

                            elif ops in (_EVALSTART,): 
                                outstack.append(res)
                                outstack.append(ops)
                                if _ingroup:
                                    raise JSONComputeException("eval:nested:"+str(outstack))
                                ops = None
                                _ingroup +=1

                            elif ops in (_DATASTART,): 
                                outstack.append(res)
                                outstack.append(ops)
                                if _ingroup:
                                    raise JSONComputeException("data:nested:"+str(outstack))
                                ops = None
                                _ingroup +=1

                            elif ops in (_GROUPEND,):
                                outstack.append(res)
                                outstack.append(ops)
                                ops = None                                     
                                _ingroup -=1
                            
                            else: # logical operations
                                outstack.append(res)
                                outstack.append(ops)

                                res = syn
#                                 if type(syn) in JSONPointer: # from string - the most calls
#                                     res = JSONPointer(prfc)
#                                 else:
#                                     res = syn
                                ops = None
    
                    if __debug__:
                        if self.debug:
                            print "result="+str(res)
                
                elif stage == 1: # resolve pointed values
    
                    if ops and ops.startswith('datafile('):
                        data = ops[9:-1]
                        if not os.path.exists(data):
                            raise JSONComputeException("datafile:missing:"+str(ops))
                        _k = {'datafile':data}
                        data = JSONDataSerializer(self.appname,**_k)
                        ops = None
    
                    elif ops and ops.startswith('data('):
                        data = ops[5:-1]
    
                    if type(syn) is int and syn == _GROUPEND: # mark eval group
                        _ineval -=1
                        outstack.append(res)
    
                    elif type(syn) is int and syn == _EVALSTART: # mark eval group
                        _ineval +=1
    
                    elif not res: # initial
                        if _ineval:
                            res = syn.get_node_or_value(self.data)
                        else:
                            res = syn
    
                    else: # process when defined
                        if ops:
                            if ops == res.__add__: # calculate sub-results with higher precedence
                                res = ops(syn)
                                ops = None
                            else: # logical operations
                                outstack.append(res)
                                outstack.append(ops)
                                ops = None
    
                    if __debug__:
                        if self.debug:
                            print "result="+str(res)
    
                elif stage == 2: # resolve logical ops, either on pointers or of pointed values
    
                    if not res: # initial
                        res = syn
                        
                    else: # process when defined
                        if ops:
                            res = ops(res,syn)
                            ops = None
    
                    if __debug__:
                        if self.debug:
                            print "result="+str(res)
            
            cnt[0]+=1

    
        if __debug__:
            if self.debug:
                print "outstack("+str(stage)+")="+str(outstack)
    
        outstack.append(res)
        return res

from jsondata.JSONDataSerializer import JSONDataSerializer
from jsondata.JSONPointer import JSONPointer
