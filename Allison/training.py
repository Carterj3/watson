'''
Created on Oct 20, 2013

@author: crumpaa
'''

""" This takes the training data and determines the parameters used later."""

def determineParameters(trainingData):
    numberOfFalseCases = findNumberOfFalseCases(trainingData);
    ratio = numberOfFalseCases / (float) (len(trainingData) - numberOfFalseCases);
    print "ratio found: ";
    print ratio;
    return calculateColumnParameters(trainingData, ratio);
    
def calculateColumnParameters(trainingData, ratio):
    " The ratio is between the number of false and the number of trues.  That way we can use all of the false training data."
    
    params = [0]*len(trainingData[0]);
    
    height = len(trainingData);
    width = len(trainingData[0]);
    
    "Ignore the 1st 2 spots (question and answer ID) and the last (the answer)"
    for i in range(2, (width-1) ):
        for j in range(height):
            if(trainingData[j][width-1]):
                scale = ratio;
            else:
                scale = -1;
                
            params[i] += scale*trainingData[j][i];
            
    return params;

def findNumberOfFalseCases(data):
    height = len(data);
    width = len(data[0]);
    
    numberOfFalses = 0;
    for i in range(height):
        if (not data[i][width-1]):
            numberOfFalses +=1;
            
    return numberOfFalses;