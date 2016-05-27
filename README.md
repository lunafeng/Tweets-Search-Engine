# Tweets-Search-Engine
Search for tweets which are semantic related with the query

This search engine is particularly designed for tweets search because the techniques adopted here are desgined specially for tweets. The goal of the search engine is return tweets that are highly semantic related with the query.

The detail of the algorithm is for each query, calculate its semantic similarity with tweets, tweets with higher semantic relatedness will be returned. The way to calculate the similarity between a query and a tweet is summing up the semantic relatedness score between each word in the tweet and the query.

The implementations includes three steps:

1. Calculate word similarity between query and tweets, store results in MySQL database.

Usage:
python wordsRelatedCal.py

This script run processes in parallel by using os.fork()

2. Refine the semantic relatedness score between words to obtain more accurate results

Usage:
python refineSim.py

3. Get final score for each tweet, tweet with higher score will be returned

Usage:
python searchTweets.py

The output of step 3 will be written into files.
