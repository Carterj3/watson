'''
Created on Oct 20, 2013

@author: Carterj3
'''
weight_file = 'C:\\Users\\Carterj3\\workspace\\ai\\AI-Watson\\jeff_weights'
# 239944
dataset_file = 'C:\\Users\\Carterj3\\workspace\\ai\\AI-Watson\\tgmctrain.csv'
#dataset_file = 'C:\\Users\\Carterj3\\workspace\\ai\\AI-Watson\\tgmctrain-1q.csv'

from multiprocessing  import Process, Queue, Array
from random import random,uniform
from Evaluater import jeff_eval_row,jeff_eval_weight
from types import BooleanType
from time import clock

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
      temp_line = line.split(":")[1]
      weights = temp_line.strip('\n').split(',')
  temp = []
  for each in weights:
    try:
      temp.append(float(each))
    except:
      # I don't store the weights well so it goes like 1,1,1,
      # and that last , screws everybody up
      pass
  return temp
  
def store_weights(weights,rating):
  from cStringIO import StringIO
  tempstring = StringIO()
  tempstring.write(str(rating)+":")
  
  for l in range(0,len(weights)-1):
    value = str(weights[l])
    tempstring.write(value+",")
  tempstring.write(str(weights[len(weights)-1])+"\n")
  
  with open(weight_file,'a') as f:
    f.write(tempstring.getvalue())

def runHelper_jeff_eval_row(dataset,rowIndex,weights,queue,t1):
  if type(dataset[rowIndex][len(dataset[rowIndex])-1]) is BooleanType:
      row = dataset[rowIndex][2:(len(dataset[rowIndex])-2)]
  else:
    row = dataset[rowIndex][2:]
 
  # Cannot return, store data in given queue
  ls = []
  ls.append(rowIndex+1)
  ls.append(jeff_eval_row(row,weights))
  queue.put(ls)

def runHelper_jeff_eval_weight(each_weight,each_score,dataset,weight_queue):
    temp_rating, temp_weight = jeff_eval_weight(dataset,each_score),each_weight
    
    ls = []
    ls.append(temp_rating)
    ls.append(temp_weight)
    weight_queue.put(ls)

def run(dataset,count=2,mutate=.10,diviance=.25,):
  
  # Load the weights
  w = get_weights()
  
  # (weights, weights_score)
  temp_all_weights = Queue()
  
  for i in range(0,count):
    wc = []
    
    for l in range(0,len(w)):
      # Copy the weight
      value = float(w[l])
      # Mutate the weight
      if (random() < mutate):
        d = value * diviance
        if d == 0:
          d = 1
        value = value + uniform(-d,d)
      wc.append(value)
    
    # Run the weight
    temp_weights_score = Queue()
    start_times = []
    end_times = []
    total_time = 0
    proccesses = []
    for j in range(0,len(dataset)):
      P = Process(target=runHelper_jeff_eval_row,args=(dataset, j, wc, temp_weights_score,clock()))
      start_times.append(clock())
      P.start()
      proccesses.append(P)
      
    for j in range(0,len(dataset)):
      proccesses[j].join()
      end_times.append(clock())
      total_time = total_time + end_times[j] - start_times[j]
      
    print "S_Threads took ", total_time / len(dataset)," seconds (AVG)"
    print "S_Threads took ", total_time, " seconds (Total)"
    
    weights_score = []
    while not temp_weights_score.empty():
      weights_score.append(temp_weights_score.get())
    temp_all_weights.put((wc,weights_score))
    wc = None
        
  # Find best weight
  all_weights = []
  while not temp_all_weights.empty():
    all_weights.append(temp_all_weights.get())

  weight_queue = Queue()
  start_times = []
  end_times = []
  total_time = 0
  proccesses = []
  
  #
  for k in range(0,len(all_weights)):
    print "W_Threads starting ",k,
    each_weight, each_score = all_weights[k]
    P = Process(target=runHelper_jeff_eval_weight,args=(each_weight, each_score, dataset, weight_queue))
    P.start()
    print " started"
    proccesses.append(P)
    start_times.append(clock())
      
  for k in range(0,len(all_weights)):
    proccesses[k].join()
    end_times.append(clock())
    total_time = total_time + end_times[k] - start_times[k]

  print "W_Threads took ", total_time / len(dataset)," seconds (AVG)"
  print "W_Threads took ", total_time, " seconds (Total)" 
  #
  max_rating, max_weight = 0,[]
  while not weight_queue.empty():
    temp_rating,temp_weight = weight_queue.get()
    if temp_rating > max_rating:
      max_rating = temp_rating
      max_weight = temp_weight
    
  # Store best weight
  
  store_weights(max_weight,max_rating)
  print "Storing weight with a value of",max_rating
  
  
if __name__ == '__main__':
  data = get_dataset()
  while True:
    t1 = clock()
    run(data)
    print "Cycle took ",clock()-t1," seconds to complete"
    break