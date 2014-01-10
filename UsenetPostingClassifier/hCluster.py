import hw5
import pickle
import argparse
from hw5 import Article
import random
import heapq

path = "/Users/xo/Study/2013Fall/AI/homework5/"

cSet = {}
def combineTFIDF(a,b):
  tfidfForCategory={}
  subdict = {}
  #compute tfidf for each file under this directory
  #and add them up
  # article.computeTFIDF(idfUnderRoot)
  for w in cSet[a].keys():
    if w not in tfidfForCategory.keys():
      tfidfForCategory[w] = cSet[a][w]

  for w in cSet[b].keys():
    if w not in tfidfForCategory.keys():
      tfidfForCategory[w] = cSet[b][w]
    else:
      tfidfForCategory[w] += cSet[b][w]

  sortedList = heapq.nlargest(1000,tfidfForCategory,key=tfidfForCategory.__getitem__)

  for w in sortedList:
    subdict[w] = tfidfForCategory[w]

  return subdict


def hCluster():

	for i in hw5.categories:
		cSet[i]=pickle.load(open(path+"pickleTFIDF/"+i))
	maxSimilar = ["",""]
	maxValue = -2
	print "Start compare..."

	index = 1
	while len(cSet.keys()) >0:
		indexA = 0
		while indexA < len(cSet.keys()):
			indexB = indexA + 1
			while indexB < len(cSet.keys()):
				temp = hw5.cosineSimilarity(cSet[cSet.keys()[indexA]],cSet[cSet.keys()[indexB]])
				if temp > maxValue:
					maxSimilar = [cSet.keys()[indexA],cSet.keys()[indexB]]
					maxValue = temp
				indexB += 1
			indexA += 1

		print "("+maxSimilar[0]+" U "+maxSimilar[1]+")"
		cSet["("+maxSimilar[0]+" U "+maxSimilar[1]+")"] = combineTFIDF(maxSimilar[0],maxSimilar[1])
		print cSet["("+maxSimilar[0]+" U "+maxSimilar[1]+")"]
		del cSet[maxSimilar[0]]
		del cSet[maxSimilar[1]]

		print "Pass",index," finish!"
		index += 1
		maxValue = -2
		maxSimilar = ["",""]

	print cSet.keys()[0]

if __name__ == '__main__' :
  parser = argparse.ArgumentParser()
  parser.add_argument("path")
  args = parser.parse_args()
  path = args.path

  hCluster()






