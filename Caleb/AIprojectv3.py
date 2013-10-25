
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
        self.ranges = []

    def train(self, value, isTrue):
        if (isTrue):
            if (len(self.ranges) > 0):
                test = False
                toAdd = []
                for v in self.ranges:
                    
                    if (type(v) == type((float()))):
                        if (value < v):
                            test = True
                            self.ranges.remove(v)
                            toAdd.append(v)
                            break
                for v in toAdd:
                    self.ranges.append(v)
                self.ranges.sort()
                if (not test):
                    self.ranges.append(value)
            else:
                self.ranges.append(value)
            self.ranges.sort()
        else:
            for val in self.ranges:
                if (type(val) != type(tuple())):
                    if (value < val):
                        self.ranges.remove(val)
                        self.ranges.append((value,val))
                        self.ranges.sort()
                        break
                else:
                    if (val[0] < value and val[1] > value):
                        #shift all the ranges
                        index = self.ranges.index(val)
                        temp = val[0]
                        for i in range(index-1,-1,-1):
                            temp2 = self.ranges[i]
                            self.ranges.remove(temp2)
                            if (type(temp2) != type(tuple())):
                                self.ranges.insert(i, (temp2, temp))
                                break
                            else:
                                self.ranges.insert(i, (temp2[1], temp))
                                temp = temp2[0]
                        temp = val[1]
                        for i in range(index, len(self.ranges)):
                            temp2= self.ranges[i]
                            self.ranges.remove(temp2)
                            if (type(temp2) != type(tuple())):
                                self.ranges.insert(i, (temp, temp2))
                                break
                            else:
                                self.ranges.insert(i, (temp, temp2[1]))
                                temp = temp2[0]

    def check(self, value):
        for el in self.ranges:
            if (not type(el) == type(tuple())):
                if (el == value):
                    return True
            else:
                if (el[0] <= value and el[1] >= value):
                    return True
        return False


def NeuralNetwork(fileName, fileName2):
    print "Processing List"
    l = returnListOfLists(fileName)
    print "Training Data"
    funcs = []
    for i in range(2, len(l[0]) - 1):
        funcs.append(functor())
    for row in l:
        print row[0]
        isTrue = row[len(row)-1] == "true"
        for i in range(2, len(row)-1):
            funcs[i-2].train(row[i], isTrue)

    #for f in funcs:
    #    f.printRule()
    #return
    #now we run versus test.
    print "Sharpening Axes"
    correctRows = []
    l= returnListOfLists(fileName2)
    for row in l:
        print "Evaluation: " + str(row[0])
        tested = True
        for i in range(2, len(row) -1):
            tested = tested and funcs[i-2].check(row[i])
        if (tested):
            correctRows.append(row[0])

    print correctRows

    if (fileName != fileName2):
        writeFile = "C:/Users/postcn/Documents/aiout.txt"
        f = open(writeFile, 'w')
        for element in correctRows:
            f.write(element[0])
        f.close()
