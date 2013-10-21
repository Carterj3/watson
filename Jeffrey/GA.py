'''
Created on Oct 20, 2013

@author: Carterj3
'''
weight_file = 'C:\\Users\\Carterj3\\workspace\\ai\\AI-Watson\\jeff_weights'

dataset_file = 'C:\\Users\\Carterj3\\workspace\\ai\\AI-Watson\\tgmctrain.csv'
#dataset_file = 'C:\\Users\\Carterj3\\workspace\\ai\\AI-Watson\\tgmctrain-1q.csv'
def get_dataset():
  # Store weights in the same file
  dataset =  [];
  i = 0
  from time import clock
  t1 = clock()
  with open(dataset_file,'r') as f:
    for line in f:
      temp = []
      for value in line.strip('\n').split(','):
        if not (value in ('true','false')):
          temp.append(float(value))
        else:
          temp.append(value == 'true')
      dataset.append(temp)
      i = i+1
      if (i %1000) == 0:
        print "Dataset",i,clock()-t1
        t1 = clock()
  return dataset

def get_weights():
  # Store weights in the same file
  weights =  None;
  with open(weight_file,'r') as f:
    for line in f:
          weights = line.strip('\n').split(',')
  temp = []
  for each in weights:
    try:
      temp.append(float(each))
    except:
      # I don't store the weights well so it goes like 1,1,1,
      # and that last , screws everybody up
      pass
  return temp
  
def store_weights(weights):
  with open(weight_file,'a') as f:
    for value in weights:
      f.write(str(value))
      f.write(',')
    f.write('\n')
    
def run(count=10,mutate=.10,diviance=.25):
  from random import random,uniform
  from Evaluater import jeff_eval_row,jeff_eval_weight
  from types import BooleanType
  from time import clock
  # Load the weights
  w = get_weights()
  dataset = get_dataset()
  
  # (weights, weights_score)
  all_weights = []
  
  for i in range(0,count):
    wc = []
    
    for l in range(0,len(w)):
      # Copy the weight
      value = float(w[l])
      # Mutate the weight
      if (random() < mutate):
        d = value * diviance
        value = value + uniform(-d,d)
      wc.append(value)
    
    # Run the weight
    weights_score = []
    t1 = clock()
    for j in range(0,len(dataset)):
      if type(dataset[j][len(dataset[j])-1]) is BooleanType:
        row = dataset[j][2:(len(dataset[j])-2)]
      else:
        row = dataset[j][2:]
      if (j % 1000) == 0:
        print "Scoring",j,clock()-t1
        t1 = clock()
      weights_score.append((j+1,jeff_eval_row(row,wc)))
    
    all_weights.append((wc,weights_score))
    wc = None
    
  max_rating,max_weight = 0,[]
  
  # Find best weight
  
  t1 = clock()
  for k in range(0,len(all_weights)):
    each_weight,each_scores = all_weights[k]
    temp_rating, temp_weight = jeff_eval_weight(dataset,each_scores),each_weight
    if temp_rating > max_rating:
      max_rating = temp_rating
      max_weight = temp_weight
    print "Weights",k,clock()-t1
    t1 = clock()
  # Store best weight
  
  store_weights(max_weight)
  print "Storing weight with a value of",max_rating
  
  
if __name__ == '__main__':
  var = "1"
  while var == "1":
    run()
    var = raw_input("Enter 1 to continue: ")
  print "Good bye ..."