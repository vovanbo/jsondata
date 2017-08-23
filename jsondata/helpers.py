import collections
import inspect


def is_generator(obj):
    """Return True if ``obj`` is a generator
    """
    return inspect.isgeneratorfunction(obj) or inspect.isgenerator(obj)


def is_iterable_but_not_string(obj):
    """Return True if ``obj`` is an iterable object that isn't a string."""
    return (
        (isinstance(obj, collections.Iterable) and not hasattr(obj, "strip"))
        or is_generator(obj)
    )


def is_collection(obj):
    """
    Return True if ``obj`` is a collection type,
    e.g list, tuple, queryset.
    """
    return (
        is_iterable_but_not_string(obj) and
        not isinstance(obj, collections.Mapping)
    )


def ensure_text_type(val):
    if isinstance(val, bytes):
        val = val.decode('utf-8')
    return str(val)


def if_none(value, default):
    return value if value is not None else default


def first(iterable, default=None, key=None):
    """Return first element of *iterable* that evaluates to ``True``, else
    return ``None`` or optional *default*. Similar to :func:`one`.

    >>> first([0, False, None, [], (), 42])
    42
    >>> first([0, False, None, [], ()]) is None
    True
    >>> first([0, False, None, [], ()], default='ohai')
    'ohai'
    >>> import re
    >>> m = first(re.match(regex, 'abc') for regex in ['b.*', 'a(.*)'])
    >>> m.group(1)
    'bc'

    The optional *key* argument specifies a one-argument predicate function
    like that used for *filter()*.  The *key* argument, if supplied, should be
    in keyword form. For example, finding the first even number in an iterable:

    >>> first([1, 1, 3, 4, 5], key=lambda x: x % 2 == 0)
    4

    Contributed by Hynek Schlawack, author of
    `the original standalone module`_.

    .. _the original standalone module: https://github.com/hynek/first
    """
    return next(filter(key, iterable), default)
