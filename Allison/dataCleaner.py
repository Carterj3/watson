'''
Created on Oct 20, 2013

@author: crumpaa
'''

""" Takes in a matrix of all the data and returns a simplified version.  Duplicate columns are removed.  Duplicate rows are removed.  Columns consisting of a single value are removed. """

def removeDuplicateColumns(data):
    data = transpose(data);
    cleanerData = removeDuplicateRows(data);
    cleanerData = transpose(cleanerData);
    
    return cleanerData;
 
def removeSingleValueColumns(originalData):
    """ Returns a matrix where none of the columns have only 1 value."""
    
    toBeRemoved = findSingleValueColumns(originalData);
    cleanerData = [];
    
    toBeRemoved.append(-1);
    
    for i in range(0, len(originalData)):
        counter = 0;
        row = [];
        for j in range(0, len(originalData[0])):
            if (j == toBeRemoved[counter]):
                counter += 1;
            else:
                row.append(originalData[i][j]);
        cleanerData.append(row);
                
    return cleanerData;

def findSingleValueColumns(originalData):
    """ Finds the columns that have only 1 value."""
    uselessColumns = [];

    for i in range(0, len(originalData[0])):
        isUsefulColumn = False;
        firstEntry = originalData[0][i];
        for j in range(1, len(originalData)):
            if (firstEntry != originalData[j][i]):
                isUsefulColumn = True;
                break;

        if (not isUsefulColumn):
            uselessColumns.append(i);
            
    return uselessColumns;

def removeDuplicateRows(originalData):
    """ Returns a matrix where none of the rows match any of the other rows.  The 1st occuring row will be the one that is removed."""
    
    cleanerData = [];
    
    for i in range(0, len(originalData)-1):
        isUsefulRow = True;
        for j in range(i+1, len(originalData)):
            if (compareEntries(originalData[i], originalData[j])):
                isUsefulRow = False;
                break;
                    
        if isUsefulRow:
            cleanerData.append(originalData[i]);
    cleanerData.append(originalData[i+1]);
    
    return cleanerData;

def compareEntries(arrayOne, arrayTwo):
    """ Expects 2 arrays of the same length.  Returns true iff they are the same."""
    for i in range(0, len(arrayOne)):
        if (arrayOne[i] != arrayTwo[i]):
            return False;
        
    return True;

def transpose(data):
    transposedData = [ [0] * len(data) for i in range(len(data[0]))]

    for i in range(0, len(data)):
        for j in range(0, len(data[0])):
            transposedData[j][i] = data[i][j];
    
    return transposedData;

    