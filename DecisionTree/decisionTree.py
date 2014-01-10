import sys, math, re
import cPickle as pickle
import readARFF
import copy
import random
# import readARFF2

### takes as input a list of class labels. Returns a float
### indicating the entropy in this data.
###Entropy is, of course, about proportions of positive
###versus negative examples
def entropy(data) :
    vals = [float(data.count(c))/len(data) for c in set(data)]
    entropy = 0
    for i in vals:
        entropy += i * (math.log(i)/math.log(2))
    return -entropy

### Compute remainder - this is the amount of entropy left in the data after
### we split on a particular attribute. Let's assume the input data is of
### the form:
###    [(value1, class1), (value2, class2), ..., (valuen, classn)]
def remainder(data) :
    possibleValues = set([item[0] for item in data])
    r = 0.0
    vl = [item[0] for item in data]
    totalE = entropy([item[1] for item in data])
    for value in possibleValues :
        c = vl.count(value)
        r += entropy([item[1] for item in data if item[0] == value]) * (float(c) / len(data) )
    r = totalE - r
    return r


### selectAttribute: choose the index of the attribute in the current
### dataset that minimizes the remainder.
### data is in the form [[a1, a2, ..., c1], [b1,b2,...,c2], ... ]
### where the a's are attribute values and the c's are classifications.
### and attributes is a list [a1,a2,...,an] of corresponding attribute values
def selectAttribute(data, attributes) :
    maxV = -1
    maxIndex = -1
    for i in attributes.keys():
        listA = [(v[i],v[-1]) for v in data]
        r = remainder(listA)
        if r > maxV:
            maxV = r
            maxIndex = i
    return maxIndex


### a TreeNode is an object that has either:
### 1. An attribute to be tested and a set of children; one for each possible
### value of the attribute.
### 2. A value (if it is a leaf in a tree)
class TreeNode :
    def __init__(self, attribute, value) :
        self.attribute = attribute
        self.value = value
        self.children = {}

    def __repr__(self) :
        if self.attribute :
            return self.attribute
        else :
            return self.value

    ### a node with no children is a leaf
    def isLeaf(self) :
        return self.children == {}

    ### return the value for the given data
    ### the input will be:
    ### data - an object to classify - [v1, v2, ..., vn]
    ### attributes - the attribute dictionary
    def classify(self, data, attributes) :
        if self.attribute:
            v = data[attributes.index(self.attribute)]
            if v not in self.children.keys():
                return self.value

            result = self.children[v]
            if result.attribute:
                return result.classify(data,attributes)
            else:
                return result.value
        else:
            return self.value


    def printTree(self):
        print "+++"
        print self.attribute," ",self.value
        print "has children: ===="
        for c in self.children:
            print c,":",self.children[c]
        print "\n"

        for c in self.children:
            if self.children[c].attribute:
                self.children[c].printTree()



### a tree is simply a data structure composed of nodes (of type TreeNode).
### The root of the tree
### is itself a node, so we don't need a separate 'Tree' class. We
### just need a function that takes in a dataset and our attribute dictionary,
### builds a tree, and returns the root node.
### makeTree is a recursive function. Our base case is that our
### dataset has entropy 0 - no further tests have to be made. There
### are two other degenerate base cases: when there is no more data to
### use, and when we have no data for a particular value. In this case
### we use either default value or majority value.
### The recursive step is to select the attribute that most increases
### the gain and split on that.


### assume: input looks like this:
### dataset: [[v1, v2, ..., vn, c1], [v1,v2, ..., c2] ... ]
### attributes: [a1,a2,...,an] }
def makeTree(dataset, attributes, defaultValue) :
    # you write; See assignment & notes for description of algorithm

    if len(dataset) == 0:
        return TreeNode(None,defaultValue)
    #calculate entropy for whole dataset
    entropyD = entropy([item[-1] for item in dataset])

    if entropyD == 0:
        return TreeNode(None,dataset[0][-1])
    if len(attributes) == 0:
        return TreeNode(None, readARFF.computeZeroR(attributes, dataset))


    copyAttr = copy.copy(attributes)
    dV = readARFF.computeZeroR(attributes,dataset)

    attrSpread = selectAttribute(dataset,attributes) # index
    vlist = attributes[attrSpread].values()[0]

    del copyAttr[attrSpread]
    node = TreeNode(attributes[attrSpread].keys()[0],None)

    for v in vlist:
        ## for each value of that removed attribute
        ## get tuples for a specific value of that removed attribute
        subDataset = [item for item in dataset if item[attrSpread] == v]

        if len(subDataset) == 0:
            node.children[v] = TreeNode(None, readARFF.computeZeroR(attributes,dV))

        node.children[v] = makeTree(subDataset,copyAttr,dV)

    return node
