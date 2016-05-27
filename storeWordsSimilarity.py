#!/usr/bin/python
import MySQLdb

def main(word1,word2,similarity):
	db_mysql = MySQLdb.connect('141.117.3.92','lunafeng','luna222','CikmTwitterDataSet')
	db_mysql.ping()
	cursor = db_mysql.cursor()
	insert = "(" + str(word1) + "," + str(word2) + "," + str(similarity) + ")"
	sql1 = "INSERT INTO WordsSimilarity(Word1,Word2,Similarity) VALUES " + insert 
	sql2 = "INSERT INTO WordsSimilarity(Word2,Word1,Similarity) VALUES " + insert 
	try:
		cursor.execute(sql1)
		db_mysql.commit()
	except:
		db_mysql.rollback()
	try:
		cursor.execute(sql2)
		db_mysql.commit()
	except:
		db_mysql.rollback()
	cursor.close()
	db_mysql.close()


