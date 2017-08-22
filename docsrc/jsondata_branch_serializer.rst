Serialize branch data by 'jsondata.JSONDataSerializer' 
******************************************************

The module jsondata.JSONDataSerializer extends the JSONData class 
with serialization for JSON documents and substructures.

Provided basic operations are:

* **json_import**:  Import a document or a branch into a document.

* **json_export**:  Export a document or a branch.

Syntax Elements
===============
The current release provides the following operators for the class 'JSONPointer'.

Import/Export Operations::

   ops := json_import | json_export


Examples 
========

Examples for the provided basic calculations are:

Import-Document
---------------

* **Branch Operations - import a JSON document**::

   # persistent file sources
   datafile = os.path.abspath(os.path.dirname(__file__))+os.sep+str('datafile.json')
   schemafile = os.path.abspath(os.path.dirname(__file__))+os.sep+str('schema.jsd')

   #
   # set some control keys for the import, refer to API 
   #
   kwargs = {}
   kwargs['datafile'] = datafile
   kwargs['schemafile'] = schemafile
   kwargs['nodefaultpath'] = True
   kwargs['nosubdata'] = True
   kwargs['pathlist'] = os.path.dirname(__file__)
   kwargs['validator'] = MODE_SCHEMA_DRAFT4

   # load JSON data, with validation by draft4
   configdata = ConfigData(appname,**kwargs)


Import-Branch
-------------
* **Branch Operations - import a JSON branch**::

   # Import another branch into initial main/master data, 
   # and validate it with branch schema.

   # Use insertion point:
   # target = configdata.data['phoneNumber']

   # partial schema for branch, use here a subtree of main schema,
   schema = {
      "$schema": "http://json-schema.org/draft-03/schema",
      'phoneNumber':configdata.schema['properties']['phoneNumber']
   }

   # import settings
   kwargs = {}
   kwargs['schema'] = schema
   kwargs['nodefaultpath'] = True
   kwargs['nosubdata'] = True
   kwargs['pathlist'] = os.path.dirname(__file__)
   kwargs['validator'] = MODE_SCHEMA_DRAFT4

   # target container
   target = configdata.data['phoneNumber']

   # do it...
   datafile = os.path.abspath(os.path.dirname(__file__))+os.sep+str('branch1.json')

   # use '*args' here
   ret = configdata.json_import(target, '-', datafile, None, **kwargs)
   assert ret == True


Export-Document
---------------
* **Branch Operations - export a JSON document**::

    #
    # Export the document.
    #
    datafile = os.path.abspath(os.path.dirname(__file__))+os.sep+str('export-doc.json')
    ret = configdata.json_export(None, datafile)
    assert ret == True


Export-Branch
-------------
* **Branch Operations - export a JSON branch**::


    #
    # Export a branch.
    #
    datafile = os.path.abspath(os.path.dirname(__file__))+os.sep+str('export-doc.json')
    branch = JSONPointer('/phoneNumber/0').get_node(configdata.data)
    ret = configdata.json_export(branch, datafile)
    assert ret == True
