'''
Created on Oct 20, 2013

@author: Carterj3
'''

train = True

weight_file = 'C:\\Users\\Carterj3\\workspace\\ai\\AI-Watson\\jeff_weights'

eval_file = 'C:\\Users\\Carterj3\\workspace\\ai\\AI-Watson\\tgmcevaluation.csv'

#dataset_file = 'C:\\Users\\Carterj3\\workspace\\ai\\AI-Watson\\tgmctrain.csv'
dataset_file = 'C:\\Users\\Carterj3\\workspace\\ai\\AI-Watson\\tgmc_200.csv'
#dataset_file = 'C:\\Users\\Carterj3\\workspace\\ai\\AI-Watson\\tgmctrain-1q.csv'
#dataset_file = 'C:\\Users\\Carterj3\\workspace\\ai\\AI-Watson\\tgmctrain-2q.csv'

from multiprocessing import Queue
from threading import Thread
from random import random,uniform
from Evaluater import jeff_eval_row,jeff_eval_weight,jeff_create_question_array,jeff_eval_qid
from types import BooleanType
from time import clock

def get_dataset(d_file=dataset_file):
  # Store weights in the same file
  dataset =  [];
  i = 0
  from time import clock
  t1 = clock()
  with open(d_file,'r') as f:
    for line in f:
      temp = []
      for tValue in line.strip('\n').split(','):
        value = tValue.strip()
        if not (value in ('true','false','True','False')):
          temp.append(float(value))
        else:
          temp.append((value == 'true' or value == 'True'))

      dataset.append(temp)
      i = i+1
      if (i %1000) == 0:
        print "Dataset",i,clock()-t1
        t1 = clock()
  return dataset

def get_weights(fil=weight_file):
  # Store weights in the same file
  weights =  None;
  score = 0
  with open(fil,'r') as f:
    for line in f:
      temp = line.split(":")
      score = float(temp[0])
      temp_line = temp[1]
      weights = temp_line.strip('\n').split(',')
  temp = []
  for each in weights:
    try:
      temp.append(float(each))
    except:
      # I don't store the weights well so it goes like 1,1,1,
      # and that last , screws everybody up
      pass
  return score,temp
  
def store_weights(weights,rating,fil=weight_file):
  from cStringIO import StringIO
  tempstring = StringIO()
  tempstring.write(str(rating)+":")
  
  for l in range(0,len(weights)-1):
    value = str(weights[l])
    tempstring.write(value+",")
  tempstring.write(str(weights[len(weights)-1])+"\n")
  
  with open(fil,'a') as f:
    f.write(tempstring.getvalue())


def store_answers(answers):
  from cStringIO import StringIO
  tempstring = StringIO()
  
  for l in range(0,len(answers)-1):
    value = str(answers[l])
    tempstring.write(value+"\n")
  tempstring.write(str(answers[len(answers)-1]))
  
  with open("answers.txt",'w') as f:
    temp = tempstring.getvalue()
    f.write(temp)



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

def Train_run(dataset,tFile,count=100,mutate=.10,diviance=.30):
  t1 = clock()
  # Load the weights
  score,w = get_weights(tFile)
  
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
    threads = []
    for j in range(0,len(dataset)):
      T = Thread(target=runHelper_jeff_eval_row,args=(dataset, j, wc, temp_weights_score,clock()))
      T.start()
      threads.append(T)
      start_times.append(clock())
      
    for j in range(0,len(dataset)):
      threads[j].join()
      end_times.append(clock())
      total_time = total_time + end_times[j] - start_times[j]
      
    print "S_Threads took ", total_time / len(dataset)," seconds (AVG)",i
    print "S_Threads took ", total_time, " seconds (Total)",i
    
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
  threads = []
  
  #
  for k in range(0,len(all_weights)):
    each_weight, each_score = all_weights[k]
    T = Thread(target=runHelper_jeff_eval_weight,args=(each_weight, each_score, dataset, weight_queue))
    T.start()
    threads.append(T)
    start_times.append(clock())
      
  for k in range(0,len(all_weights)):
    threads[k].join()
    end_times.append(clock())
    total_time =  total_time + end_times[k] - start_times[k]

  print "W_Threads took ", total_time / len(dataset)," seconds (AVG)"
  print "W_Threads took ", total_time, " seconds (Total)" 
  #
  max_rating, max_weight = -1,[]
  while not weight_queue.empty():
    temp_rating,temp_weight = weight_queue.get()
    if temp_rating > max_rating:
      max_rating = temp_rating
      max_weight = temp_weight
    
      
  
  # Store best weight fi it was better than the old one
  if score < max_rating:
    store_weights(max_weight,max_rating,tFile)
  print "Storing weight with a value of",max_rating,"took",clock()-t1,"seconds"
  
def Eval_run():
  t1 = clock()
  # Load the weights
  score,w = get_weights()
  
  eval = get_dataset(eval_file)
  
  eval_qids = jeff_create_question_array(eval)
  
  answers = []
  t1 = clock()
  for i in range(0,len(eval_qids)):
    qid = eval_qids[i]
    temp = jeff_eval_qid(qid,w)
    sorted_temp = sorted(temp,key=lambda x: x[1])
    answers.append(sorted_temp[len(sorted_temp)-1][0])
    if (i % 1) == 0:
      print "qids",i+1,"/",len(eval_qids),"|",clock()-t1,"seconds"
      t1 = clock()
    
  store_answers(answers)
  
    
if __name__ == '__main__':
  import sys
  args = sys.argv
  
  if len(args) < 2:
    tFile = weight_file
  else:
    tFile = args[1]
  
  if train:
    data = get_dataset()
    while True:
      Train_run(data,tFile)
  else:
    #Eval_run()
    from Evaluater import jeff_save_n_qid
    data = get_dataset()
    jeff_save_n_qid(data,300)