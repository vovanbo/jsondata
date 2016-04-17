Operations by 'jsondata.JSONPointer' 
************************************

The module jsondata.JSONPointer provides for the most important operators for
the assembly and evaluation of JSON pointers in accordance to RFC6901.

Basic types of provided basic operations are:

* **Pointer Arithmetics**:  Manipulates and calculates the pointer itself.
  Thus the comparison is related to the resulting contained set.
  Where the shorter matching pointer path contains more elements, than 
  the longer, which itself is contained in the matching shorter path. 

* **Pointed Value Evaluation**: Fetches values from JSON documents.
  Thus the comparison is related to the resulting values pointed 
  to by the pointer path.

* **Calculations with Pointed Values**: Applies common arithmetics on to evaluated 
  values and numeric parts of pointers.

Syntax Elements
===============
The current release provides the following operators for the class 'JSONPointer'.

Pointer comparison::

   ops := '>' | '<' | '>=' | '<=' | '==' | '!='


Pointer calculation and assignment operations::

   ops := '=' | '+' | '+='


Pointed value evaluation operators::

   ops := '()'


Examples 
========

Examples for the provided basic calculations are:

Arithmetics
-----------

* **Pointer Arithmetics**::

     import jsondata.JSONPointer

     a = JSONPointer("/a/b/c")
     b = JSONPointer("/x/y")
     c = JSONPointer("/a/b/c/2/x/y/v")
     d = JSONPointer("/a/b/c/2/x/y")
     e = JSONPointer("/a/b/c/2/x")

     # loop with increment
     for i in range(0,4):
        print str(a + i + b) + " > " + str(c) + " = " + str(a + i + b > c )

     print
     print str(a + 2 + b) + " > " + str(d) + " = " + str(a + 2 + b > d )

     print
     print str(a + 2 + b) + " > " + str(e) + " = " + str(a + 2 + b > e )

  prints the results::

     /a/b/c/0/x/y > /a/b/c/2/x/y/v = False
     /a/b/c/1/x/y > /a/b/c/2/x/y/v = False
     /a/b/c/2/x/y > /a/b/c/2/x/y/v = True
     /a/b/c/3/x/y > /a/b/c/2/x/y/v = False

     /a/b/c/2/x/y > /a/b/c/2/x/y = False

     /a/b/c/2/x/y > /a/b/c/2/x = False

  Where the shorter matching pointer path contains more elements, than 
  the longer, which itself is contained in the matching shorter path. 

Evaluation
----------

* **Pointed Value Evaluation**::

     import jsondata.JSONPointer

     jdata = { 'a': { 'b': { 'c': 2, 'd': 3 } } }

     a = JSONPointer("/a/b/c")
     b = JSONPointer("/x/y")
     c = JSONPointer("/2/x/y/v")
     d = JSONPointer("/a/b/d")

     print a(jdata) + b 
     print JSONPointer(a(jdata)) + d(jdata)
     print JSONPointer(a(jdata)) + JSONPointer(d(jdata))
     print c
     print a(jdata) + b > c

  prints the results::

     /2/x/y
     /2/3
     /2/3
     /2/x/y/v
     True 

Calculation
-----------

* **Calculations with Pointed Values**::

     import jsondata.JSONPointer

     jdata = { 'a': { 'b': { 'c': 2, 'd': 3 } } }

     a = JSONPointer("/a/b/c")
     b = JSONPointer("/x/y")
     c = JSONPointer("/2/x/y/v")
     d = JSONPointer("/a/b/d")

     print a(jdata) + d(jdata)
     print JSONPointer(a(jdata) + d(jdata))

  prints the results::

     5
     /5

