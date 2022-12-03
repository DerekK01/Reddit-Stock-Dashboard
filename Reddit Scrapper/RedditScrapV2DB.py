#
#		Reddit Scrapper V2
#		Created by Derek Kwan
#
#	Info: Extract reddit data from pushshift api, and importing the data to MongoDB, in order to bypass the query restriction.
#



#Inspired by
#https://github.com/Watchful1/Sketchpad/blob/master/postDownloader.py

import requests
from datetime import datetime
import traceback
import time
import json
import sys
import csv
from pymongo import MongoClient

#set database connection
client = MongoClient("localhost:27017")
db=client.Reddit_stock




#pushshift api url = https://api.pushshift.io/reddit/submission/search?limit=1000&sort=desc&subreddit=wallstreetbets&after=1639238400&before=1639324799

def getDataWrapper(start,end,postfile,commentfile):
	username = ""  # username to get specific user post
	subreddit = "wallstreetbets"  # spcific subreddit post
	# leave either one blank to download an entire user's or subreddit's history
	# or fill in both to download a specific users history from a specific subreddit


	#set the filter, choose author or subreddit
	filter_string = None
	if username == "" and subreddit == "":
		print("Fill in either username or subreddit")
		sys.exit(0)
	elif username == "" and subreddit != "":
		filter_string = f"subreddit={subreddit}"
	elif username != "" and subreddit == "":
		filter_string = f"author={username}"
	else:
		filter_string = f"author={username}&subreddit={subreddit}"


	#convert the end time to timestamp
	end_time = int(end.timestamp())
	#create the url | {"submission" or "comment"} | {filter_string}
	#end time/start time timestamp need to be in string
	url = "https://api.pushshift.io/reddit/{}/search?limit=1000&sort=desc&{}&after=" + str(end_time) + "&before="

	#usage:
	#downloadFromUrl(filename, object_type,start_time,filter_string,url)
	downloadFromUrl(postfile, "submission",start,filter_string,url)
	downloadFromUrl(commentfile, "comment",start,filter_string,url)


def downloadFromUrl(filename, object_type,start_time,filter_string,url):
	#print in console the amount of file it is saving
	print(f"Saving {object_type}s to {filename}")

	count = 0
	previous_epoch = int(start_time.timestamp())
	



	while True:
		#sent get api request url
		#create the url | {"submission" or "comment"} | {filter_string}
		#"https://api.pushshift.io/reddit/{}/search?limit=1000&sort=desc&{}&after=" + str(end_time) + "&before="
		#end time/start time timestamp need to be in string
		new_url = url.format(object_type, filter_string)+str(previous_epoch)
		json_text = requests.get(new_url)
		time.sleep(1)  # pushshift has a rate limit, if we send requests too fast it will start returning error messages
		#get the json data
		try:
			json_data = json_text.json()
		except json.decoder.JSONDecodeError:
			time.sleep(1)
			continue

		#check if it is empty
		if 'data' not in json_data:
			break
		objects = json_data['data']
		if len(objects) == 0:
			break

		#format each data
		for object in objects:
			previous_epoch = object['created_utc'] - 1
			count += 1


			if object_type == 'comment':
				try:
					# getting the following json tag
					# score | created_utc | id | author | body | permalink | 
					
					# UPLOAD TO DATABASE
					data = {
        				'score' : str(object['score']),
        				'created_utc' : object['created_utc'],
        				'id' : object['id'],
						'author' : object['author'],
						'body' : object['body'],
						'permalink' : object['permalink']
    				}
					result=db.Reddit_Comment.insert_one(data)
				except Exception as err:
					print(f"Couldn't print comment: https://www.reddit.com{object['permalink']}")
					print(traceback.format_exc())
			elif object_type == 'submission':
				if object['is_self']:
					if 'selftext' not in object:
						continue
					# getting the following json tag
					# score | created_utc | title | author | selftext | full_link | 
					try:
						data = {
							'score' : str(object['score']),
							'created_utc' : object['created_utc'],
							'title' : object['title'],
							'author' : object['author'],
							'selftext' : object['selftext'],
							'full_link' : object['full_link']
						}
						result=db.Reddit_Post.insert_one(data)
					except Exception as err:
						print(f"Couldn't print post: {object['url']}")
						print(traceback.format_exc())

		#print saved message on console
		print("Saved {} {}s through {}".format(count, object_type, datetime.fromtimestamp(previous_epoch).strftime("%Y-%m-%d")))

	print(f"Saved {count} {object_type}s")
	#handle.close()


