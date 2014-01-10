import re
import random
import sets

punctuationSet = ['$','<','>','%','\'', '[',']','(',')','{','}','<','>',':',',', '...', '. . .','!','.','-','?','\'', '"', ';','/','*','&','|','^','_','\\']
negWordsList = ['dont', "don't", 'wasnt', ' wouldnt', " wouldn't", "didn't", "hadn't", " mustn't", 'doesnt', "won't", " can't", "doesn't", 'hasnt', 'no', ' mustnt', 'isnt', ' cant', ' couldnt', " couldn't", "haven't", "weren't", 'arent', 'never', " shouldn't", 'werent', 'not', "aren't", 'havent', 'wont', ' shouldnt', "wasn't", "hasn't", 'hadnt', ' cannot', " shan't", ' shant', 'didnt', "isn't"]
tag = ['<pros>','</pros>','<cons>','</cons>']

def classify(negation):
	"""Classify the test sentence, calculate the accuracy and print the result"""

	pTests = createTests('pros-cons/IntegratedPros.txt',negation)
	cTests = createTests('pros-cons/IntegratedCons.txt',negation)
	TP = 0
	TN = 0
	for t in pTests:
		pCount = 0
		cCount = 0
		for w in t:
			if w in proWordSet:
				pCount += 1
			elif w in conWordSet:
				cCount += 1
		if pCount>cCount:
			TP += 1
		elif pCount == cCount:
			TP += random.randint(0,1)

	for t in cTests:
		pCount = 0
		cCount = 0
		for w in t:
			if w in proWordSet:
				pCount += 1
			elif w in conWordSet:
				cCount += 1
		if pCount<cCount:
			TN += 1
		elif pCount == cCount:
			TN += random.randint(0,1)

	if negation:
		print "====Negation Classify===="
	else:
		print "====Simple Classify===="
	print "Accuracy for pros testing is:"
	print round(float(TP)/len(pTests),3)
	print "Accuracy for cons testing is:"
	print round(float(TN)/len(cTests),3)

def train():
	"""Read opinion-lexicon file and store the words in local list"""

	proWordList = []
	conWordList = []

	fpro = file('opinion-lexicon-English/positive-words.txt','r')
	fcon = file('opinion-lexicon-English/negative-words.txt','r')
	for i in fpro:
		i = i.strip('\n')
		if i and not i.startswith(';'):
			proWordList.append(i)

	proWordSet = set(proWordList)
	for i in fcon:
		i = i.strip('\n')
		if i and not i.startswith(';'):
			conWordList.append(i)
	conWordSet = set(conWordList)

	# negate words' sentiment
	for p in proWordSet:
		conWordSet.add('NOT_'+p)
	for c in conWordSet:
		# prevent NOT_NOT_xxx
		if not c.startswith('NOT_'):
			proWordSet.add('NOT_'+c)
	return proWordSet, conWordSet

def createTests(infile,negation):
	"""Read pros-cons file and get all words in all test cases"""

	testSet = []
	f = file(infile,'r')
	for i in f:
		i = i.lower().strip('\n').strip(' ')
		for t in tag:
			i = i.replace(t,'')
		wordList = re.findall("[\w|-|']+|[,.;!/]",i)

		# flap word sentiment
		if negation:
			flapSentiment(wordList)
		testSet.append(wordList)
	return testSet

def flapSentiment(wordList):
	"""Flap the word sentiment"""
	flag = 0
	for i in range(len(wordList)):
		#start negate word sentiment, till meet a punctuation
		if wordList[i] in negWords:
			flag = 1
		#reset the negation, since this sentence is ended
		elif wordList[i] in punctuationSet:
			flag = 0
		#flap the sentiment by adding a "NOT_"
		elif flag:
			wordList[i] = "NOT_" + wordList[i]


if __name__ == '__main__':
	negWords = set(negWordsList)
	proWordSet,conWordSet = train()

	classify(False)
	classify(True)












