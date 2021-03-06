inputfilename  = 'Iris0000.csv'                  #filename input data
outputfilename = inputfilename + '.erg'       #filename output data
inputseparator = ';'                          #separator for csv columns
labelcolumn    = 4                            #column of label
columnfilter   = [0,1,2,3]                    #columns with features
columnflen     = len(columnfilter)            #count of features in data
featurecols    = [0,1,2,3]                    #selected Features
linefilter     = '[70, 72, 83, 106, 119, 133, 134]'                         #linefilter: lines to ignore
firstrelpred   = 10                           #count of first neighbours in outputlist
rpdigits       = 4                            #relative prediction: number of digits after decimal point
dnnrange       = [0,1,2,3,4]                  #show different nearest neighbour range
printseparator = '*'*80+'\n'
columnname = ["sepal_length", "sepal_width", "petal_length", "petal_width", "species"]