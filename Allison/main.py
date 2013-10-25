'''
Created on Oct 20, 2013

@author: crumpaa
'''

""" Reads in my textData file and creates a matrix.  Calls my data cleaner code and prints the output."""

import dataCleaner;
import training;
import perceptrons;
import csv;

def main():
    trainingData = loadData("smallTrain.csv");
    #data = loadData("smallEvaluation.csv");
    print "loaded";
    trainingData = normalizeData(trainingData);
    print "normalized";
    params = training.determineParameters(trainingData);
    print "params: ";
    print params;
    print;
    
    #data = normalizeData(data);
    answers = perceptrons.findTheRightAnswers(trainingData, params);
    print "answers: ";
    print answers;
    print;
    
def loadData(fileName):
    data = [];
    with open(fileName, 'rb') as f:
        reader = csv.reader(f)
        for row in reader:
            dataRow = [];
            for char in row:
                if char != "FALSE" and char != "false" and char != "TRUE" and char != "true" :
                    dataRow.append(float(char));
                else:
                    if char == "FALSE":
                        dataRow.append(0);
                    else:
                        dataRow.append(1);
                
            data.append(dataRow);
    
    return data;
    
def loadText():
    file = open('textData','r');
    line = file.readline();
    data = [];
    while (line != ''):
        row = [];
        for char in line:
            if char != ' ' and char!= '\n':
                row.append(int(char));
        data.append(row);
        line = file.readline();
    
    file.close();
    return data;

def normalizeData(data): 
    for i in range(len(data[0])):
        sum = 0;
        for j in range(len(data)):
            sum += data[j][i];
            
        if sum != 0:    
            for j in range(len(data)):
                data[j][i]  = data[j][i] / float(sum);
                
    return data;
  
if __name__ == '__main__':
    main()