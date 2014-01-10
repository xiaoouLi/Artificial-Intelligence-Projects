import os
import collections
import math
import random
import sys
import pickle
import re
import heapq
import string
import argparse

punctuationSet = ['$','<','>','%','\'', '[',']','(',')','{','}','<','>',':',',', '...', '. . .','!','.','-','?','\'', '"', ';','/','*','&','|','^','_','\\']
path = ""
filePath = ""


stopWords = ["a", "about", "above", "above", "across", "after",
  "afterwards", "again", "against", "all", "almost", "alone", "along",
   "already", "also","although","always","am","among", "amongst",
   "amoungst", "amount",  "an", "and", "another", "any","anyhow",
   "anyone","anything","anyway", "anywhere", "are", "around", "as",
   "at", "back","be","became", "because","become","becomes", "becoming",
   "been", "before", "beforehand", "behind", "being", "below", "beside",
   "besides", "between", "beyond", "bill", "both", "bottom","but", "by",
   "call", "can", "cannot", "cant", "co", "con", "could", "couldnt",
   "cry", "de", "describe", "detail", "do", "done", "down", "due",
   "during", "each", "eg", "eight", "either", "eleven","else",
   "elsewhere", "empty", "enough", "etc", "even", "ever", "every",
   "everyone", "everything", "everywhere", "except", "few",
   "fifteen", "fify", "fill", "find", "fire", "first", "five",
   "for", "former", "formerly", "forty", "found", "four", "from",
   "front", "full", "further", "get", "give", "go", "had", "has",
   "hasnt", "have", "he", "hence", "her", "here", "hereafter",
   "hereby", "herein", "hereupon", "hers", "herself", "him",
   "himself", "his", "how", "however", "hundred", "ie", "if",
   "in", "inc", "indeed", "interest", "into", "is", "it",
   "its", "itself", "keep", "last", "latter", "latterly",
   "least", "less", "ltd", "made", "many", "may", "me", "meanwhile",
   "might", "mill", "mine", "more", "moreover", "most", "mostly",
   "move", "much", "must", "my", "myself", "name", "namely",
   "neither", "never", "nevertheless", "next", "nine", "no",
   "nobody", "none", "noone", "nor", "not", "nothing", "now",
    "nowhere", "of", "off", "often", "on", "once", "one", "only",
     "onto", "or", "other", "others", "otherwise", "our", "ours",
      "ourselves", "out", "over", "own","part", "per", "perhaps",
      "please", "put", "rather", "re", "same", "see", "seem",
      "seemed", "seeming", "seems", "serious", "several", "she",
      "should", "show", "side", "since", "sincere", "six", "sixty",
       "so", "some", "somehow", "someone", "something", "sometime",
        "sometimes", "somewhere", "still", "such", "system",
        "take", "ten", "than", "that", "the", "their", "them",
        "themselves", "then", "thence", "there", "thereafter",
        "thereby", "therefore", "therein", "thereupon", "these",
        "they", "thickv", "thin", "third", "this", "those", "though",
        "three", "through", "throughout", "thru", "thus", "to",
        "together", "too", "top", "toward", "towards", "twelve",
        "twenty", "two", "un", "under", "until", "up", "upon",
        "us", "very", "via", "was", "we", "well", "were", "what",
        "whatever", "when", "whence", "whenever", "where", "whereafter",
        "whereas", "whereby", "wherein", "whereupon", "wherever",
        "whether", "which", "while", "whither", "who", "whoever",
        "whole", "whom", "whose", "why", "will", "with", "within",
        "without", "would", "yet", "you", "your", "yours", "yourself",
        "yourselves", "the","maybe"]

TotalArticle = 20000
#articles_by_category store article object in each subdir
articles_by_category = collections.defaultdict(list)
categories = ["alt.atheism", "comp.sys.mac.hardware", "rec.motorcycles", "sci.electronics", "talk.politics.guns", "comp.graphics", "comp.windows.x", "rec.sport.baseball", "sci.med", "talk.politics.mideast", "comp.os.ms-windows.misc", "misc.forsale", "rec.sport.hockey", "sci.space", "talk.politics.misc", "comp.sys.ibm.pc.hardware", "rec.autos", "sci.crypt", "soc.religion.christian", "talk.religion.misc" ]

#store idf for each word under root
idfUnderRoot = {}


def cleanEmail(text):
  p = re.compile("[^\._-][\w\.-]+@(?:[A-Za-z0-9]+\.)+[A-Za-z]+$")


# DONE
def cleanup(raw_text):
  #Only remove punctuation on its own or at the start
  #or end of words, but if there are multiple punctuation
  #marks ("!??!!") remove them all.
  #Remove email address and stopwords which are stopwords list
  # return unique words
  p1 = re.compile("[^\._-][\w\.-]+@(?:[A-Za-z0-9-]+\.)+[A-Za-z-]+$")
  p2 = re.compile("[0-9]+")
  words = re.split("[ ]*",raw_text.strip())
  result = []
  #remove the puntuation at the beginning of the word
  for word in words:
    word = word.strip()
    for s in word:
      if s in punctuationSet:
        word = word[1:]
      else:
        break

    #remove the puntuation at the end of the word
    for s in word[::-1]:
      if s in punctuationSet:
        word = word[0:-1]
      else:
        break

    #to lower case
    if word.strip() and word not in stopWords and word not in result and not p1.match(word) and not p2.match(word):
      result.append(word.lower())
  return result


