#!/usr/bin/python
import MySQLdb
import os,sys
import json
import stemming, getId, cooccurrences, getWordsRefinedSimilarity
import subprocess
import time


def calculate(givenWord,loop,first,second):
	fd = open("Luna"+givenWord+"RemoveCo0"+str(loop),"w+")
	wordId1 = getId.main(stemming.main(givenWord))
	for tweetId in tweetIdList[first:second]:
		similarityFinal = 0
		oneTweetWords = tweetId_words[tweetId]
		length = 0
		length = len(oneTweetWords)
		for word in oneTweetWords:
			wordId2 = getId.main(stemming.main(word))
			co = cooccurrences.main(wordId1,wordId2)
			if co > 0:
				similarityWord = getWordsRefinedSimilarity.main(wordId1,wordId2)
				similarityFinal += float(similarityWord)
		similarityFinal = float(similarityFinal)/length
		fd.write(str(tweetId))
		fd.write("\t")
		fd.write(str(float(similarityFinal)))
		fd.write("\n")
		fd.flush()

def main(givenWord):
	db_mysql = MySQLdb.connect('141.117.3.92','lunafeng','luna222','CikmTwitterDataSet')
	wordId = getId.main(stemming.main(givenWord))
	global tweetIdList
	global tweetId_words
	global vector1
	tweetId_words = {}
	while(db_mysql.open != 1):
		db_mysql.ping()
	cursor = db_mysql.cursor()
	# removed words itself and love, like, day, lol, today, tomorrow, time, tonight, thing, ready, found,free
	getTweetWords = "select A.tweetId,w.word from Words w join (select c.tweetId,tw.wordId from " + givenWord + " c join TweetsWords tw on (c.TweetId = tw.TweetId)) A on (w.id = A.wordId) where A.wordId !=" + str(wordId) + " and A.wordId != 1804507 and A.wordId != 1040690 and A.wordId != 1111170 and A.wordId != 991563 and A.wordId != 13304 and A.wordId != 3368935 and A.wordId != 2113819 and A.wordId != 1990840 and A.wordId != 2977454 and A.wordId != 3489500 and A.wordId != 1326944 and A.wordId != 419686"
	cursor.execute(getTweetWords)
	resultsRaw = cursor.fetchall()
	cursor.close()
	db_mysql.close()
	for result in resultsRaw:
		tweetId = result[0]
		word = result[1]
		if tweetId not in tweetId_words:
			tweetId_words[tweetId] = []
		tweetId_words[tweetId].append(word)


	vector1 = json.load(open("/data/CikmTwitterProject/Paper/SearchTweets/WordsDistribution#5/"+str(wordId)))


	pids = []
	tweetIdList = tweetId_words.keys()
	print "length:",len(tweetIdList)
	time.sleep(1)
	tweetIdList.sort()
	calculate(givenWord,0,0,len(tweetIdList))

words = ["Forget","Lead","Ride","Shoot","Wake","Bless","Offer","Lie","Review","Laugh","Dress","Band","Bore","Chick","Artist","Spend","Church","Perfect","Box","Cook","Wine","Tune","Message","Fat","Expect","Fix","Gym","Summer"]
for word in words:
	main(word)
	time.sleep(30)
