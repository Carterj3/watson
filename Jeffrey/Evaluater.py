'''
Created on Oct 20, 2013

@author: Carterj3
'''
from time import clock

if __name__ == '__main__':
    pass

def jeff_cube(x):
  return (x**3)
  
def jeff_square(x):
  return (x**2)

# takes a row, weights, and func. Evaluates every row and returns their weighted sum
def jeff_eval_row(row,weights,func=jeff_cube):
  s = 0
  for i in range(0,len(row)):
    s += weights[i] * func(row[i])
  return s

def jeff_eval_qid(qid,weights,func=jeff_square):
  temp = []
  for i in range(0,len(qid)):
    row = qid[i]
    temp.append((row[0],jeff_eval_row(row[2:],weights,func)))
  return temp

def jeff_is_answer_row(row):
  return (row[len(row)-1])

'''
dataset is a list of lists containing all the data for rows

weights_score is a list of tuples [1indexed row , value for row]
'''
def jeff_eval_weight(dataset,weights_score):
  weight_score = 0
  # Row 2 is the QID
  i = 0
  while i < len(dataset):
    start = i
    # Get the length of the question
    j = i
    question_size = 0
    while j < len(dataset) and dataset[j][1] == dataset[start][1]:
      j = j + 1
    answers = []
    while i < j:
      question_size = question_size + 1
      if dataset[i][len(dataset[i])-1]:
        answers.append(dataset[i][0])
      i = i + 1
    # This block is a QID
    sorted_weights = sorted(weights_score,key=lambda x: x[1])
    
    for k in range(0,len(sorted_weights)):
      row_id,score = sorted_weights[k]
      if row_id in answers:
        weight_score += (k - start) ** 3
        
  return weight_score

def jeff_create_question_array(dataset):
  i = 0
  j = 0
  master_qids = []
  while i < len(dataset):
    t1 = clock()
    start = i
    qids = []
    while i < len(dataset) and dataset[i][1]== dataset[start][1]:
      qids.append(dataset[i])
      i = i +1
    master_qids.append(qids)
    print "Create_QIDs",i,"/",len(dataset),"|",clock()-t1
    t1 = clock()
    
  return master_qids


def jeff_save_n_qid(dataset,n,m=0):
  qids = jeff_create_question_array(dataset)
  
  from cStringIO import StringIO
  tempstring = StringIO()
  
  i = m
  while i < n and i <len(qids):
    t1 = clock()
    q = qids[i]
    for row in q:
      for l in range(0,len(row)-1):
        value = str(row[l])
        tempstring.write(value+",")
      tempstring.write(str(row[len(row)-1])+"\n")
    #qids[i] = []
    print "Save-QIDS",i,"|",clock()-t1
    t1 = clock()
    i = i +1
    
  with open("tgmc_"+str(n)+".csv",'w') as f:
    f.write(tempstring.getvalue())
    
    
      