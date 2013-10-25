'''
Created on Oct 21, 2013

@author: crumpaa
'''

def findTheRightAnswers(data, params):
    correctAnswers = [];
    
    for i in range(len(data)):
        score = dotProduct(params, data[i]);
        if (score > 0):
            correctAnswers.append(i);
        
    return correctAnswers;

def dotProduct(params, row):
    answer = 0;
    
    for i in range(len(row)):
        answer += row[i]*params[i];
        
    return answer;