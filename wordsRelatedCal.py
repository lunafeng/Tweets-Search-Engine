#!/usr/bin/python
import MySQLdb
import os,sys
import json
import stemming, getId,cooccurrences, getWordsSimilarity, storeWordsSimilarity
import subprocess

def countSim(hash1,hash2):
	top = 0.0
	bottom1 = 0.0
	bottom2 = 0.0
	count = 0
	keys_list = hash1.keys()
	try:
		for element in keys_list:
			value1 = hash1[element]
			value2 = hash2[element]
			top = top + value1*value2
		for w1 in hash1:
			bottom1 = bottom1 + hash1[w1]**2
		for w2 in hash2:
			bottom2 = bottom2 + hash2[w2]**2
		return top/(bottom1*bottom2)**0.5
	except:
		return 0

def calculate(givenWord,loop,first,second):
	wordId1 = getId.main(stemming.main(givenWord))
	for tweetId in tweetIdList[first:second]:
		oneTweetWords = tweetId_words[tweetId]
		for word in oneTweetWords:
			wordId2 = getId.main(stemming.main(word))
			co = cooccurrences.main(wordId1,wordId2)
			if co > 0:
				similarityWord = getWordsSimilarity.main(wordId1,wordId2)
				if similarityWord == None:
					vector2 = json.load(open("/data/CikmTwitterProject/Paper/SearchTweets/WordsDistribution#5/"+str(wordId2)))
					similarityWord = countSim(vector1,vector2)
					storeWordsSimilarity.main(wordId1,wordId2,similarityWord)

def main(givenWord):
	wordId = getId.main(stemming.main(givenWord))
	global tweetIdList
	global tweetId_words
	global vector1
	tweetId_words = {}
	db_mysql = MySQLdb.connect('141.117.3.92','lunafeng','luna222','CikmTwitterDataSet')
	db_mysql.ping()
	cursor = db_mysql.cursor()
	getTweetWords = "select A.tweetId,w.word from Words w join (select c.tweetId,tw.wordId from " + givenWord + " c join TweetsWords tw on (c.TweetId = tw.TweetId)) A on (w.id = A.wordId) where A.wordId !=" + str(wordId)
	cursor.execute(getTweetWords)
	resultsRaw = cursor.fetchall()
	for result in resultsRaw:
		tweetId = result[0]
		word = result[1]
		if tweetId not in tweetId_words:
			tweetId_words[tweetId] = []
		tweetId_words[tweetId].append(word)
	cursor.close()
	db_mysql.close()


	vector1 = json.load(open("/data/CikmTwitterProject/Paper/SearchTweets/WordsDistribution#5/"+str(wordId)))


	pids = []
	tweetIdList = tweetId_words.keys()
	tweetIdList.sort()
	for loop in range(8):
		pid = os.fork()
		pids.append(pid)
		if pid == 0 :
			first = loop*len(tweetIdList)/8
			second = (loop+1)*len(tweetIdList)/8
			calculate(givenWord,loop,first,second)
			os._exit(0)
		else:
			continue
	for pid in pids:
		os.waitpid(pid,0)

words = ["Commercial","Import","Develop","Hotel","Message","Experience","Score","Hire","Chat","Rule","Enter","Joke","Tax","View","Kiss","Connect","Jump","Tool","Intern","Edit","Cake","Discuss","Burn","Inform","Push","Client","Cash"]
for word in words:
	print word
	main(word)
