#!/usr/bin/python
import MySQLdb
import os,sys
import json
import stemming, getId


def main(givenWord):
	wordId = getId.main(stemming.main(givenWord))
	db_mysql = MySQLdb.connect('141.117.3.92','lunafeng','luna222','CikmTwitterDataSet')
	db_mysql.ping()
	cursor = db_mysql.cursor()
	Max = 2.62507
	update = "UPDATE WordsSimilarity SET RefinedSimilarity=(" + str(Max) + "-ABS(Log(10,Similarity)))*10 WHERE RefinedSimilarity IS NULL"  
	print update
	cursor.execute(update)
	db_mysql.commit()
	cursor.close()
	db_mysql.close()

words = ["Commercial","Import","Develop","Hotel","Message","Experience","Score","Hire","Chat","Rule","Enter","Joke","Tax","View","Kiss","Connect","Jump","Tool","Intern","Edit","Cake","Discuss","Burn","Inform","Push","Client","Cash"]
for word in words:
	print word
	main(word)
