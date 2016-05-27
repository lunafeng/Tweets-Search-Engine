#!/usr/bin/python
import MySQLdb
import getId,stemming

def main(word1,word2):
	db_mysql = MySQLdb.connect('141.117.3.92','lunafeng','luna222','CikmTwitterDataSet')
	db_mysql.ping()
	cursor = db_mysql.cursor()
	sql = "SELECT Similarity FROM WordsSimilarity WHERE Word1=" + str(word1) + " AND Word2=" + str(word2)
	try:
		cursor.execute(sql)
		similarity = cursor.fetchone()
	except:
		db_mysql.rollback()
	cursor.close()
	db_mysql.close()
	try:
		similarity = similarity[0]
		return similarity
	except:
		return None


words1 = getId.main(stemming.main("popcorn"))
words2 = getId.main(stemming.main("microwave"))
print main(words1,words2)
