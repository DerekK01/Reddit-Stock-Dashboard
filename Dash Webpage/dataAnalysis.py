#
#		Reddit Stock Analysis Module
#		Created by Derek Kwan
#
#	Info: Analysis Modules used in app.py
#



import requests
from datetime import datetime
import traceback
import time
import json
import sys
import csv
from pickle import TRUE
import pandas as pd
import numpy as np
import re
from collections import OrderedDict

# Header

# For Comment Database
# json tag
# score | created_utc | id | author | body | permalink |  

# For Post Database
# json tag
# score | created_utc | title | author | selftext | full_link | 



#Function: getNumberOfMention
#Require:  Url - The link of the api
#          Type - The database specified (posts or comments)
#Optional: Title - The keyword / phrase mentioned in the post title
#          Text - The keyword / phrase mentioned in the content of Post or Comments
#          Start - The start stime for the query (Format in Epoch utc)
#          End - The end stime for the query (Format in Epoch utc)
#Usage:    To get the number of keyword / phrase mentioned in a period of time

def getNumberOfMention(url,dbType,title=None,text=None,start=None,end=None):
    queryString = ""
    if title != None:
        queryString += f"&title={title}"
    if text != None:
        queryString += f"&text={text}"
    if start != None:
        queryString += f"&start={start}"
    if end != None:
        queryString += f"&end={end}"
    newUrl = url.format(dbType, queryString)
    jsonText = requests.get(newUrl)
    
    try:
        jsonData = jsonText.json()
    except json.decoder.JSONDecodeError:
        time.sleep(1)
    return len(jsonData)


#Function: constructQuery
#Require:  Url - The link of the api
#          dbType - The database specified (posts or comments)
#Optional: Title - The keyword / phrase mentioned in the post title
#          Text - The keyword / phrase mentioned in the content of Post or Comments
#          Start - The start stime for the query (Format in Epoch utc)
#          End - The end stime for the query (Format in Epoch utc)
#Usage:    Get the url for query
def constructQuery(url,dbType,title=None,text=None,start=None,end=None):
    queryString = ""
    if title != None:
        queryString += f"&title={title}"
    if text != None:
        queryString += f"&text={text}"
    if start != None:
        queryString += f"&start={start}"
    if end != None:
        queryString += f"&end={end}"
    newUrl = url.format(dbType, queryString)
    return newUrl


#Function: getAllSymbolFromCSV
#Optional: AMEX_file - File name for AMEX symbol list
#          NASDAQ_file - File name for NASDAQ symbol list
#          NYSE_file - File name for NYSE symbol list
#Usage:    Combine all the stock symbol in to a list

def getAllSymbolFromCSV(AMEX_file='AMEX_stock.csv',NASDAQ_file='NASDAQ_stock.csv',NYSE_file='NYSE_stock.csv'):
    symbol = []
    amex = pd.read_csv(AMEX_file)
    nasdaq = pd.read_csv(NASDAQ_file)
    nyse = pd.read_csv(NYSE_file)
    for stock in amex['Symbol']:
        symbol.append(stock)
    for stock in nasdaq['Symbol']:
        symbol.append(stock)
    for stock in nyse['Symbol']:
        symbol.append(stock)
    blacklist(symbol)
    return symbol

#Function: blacklist
#Require:  stock - The list of stock symbol 
#Usage:    remove the blacklisted symbol from the list

def blacklist(stock):
    blacklist_array = ['DD','A','NEW','OP','S','IS','AI','ON','JP','E','FOR','UP','IT','IRS','ARE','D','LMAO','YOU','R','USA','B','TA','BOOM','Y','TV']
    for i in blacklist_array:
        stock.remove(i)


#Function: symbolMentionCountPosts
#Require:  jsonData - The raw json data 
#Optional: mentionCount - A dictionary to store the mention increment (Can be used for cumilative)
#          reset - Reset the mentionCount dictionary
#Usage:    calculate the amount of times each stock symbol are mentioned in the json data
def symbolMentionCountPosts(jsonData,mentionCount= {},reset=False):
    if reset == True:
        mentionCount = {}
    data = pd.DataFrame.from_dict(jsonData)
    symbol = getAllSymbolFromCSV()
    for i in range(0,data.shape[0]-1):
        #If the data is not NULL
        if pd.notna(data['body'][i]):
            #Find the stock symbol
            word_set = set(symbol)
            phrase_set = set(re.findall(r"[\w']+|[.,!?;]", data['body'][i]))
            match = word_set.intersection(phrase_set)
            if match:
                for stock in match:
                    if stock in mentionCount:
                        mentionCount[stock] += 1
                    else:
                        mentionCount[stock] = 1
    return mentionCount


#Function: convertDictToArray
#Require:  dictionary - The dictionary to be converted
#Usage:    Convert a dictionary to array
def convertDictToArray(dictionary):
    data = np.array(list(dictionary.items()), dtype=object)
    return data


#Function: getTopMentionedStockTop10
#Require:  url - The API link
#Optional: start - Start time
#          end - End time 
#Usage:    Get the top 10 stock symbol mentioned in a specific period
def getTopMentionedStockTop10(url,start=None,end=None):
    newUrl = constructQuery(url,"comments",start=start,end=end)
    jsonText = requests.get(newUrl)
    jsonData = jsonText.json()
    
    mention = symbolMentionCountPosts(jsonData)
    mention_array = convertDictToArray(mention)
    mention_sorted = mention_array[mention_array[:, 1].argsort()]
    stock = []
    mention = []
    for i in range(np.shape(mention_sorted)[0]-1,np.shape(mention_sorted)[0]-11,-1):
        #print(mention_sorted[i])
        stock.append(mention_sorted[i][0])
        mention.append(mention_sorted[i][1])
    return stock, mention



#Function: getTopMentionedStock
#Require:  url - The API link
#Optional: start - Start time
#          end - End time 
#Usage:    Get the stock symbol mentioned in a specific period
def getTopMentionedStock(url,start=None,end=None):
    newUrl = constructQuery(url,"comments",start=start,end=end)
    jsonText = requests.get(newUrl)
    jsonData = jsonText.json()
    
    mention = symbolMentionCountPosts(jsonData)
    mentionDf = pd.DataFrame({'Stock': list(mention.keys()), 'Mentions': list(mention.values())})
    return mentionDf

