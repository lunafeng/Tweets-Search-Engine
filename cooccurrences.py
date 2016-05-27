#!/usr/bin/python
import json
import MySQLdb
from nltk.stem.porter import PorterStemmer
from nltk.corpus import stopwords
import sys
import re
import math

def main(word1Id,word2Id):
	db_mysql = MySQLdb.connect('141.117.3.92','lunafeng','luna222','CikmTwitterDataSet')
	db_mysql.ping()
	cursor = db_mysql.cursor()
	getCo = "select case when frequencyRefined != 0 then frequencyRefined else frequency end from CooccurrencesNoOneNoCommonRefined where word1=" + str(word1Id) + " and word2=" + str(word2Id)
	print "!!!!!!"
	print getCo
	try:
		cursor.execute(getCo)
		co = cursor.fetchone()
		co = co[0]
	except:
		co = 0
	cursor.close()
	db_mysql.close()
	return co 
