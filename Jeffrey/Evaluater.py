'''
Created on Oct 20, 2013

@author: Carterj3
'''

if __name__ == '__main__':
    pass
  
  
def jeff_square(x):
  return (x**2)

# takes a row, weights, and func. Evaluates every row and returns their weighted sum
def jeff_eval_row(row,weights,func=jeff_square):
  s = 0
  for i in range(0,len(row)):
    s += weights[i] * func(row[i])
  return s

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
      if j == 85:
        pass
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
        weight_score += k - start
        
  return weight_score
      