def computePrecision(TP,FP,TN,FN):
    if float(TP + FP) == 0:
        return "----"
    return round(float(TP)/(TP + FP),3)

def computeRecall(TP,FP,TN,FN):
    if float(TP + FN) == 0:
        return "----"
    return round(float(TP)/(TP + FN),3)

def computeAccuracy(TP,FP,TN,FN):
    return round(float(TP+TN)/(TP + TN + FP + FN),3)

def evaluate(root, data,alist, classification):
    classification = classification.values()[0]
    evalResult = {}

    for c in classification:
        TPCount = 0
        TNCount = 0
        FPCount = 0
        FNCount = 0

        for d in data:
            cl = root.classify(d[:-1], alist)

            if d[-1] == cl:
                if c == cl:
                    TPCount += 1
                else:
                    TNCount += 1
            else:
                if c == cl:
                    FPCount += 1
                else:
                    FNCount += 1
        p = computePrecision(TPCount,FPCount,TNCount,FNCount)
        r = computeRecall(TPCount,FPCount,TNCount,FNCount)
        a = computeAccuracy(TPCount,FPCount,TNCount,FNCount)
        evalResult[c] = (p,r,a)
    drawChart(evalResult)
    return evalResult

def drawChart(Result):
    for c in Result.keys():
        print "Class:     ",c
        print "Precision: ",Result[c][0]
        print "Recall:    ",Result[c][1]
        print "Accuracy:  ",Result[c][2]
        print "\n"
    print "------------------------------"

def evalZeroR(trainDataset,testDataset,classification,attrs):
    classification = classification.values()[0]
    evalResult = {}
    zeroR = readARFF.computeZeroR(attrs,trainDataset)

    for c in classification:
        TPCount = 0
        TNCount = 0
        FPCount = 0
        FNCount = 0
        if zeroR == c:
            for i in testDataset:
                if i[-1] == zeroR:
                    TPCount += 1
                else:
                    FPCount += 1
        else:
            for i in testDataset:
                if i[-1] == zeroR:
                    TNCount += 1
                else:
                    FNCount += 1

        p = computePrecision(TPCount,FPCount,TNCount,FNCount)
        r = computeRecall(TPCount,FPCount,TNCount,FNCount)
        a = computeAccuracy(TPCount,FPCount,TNCount,FNCount)
        evalResult[c] = (p,r,a)

    drawChart(evalResult)
    return evalResult



if __name__ == '__main__' :
    if len(sys.argv) < 2 :
        print "Usage: decisionTree.py #datasetName"
        sys.exit(-1)
    fname = sys.argv[-1]
    (attrs, data, classification) = readARFF.readArff(open(fname))

    resultTest = {}
    resultTrain = {}
    resultZeroR = {}
    for time in range(5):
        print "Round ",time+1,":"
        index = range(len(data))
        trainSample = random.sample(index,int(len(data)*0.8))
        testSample = [i for i in index if i not in trainSample]

        trainDataset = [data[i] for i in trainSample]
        testDataset = [data[i] for i in testSample]

        print "\nUsing ZeroR:"
        rz = evalZeroR(trainDataset,testDataset,classification,attrs)
        for k in rz:
            if k in resultZeroR:
                resultZeroR[k] += rz[k]
            else:
                resultZeroR[k] = rz[k]

        alist = [i.keys()[0] for i in attrs.values()]
        defaultValue = readARFF.computeZeroR(attrs,trainDataset)
        root = makeTree(trainDataset,attrs,defaultValue)
        print "\nTest Set: "
        r1 = evaluate(root,testDataset,alist, classification)
        for k in r1:
            if k in resultTest:
                resultTest[k] += r1[k]
            else:
                resultTest[k] = r1[k]
        print "\nTraining Set:"
        r2 = evaluate(root,trainDataset,alist, classification)
        for k in r1:
            if k in resultTrain:
                resultTrain[k] += r2[k]
            else:
                resultTrain[k] = r2[k]
        print "------------------------------"
    print "\nSummary: "
    print "Using ZeroR:"
    drawChart(resultZeroR)
    print "Test Set:"
    drawChart(resultTest)
    print "Training Set:"
    drawChart(resultTrain)
    print "------------------------------"



