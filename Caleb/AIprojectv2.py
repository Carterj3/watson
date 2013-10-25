
def checkForOneRightAnswer(fileName):
    opened = open(fileName)
    import csv
    fileReader = csv.reader(opened, delimiter=',')
    valueDict = {}
    trueRows = {}
    for row in fileReader:
        val = 0
        try:
            val = 0 if row[len(row) - 1] == 'false' else 1
            valueDict[row[1]] += val
        except(KeyError):
            val = 0 if row[len(row) - 1] == 'false' else 1
            valueDict[row[1]] = val
        if (val == 1):
            try:
                trueRows[row[1]].append(row[0])
            except(KeyError):
                trueRows[row[1]] = [row[0]]
    count = 0
    displayRows = {}
    for element in valueDict:
        if valueDict[element] > 1:
            count += 1
            displayRows[element] = trueRows[element]
            

    if (count == 0):
        print 'There is only one right answer per question'
    else:
        print 'There are questions with more than one right answer, ' + str(count)
        print displayRows

def returnListOfLists(fileName):
    opened = open(fileName)
    import csv
    fileRead = csv.reader(opened, delimiter = ',')
    colRemove = []
    lines = []
    for line in fileRead:
        lines.append(line)
    return lines
    line1 = lines[0]
    line2 = lines[1]
    sames = []
    for i in range(len(line1)):
        if (line1[i] == line2[i] and type(line1[i] != type(str()))): #ignore strings because the only one is the true or false at the end
            sames.append(i)
    for i in sames:
        check = lines[0][i]
        if type(check) == type(str()):
            val = True
        else:
            val = 0
        for j in range(len(lines)):
            if (type(val) == type(bool())):
                val = val and check == lines[j][i];
            else:
                val += lines[j][i]
        if ((val == 0 and check == 0) or (val/len(lines) == check) or (val == True)):
            colRemove.append(i)
    if (len(colRemove) > 0):
        print colRemove
        print "These columns were completely redundant values"



def eq(val1, val2):
    return val1 == val2

def gt(val1, val2):
    return val1 >= val2

def lt(val1, val2):
    return val1 <= val2

def f(val1, val2):
    return false

def t(val1, val2):
    return true

funcArr = {"equals": eq,
            "greaterThan": gt,
            "lessThan": lt,
           "false": f,
           "true": t}
    
class functor():

    def __init__(self):
        self.EQUAL = "equals"
        self.GREATERTHAN = "greaterThan"
        self.LESSTHAN = "lessThan"
        self.FALSE = "false"
        self.TRUE = "true"
        self.function = self.EQUAL
        self.vals = []
        self.isInt = False

    def printRule(self):
        print self.function + " " + self.val

    def train(self, value, isTrue):
        if (isTrue):
            if (value not in self.vals):
                self.vals.append(value)

        

    def check(self, value):
        return value in self.vals
        if (self.satisfied):
            return funcArr[self.function](value, self.val)
        else:
            return funcArr[self.function](value, self.lastFalse)


def NeuralNetwork(fileName, fileName2):
    l = returnListOfLists(fileName)
    funcs = []
    for i in range(2, len(l[0]) - 1):
        funcs.append(functor())
    for row in l:
        isTrue = row[len(row)-1] == "true"
        for i in range(2, len(row)-1):
            funcs[i-2].train(row[i], isTrue)

    #for f in funcs:
    #    f.printRule()
    #return
    #now we run versus test.
    correctRows = []
    l= returnListOfLists(fileName2)
    for row in l:
        tested = True
        for i in range(2, len(row) -1):
            tested = tested and funcs[i-2].check(row[i])
        if (tested):
            correctRows.append(row[0])

    print correctRows

    writeFile = "C:/Users/postcn/Documents/aiout.txt"
    f = open(writeFile, 'w')
    for element in correctRows:
        f.write(element[0])
    f.close()
