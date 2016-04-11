'jsondata' Compute Language
***************************

The module jsondata.JSONCompute supports a basic language 
for computing of JSON based data structures.
This provides in particular for pointer artithmetics in order to provide
loop constructs of compound pointers, evaluate pointed values within
JSON documents, and the calculation of values.

Examples for the provided basic calculations are:

* **Pointer Arithmetics**:  manipulates and calculates the pointer itself::

     import jsondata.JSONPointer

     a = JSONPointer("/a/b/c")
     b = JSONPointer("/x/y")
     c = JSONPointer("/a/b/c/2/x/y/v")

     for i in range(0,4):
        print a + i + b > c

  prints the results::

     False 
     False 
     True 
     False 

* **Pointed Value Evaluation**: fetches values from JSON documents::

     import jsondata.JSONPointer
     import jsondata.JSONDataSerializer

     jsonfile = "data.json"

     a = JSONPointer("/a/b/c")
     b = JSONPointer("/x/y")
     c = JSONPointer("/2/x/y/v")

     D = JSONDataSerializer("app0", jsonfile)

     print eval( a ) + b 
     print c
     print eval( a ) + b > c

  where the file "data.json" contains the data::
     {
        a: {
          b: {
            c: 2
          }
        }
     }

  prints the results::

     /2/x/y
     /2/x/y/v
     True 

* **Calculations with Pointed Values**: applies common arithmetics on to evaluated 
  values and numeric parts of pointers::

     import jsondata.JSONPointer
     import jsondata.

     a = JSONPointer("/a/b/c")
     c = 3
     D = JSONDataSerializer("app0", "data.json")

     print "c="+str(c)
     for i in range(0,4):
        print a + i + " - " + a + i > c

  prints the results::

     c=3
     2 - False 
     3 - False 
     4 - True 
     5 - False 

Syntax Elements
===============
The current release provides a simplified pre-version of the syntax 
based on tokens of the lexial analysis output.
The scanner and parser frontend will be available soon.

Conversion of JSON pointers::

   input: (RFC6901,Python)
             
   output (RFC6901,Python,PythonNodeKey,JSONPointer)


Pointer comparison::

   ops := '>' | '<' | '>=' | '<=' | '==' | '!='


Pointer calculation, assignment and group operations::

   ops := '=' | '(' | ')'


Miscellaneous operators::

   ops := '"' | '\'


Pointed-Value operations::
        
   as provided by Python


Keywords::

   'copy' | 'del' | 'eval' 
   | 'data' | 'datafile' | 'schema' | 'schemafile'

   'if' | 'else'


**REMARK**: The syntax as a pre-release is going to be extended forward compatible.
    
