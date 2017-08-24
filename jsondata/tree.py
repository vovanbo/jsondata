# -*- coding:utf-8   -*-
"""The JSONTree module provides features for in-memory JSON structures.

The provided features comprise:

* The construction and printout of tree formatted 
  structures for screen analysis.
* Comparison of JSON strings as tree structures.


"""
import logging
from collections import Mapping, namedtuple
from enum import Enum
import itertools
import pprint
import textwrap

from .helpers import is_collection, is_iterable_but_not_string

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
    ALL = 'all'  # list all diffs


class Charset(Enum):
    RAW = 'raw'  # display character set as raw
    STR = 'str'  # display character set as str
    UTF = 'utf'  # display character set as utf


class LineFit(Enum):
    CUT = 'cut'  # force line fit
    WRAP = 'wrap'  # wrap line in order to fit to length
    LINE = 'line'  # one-line


def ensure_enum(enum, value):
    if isinstance(value, enum):
        return value
    elif isinstance(value, str):
        return enum(value)
    else:
        raise ValueError(value)


JSONTreeDiff = namedtuple('JSONTreeDiff', 'first second level path key_path')


class JSONTree:
    def __init__(self, scope=Diff.ALL, line_fit=LineFit.WRAP, line_width=60,
                 charset=Charset.RAW, indent=4):
        """
        Create an object for the tree representation.

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
        self.scope = ensure_enum(Diff, scope)
        self.charset = ensure_enum(Charset, charset)
        self.line_fit = ensure_enum(LineFit, line_fit)

        assert isinstance(self.scope, Diff), \
            'Enumeration of Diff is required.'
        assert isinstance(self.charset, Charset), \
            'Enumeration of Charset is required.'
        assert isinstance(self.line_fit, LineFit), \
            'Enumeration of LineFit is required.'

        self.line_width = line_width

        if self.line_fit in (LineFit.CUT, LineFit.WRAP) and not self.line_width:
            raise ValueError('Line width is required for line fit '
                             '"{}"'.format(self.line_fit.value))

        self.indent = indent

        self.level_top = None
        self.level_bottom = None
        self.delta = None
        self.path_only = None

    def _format_diff_line(self, path, key, value):
        indent = ' ' * self.indent
        fmt = '{key}{path} = {value}'

        if self.line_fit is LineFit.CUT:
            return textwrap.indent(
                textwrap.shorten(
                    fmt.format(key=key, path=path, value=value),
                    width=self.line_width, placeholder='...'
                ),
                indent
            )
        elif self.line_fit is LineFit.WRAP:
            return textwrap.indent(
                fmt.format(
                    key=key, path=path,
                    value=pprint.pformat(value, self.indent, self.line_width)
                ),
                indent
            )
        elif self.line_fit is LineFit.LINE:
            return textwrap.indent(
                fmt.format(key=key, path=path, value=value),
                indent
            )

    def _formatted_lines(self, lines):
        for path, diffs in itertools.groupby(lines, key=lambda i: i[0]):
            yield 'path: {}'.format(path)
            for _, key, value in diffs:
                yield self._format_diff_line(path, key, value)

    def print_diff(self):
        """
        Prints out the resulting list of differences.

        Returns:
            When successful returns tree representation.
        """
        lines = (
            (d.key_path or d.path, k, getattr(d, k))
            for d, k in itertools.product(self.diff_list, ('first', 'second'))
        )
        return '\n'.join(self._formatted_lines(lines))

    def _populate_diff(self, first, second, level, path, key_path=None):
        self.diff_list.append(
            JSONTreeDiff(first, second, level, path.copy(), key_path)
        )

    def fetch_diff(self, first, second, path=None, level=0):
        """
        Recursive tree compare for Python trees as used for the package 'json'.
        
        Finds diff in native Python trees assembled by the standard
        package 'json' and compatible, e.g. 'ujson'.
        
        * level_top
        * level_bottom
        * delta (for containers)
        * scope(all, first)
        * line_width
        * displaycharset (str,utf)
        * path_only
        
        Args:

            first: JSON string of type 'str'
            second: JSON string of type 'str'
            path=[]: Result entries for each difference:
                ::

                    {
                        'first': first,
                        'second': second,
                        'level': level,
                        'path': path[:]
                    }

                #. first JSON data
                #. second JSON data
                #. diff count increment value
                #. current diff including path

                List of differences as of:
                
                #. non equal types are different:
                    type(first) != type(second)
                #. equal types, both list:
                    type(first) is list

                #. length is different:
                    len(first.keys()) != len(second.keys())
                #. at leats one item is different:
                    second.get(ni) and v != second[ni]

                #. equal types, both dict:
                    type(first) is dict and type(second) is dict

                #. length is different:
                    len(first.keys()) != len(second.keys())
                #. at leats one item is different:
                    second.get(ni) and v != second[ni]

                default:=0

        Returns:
            When no diffs returns True, else False or raises an exception.
            The resulting differences are contained in the provided 
            list parameter 'path'. When not provided the resulting list
            is suppressed. 

        Raises:
            passed through exceptions:
            
        """
        result = True

        self.level_top = -1
        self.level_bottom = -1
        self.delta = False
        self.path_only = False

        level += 1
        path = path if path is not None else []

        if type(first) is not type(second):  # non equal types are different
            logger.debug('type: %s != %s', type(first), type(second))
            self._populate_diff(first, second, level, path)
            result &= False

        elif is_collection(first):  # equal types, both list
            if len(first) != len(second):
                logger.debug('len: %s != %s', len(first), len(second))
                self._populate_diff(first, second, level, path)
                result &= False
            else:
                for key, first_value in enumerate(first):
                    if not path:
                        key_path = [key]
                    else:
                        key_path = path.copy()
                        key_path.append(key)
                    result &= self.fetch_diff(
                        first_value, second[key], key_path, level
                    )

                    if self.scope is Diff.FIRST and not result:
                        break

        elif isinstance(first, Mapping):
            if len(first.keys()) != len(second.keys()):
                logger.debug('len: %s != %s',
                             len(first.keys()), len(second.keys()))
                self._populate_diff(first, second, level, path)
                result &= False
            else:
                for key, first_value in first.items():
                    if not path:
                        key_path = [key]
                    else:
                        key_path = path.copy()
                        key_path.append(key)

                    second_value = second.get(key)
                    if second_value and first_value != second_value:
                        logger.debug('item(%s): %s != %s',
                                     key, first_value, second_value)
                        if is_iterable_but_not_string(first_value):
                            result &= self.fetch_diff(
                                first_value, second_value, key_path, level
                            )
                        else:
                            self._populate_diff(first_value, second_value,
                                                level, path, key_path=key_path)
                            result &= False

                        if self.scope is Diff.FIRST and not result:
                            break

                    elif is_iterable_but_not_string(first_value):
                        result &= self.fetch_diff(
                            first_value, second_value, key_path, level
                        )

        else:  # invalid types may have been eliminated already
            if first != second:
                self._populate_diff(first, second, level, path)
                result &= False

        return result
