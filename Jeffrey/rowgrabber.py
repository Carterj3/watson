'''
Created on Nov 4, 2013

@author: Carterj3
'''

def get_dataset(d_file):
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

def get_answers(a_file):
  # Store weights in the same file
  answers =  [];
  i = 0
  from time import clock
  t1 = clock()
  with open(a_file,'r') as f:
    for line in f:
      temp = float(line.strip('\n'))
      
      answers.append(temp)
      i = i+1
      if (i %1000) == 0:
        print "Answers",i,clock()-t1
        t1 = clock()
  
  return answers

def create_dataset(o_file):
  from cStringIO import StringIO
  tempstring = StringIO()
  
  for row in o_file:
    value = str(int(row[0]))
    tempstring.write(value+",")
    for i in range(1,len(row)-1):
      value = str(row[i])
      tempstring.write(value+",")
    tempstring.write(str(row[len(row)-1])+"\n")
  
  with open("output.txt",'w') as f:
    f.write(tempstring.getvalue())
    
if __name__ == '__main__':
  import sys
  args = sys.argv
  
  if len(args) < 3:
    print "Not enough arguments passed. Need both answer file and data file given:",args
    exit(1)
  
  aFile = args[1]
  dFile = args[2]
  #Given answer file and dataset file
  answers = get_answers(aFile)
  dataset = get_dataset(dFile)
  
  output = []
  
  for eachRow in dataset:
    rowid = eachRow[0]
    if rowid in answers:
      output.append(eachRow)
      
  #Produce a file containing only those rows
  create_dataset(output)
  pass