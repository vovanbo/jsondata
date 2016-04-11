
jsonproc
########

A command line interface for the processing of in-memory structures of JSON data.

Command line interface for the processing of JSON data by the classes:

  * JSONCompute
  
  * JSONDataSerializer
  
  * JSONPatch
  
  * JSONPointer
  
  * JSONTrees
  
The 'main' module for for the command line usage of 'jsondata' classes.
Provides the apropriate subset of methods for the command line and
scripting usage.

**SYNOPSIS:**::

  jsonproc [--mode=<proc-mode>] [OPTIONS] [<proc-mode-params>]
  
  <proc-mode> := (diff|patch|pointer|validate)
    
  <proc-mode-params>:=(
      <diff-mode-params>
    | <validate-mode-params>
    | <pointer-mode-params>
    | <patch-mode-params>
  )

  <diff-mode-params> := <file0> <file1>

  <pointer-mode-params> := [(pointer|python|pythonkey)] <JSONPointer-operations>

  <patch-mode-params> := not yet implemented, ffs.

  <validate-mode-params> := <file0> [<validate-mode-params>]


  pointer := "Convert result to JSONPointer-string."
  pydata := "Convert result to native Python address."
  <JSONPointer-operations>:=(
      JSONPointer-string
    | JSONPointer-string (operator|keyword) <JSONPointer-operations>
  )
  JSONPointer-string := "A string in accordance to RFC6901"

**OPTIONS:**

  **Processing mode**:
      -mode= (diff|patch|pointer|validate)
          Defines processing mode:
              'diff': Displays the differences of the JSON data
                  for <file0> and <file1>::

                    jsonproc --mode=diff [OPTIONS] <file0> <file1>

              'patch': Not yet implemented, follows soon.
              
              'pointer': Helper mode for command line interaction building
                  JSON pointers, in particular for cut-and-paste ops::
                  
                    jsonproc --mode=pointer [OPTIONS] [format] <pointer> [<pointer-ops> <pointer>]
              
              'validate': Validates JSON data by JSONschema for <file0>::
                  
                    jsonproc --mode=validate --schemafile=<schemafile> [OPTIONS] <file0>
              
         default:= validate

  **Processing parameters**:
      -j, --json= (json|ujson)
          Use as scanner and parser one of the verified packages:
              'json': standard package

              'ujson': ultra-json for performance, check platform availability,
                  and eventually run unit tests.

         default:= json
      -p, --pathlist= <search-path-JSON-data>
         Search path for JSON data file(s), standard list for current platform.

         default:= ../dirname(__file__)/:dirname(__file__)/:/etc/:$HOME/
      -s, --schemafile= <schemafile>
         Schema file - JSONschema.

         default: jsondatacheck.jsd
      --scope= (all|first)
         The scope of match filter for results.

         default:= all
      -V, --validator= <validator>
         Alternate validator provided by module 'jsonschema'

         - default: validate

         - draft3: Draft3Validator

         - off: None

        default:= validate

  **Display options**:
      --indent= #width
         The number of characters for indent.

         default:= 4
      -i --interactive
         Dialog mode, displays formatted for interactive JSON and 
         JSONschema design.
      --linefit= (raw|cut|wrap)
         The handling of lines exceeding width.

         default:= raw
      --linewidth= #width
         The number of characters.

         default:= 80
     
  **Generic**:
      -d --debug
         Debug entries, does NOT work with 'python -O ...'.
         Developer output, aimed for filtering.
      -h --help
         This help.
      -v --verbose
         Verbose, some relevant states for basic analysis.
         When '--selftest' is set, repetition raises the display level.
      -version
         Current version terse.
      -Version
         Current version detailed.
      -selftest
         Performs a basic functional selftest by load, verify, and validate.


**ENVIRONMENT:**
  * PYTHON OPTIONS: -O -OO: Eliminates '__debug__' code.
   
**EXAMPLES:**

  * Default call for diff of equal files::
    
      bin/jsonproc --indent=2 --scope=all --linewidth=80 jsondata/selftest.json jsondata/selftest2.json

    Results in::
    
      n0:selftest.json
      n1:selftest3.json

      diff(n0,n1)=0

  * Default call for diff for different file contents::
    
      bin/jsonproc --mode=diff --indent=2 --scope=all --linewidth=80 jsondata/selftest.json jsondata/selftest3.json

    Results in error condition due to defaults::

      ...
      jsondata.JSONDataExceptions.JSONDataSourceFile: JSONDataSourceFile:open:schemafile:None

    Due to default resolution of schema files, the second input file tried 'selftest3.jsd', which
    is not present. Thus try the following example with assigned schema file.

  * Default call for diff for different file contents::
    
      bin/jsonproc --mode=diff --indent=2 --scope=all --linewidth=80 -s jsondata/selftest.jsd jsondata/selftest.json jsondata/selftest3.json

    Results in::
    
      n0:selftest.json
      n1:selftest3.json
      path=[u'testcase', u'description', 0]
        n0[u'testcase', u'description', 0] = A first test base
        n1[u'testcase', u'description', 0] = diff0
      path=[u'customers', u'domestic', 0, u'products']
        n0[u'customers', u'domestic', 0, u'products'] = [{u'priority': 0, u'quantities
          ': 2000, u'name': u'product0', u'quota': 1.5}, {u'priority': 1, u'quantities': 2
          001, u'name': u'product1', u'quota': 2.5}]
        n1[u'customers', u'domestic', 0, u'products'] = [{u'priority': 0, u'quantities
          ': 2000, u'name': u'product0', u'quota': 1.5}]
      path=[u'phoneNumber']
        n0[u'phoneNumber'] = [{u'type': u'home0', u'number': u'000'}, {u'type': u'home
          1', u'number': u'111'}, {u'type': u'office', u'number': u'222'}, {u'type': u'hol
          idays', u'number': u'333'}]
        n1[u'phoneNumber'] = [{u'type': u'home0', u'number': u'000'}, {u'type': u'home
          1', u'number': u'111'}, {u'type': u'office', u'number': u'222'}]

      diff(n0,n1)=1

  * Call for validate - as default mode::
    
      bin/jsonproc jsondata/selftest.json

    Results in::

      data:   selftest.json
      schema: selftest.jsd
      validate(data,schema)=0

  * Call for validate - as default mode with quiet option '-q'::
    
      bin/jsonproc -q jsondata/selftest.json

    Results in::

      "silent, with exit code only, thus display with: echo $? => '0')"

  * Call for validate::
    
      bin/jsonproc --mode=validate -s jsondata/selftest.jsd jsondata/selftest3.json

    Results in::

      data:   selftest3.json
      schema: selftest.jsd
      validate(data,schema)=0

  * Call for pointer operations::
    
    Convert
      Call::

        bin/jsonproc --mode=pointer-ops '[phoneNumber][0]'

      Results in::

        /phoneNumber/0

    Convert
      Call::

        bin/jsonproc --mode=pointer-ops python '/phoneNumber/0'

      Results in::

         [phoneNumber][0]

    Add
      Call::

        bin/jsonproc --mode=pointer-ops '/phoneNumber/0' + '/type' 

      Results in::

        '/phoneNumber/0/type' 

    Add and convert
      Call::

        bin/jsonproc --mode=pointer-ops pythonkey '/phoneNumber/0' + '/type' 

      Results in::

        '/phoneNumber/0/type' 

    
