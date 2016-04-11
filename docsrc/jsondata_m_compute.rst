'jsondata.JSONCompute' - Module
*******************************

.. automodule:: jsondata.JSONCompute


Class: JSONCompute
------------------
.. autoclass:: JSONCompute

Attributes
^^^^^^^^^^

**JSONCompute**:

* JSONCompute.result: Result of operations.

Methods:
^^^^^^^^

__init__
""""""""
	.. automethod:: JSONCompute.__init__

__repr__
""""""""
	.. automethod:: JSONComputePointer.__repr__

__str__
"""""""
	.. automethod:: JSONComputePointer.__str__

Operators:
^^^^^^^^^^

    The syntax displayed for provided operators is::

      S: self
      x: parameter
      n: numerical parameter for shift operators.

    Thus the position of the opreator and parameteres is defined as follows::

      z = S + x: LHS: __add__
      z = x + S: RHS: __radd__
      S += x:    LHS: __iadd__


  
'S+x'
"""""
	.. automethod:: JSONCompute.__add__

'S==x'
""""""
	.. automethod:: JSONCompute.__eq__

'S>=x'
""""""
	.. automethod:: JSONCompute.__ge__

'S>x'
"""""
	.. automethod:: JSONCompute.__gt__

'S+=x'
""""""
	.. automethod:: JSONCompute.__iadd__

'S<x'
"""""
	.. automethod:: JSONCompute.__le__

'S<x'
"""""
	.. automethod:: JSONCompute.__lt__

'S!=x'
""""""
	.. automethod:: JSONCompute.__ne__

'x+S'
"""""
	.. automethod:: JSONCompute.__radd__

Exceptions
----------
* `jsondata.JSONComputeException [source] <_modules/jsondata/JSONCompute.html#JSONComputeException>`_