# DONE
class Article:
  def __init__(self, category, raw_text):
    self.category = category
    self.raw_text = raw_text
    self.wordlist = cleanup(raw_text)
    self.tf = collections.defaultdict(int) #tf dict
    self.tfidf = {} # tfidf dict
    self.computeTF()

  # DONE
  def computeTFIDF(self,idf):
    for word in self.tf.keys():
      self.tfidf[word] = self.tf[word] * idf[word]

  # DONE
  def computeTF(self):
    for word in self.wordlist:
      self.tf[word] += 1

  # DONE
  def getUniqueWords(self):
    return self.wordlist

def files(dir):
  list = []
  for dirpath, dirs, files in os.walk(dir):
    for f in files:
      qf = dirpath + "/" + f
      list.append(qf)
  return list

#DONE
def computeDocumentFrequency(directory):
  """Return word-DF dict of one category"""

  document_count = collections.defaultdict(int)
  total_file_count = 0
  path = filePath+directory
  for dirpath, dirs, files in os.walk(path):
    for f in files:
      if not f.startswith("."):
        total_file_count += 1
        # check whether the file contain a word
        try:
          infile = open(path+"/"+f,'r')
        except IOError:
            print "The file \"" + f + "\" dose not exit! Exit!"
            exit()

        article = Article(directory, infile.read().replace("\n"," ").replace("\r"," "))
        articles_by_category[directory].append(article)
        infile.close()
        for word in article.getUniqueWords():
          document_count[word] += 1
  return document_count

def computeTFIDFCategory(directory):
  tfidfForCategory={}
  subdict = {}
  for article in articles_by_category[directory]:
    #compute tfidf for each file under this directory
    #and add them up
    article.computeTFIDF(idfUnderRoot)
    for w in article.tfidf:
      if w not in tfidfForCategory.keys():

        tfidfForCategory[w] = article.tfidf[w]
      else:
        tfidfForCategory[w] += article.tfidf[w]

  sortedList = heapq.nlargest(1000,tfidfForCategory,key=tfidfForCategory.__getitem__)

  for w in sortedList:
    subdict[w] = tfidfForCategory[w]

  return subdict


def cosineSimilarity(tfidf1, tfidf2):
  """compare two tfidf vectors of two directories to see whether they are similar,
  if so, they are the same category."""

  for i in tfidf1.keys():
    if i not in tfidf2.keys():
      tfidf2[i] = 0.000001

  for i in tfidf2.keys():
    if i not in tfidf1.keys():
      tfidf1[i] = 0.000001

  up = 0.0
  bottom1 = 0.0
  bottom2 = 0.0
  for key in tfidf1.keys():
    up += tfidf1[key] * tfidf2[key]
    bottom1 += (tfidf1[key]*tfidf1[key])
    bottom2 += (tfidf2[key]*tfidf2[key])

  return up / (math.sqrt(bottom1) * math.sqrt(bottom2))



  # TODO
def classify(article):
  # get tfidf vector for this article
  maxCosin = -2
  similarCategory = ""
  #read in 20 pickled tfidf vectors and compare with article
  for i in categories:
    #pickleList store the names of categories
    cos = cosineSimilarity(article.tfidf,pickle.load(open(path+"pickleTFIDF/"+i)))
    if cos>maxCosin:
      maxCosin = cos
      similarCategory = i
  return similarCategory

def driver(root):
#go through root, to populate the
#"idfUnderRoot dict"
# at the same time, the articles_by_category dict is populated too
  for category in os.listdir(root):
     if not category.startswith("."):
        sublist = computeDocumentFrequency(category)
        for i in sublist.keys():
          if i not in idfUnderRoot:
            idfUnderRoot[i] = sublist[i]
          else:
            idfUnderRoot[i] += sublist[i]

  for i in idfUnderRoot:
    # print TotalArticle / idfUnderRoot[i]
    idfUnderRoot[i]=math.log(float(TotalArticle) / float(idfUnderRoot[i]))

  #calculate tfidf for 20 categories
  for category in os.listdir(root):
     if not category.startswith("."):
        #pickle 20 elements in the set
        tc = computeTFIDFCategory(category)
        # print category
        pickle.dump(tc,file(path+"pickleTFIDF/"+category,'w'))


if __name__ == '__main__' :
  parser = argparse.ArgumentParser()
  parser.add_argument("pathFile")
  parser.add_argument("pathPickle")
  args = parser.parse_args()
  path = args.pathPickle
  filePath = args.pathFile


  driver(filePath)
  pickle.dump(articles_by_category,file(path+"pickleArticles/pickledArticle",'w'))
































