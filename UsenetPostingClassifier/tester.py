import hw5
import pickle
import argparse
from hw5 import Article
import random


def tester(articleCount):
  #random choose some articles
  articles_by_category = pickle.load(open("/Users/xo/Study/2013Fall/AI/homework5/pickleArticles/pickledArticle"))
  count = articleCount
  generateList =[]
  generateNum = 0
  correct = 0
  # print count
  l = 0
  while l < int(count):
    print l<count
    print l
    print count
    if l == count:
      break
    generateNum = random.randint(0,20000)
    if generateNum not in generateList:
      generateList.append(generateNum)
      l +=1
      colunm = articles_by_category.keys()[generateNum/1000]
      article = articles_by_category[colunm][generateNum%1000]
      result = hw5.classify(article)
      print "========="
      print result
      print colunm
      print "========="
      if result==colunm:
        correct += 1

    # l = len(generateList)

  print float(correct)/float(articleCount)

if __name__ == '__main__' :
  parser = argparse.ArgumentParser()
  parser.add_argument("count")
  args = parser.parse_args()
  count = args.count
  print count
  tester(count)









  # driver("/Users/xo/Downloads/20_newsgroups")