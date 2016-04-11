Compute Language Examples 
*************************

Add and convert::

    a + b + c
    
Compare::
    
    a + b + c > d 
    a + b + c > d + e
    
    
The following are the same pointer-only operations::

    ( a + b + c ) > d
    ( a + b + c ) > ( d + e )
    ( a + ( b + c ) ) > ( d + e )
    
    
The following equivalent operation are NOT the same as the 
previous, because they operate on the JSON data by evaluation
of the pointed value::
                
    eval( a + b + c ) > ( d + e )
    ( eval( a + b ) + eval( c ) > eval( d + e )
    

The following changes the data for evaluation::
      
    A=datafile(filename0) B=datafile(filename1) \\
      ( eval( a + b ) + eval( c ) > data(A) eval( d + ( data(B) e )
       

For additional examples refer to documentation of the 'jsonproc' utility.
    
