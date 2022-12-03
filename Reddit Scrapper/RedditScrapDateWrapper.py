#
#		Reddit Scrapper Wrapper (Monthly Scrap)
#		Created by Derek Kwan
#
#	Info: Extract specific period of reddit data from pushshift api..
#


import RedditScrapV2DB as rs
from datetime import datetime


#set the range of the scrapper
year = 2022
month = 11

#loop through each day and scrap the data (*It should be the last day of month + 1)
for day in range(3,31):
    #detect crash/error
    try:
        #convert start and end time format to eg.year-month-day 23:59:59
        start = datetime(year,month,day,23,59,59)
        end = datetime(year,month,day,0,0,0)
        #set the name of the post and comment file
        post = "post_"+ str(year) + "_" + str(month) + "_" + str(day) + ".csv"
        comment = "comment_"+ str(year) + "_" + str(month) + "_" + str(day) + ".csv"
        #uses the scrapper function
        rs.getDataWrapper(start,end,post,comment)
    except:
        #print in crash.txt the amount of time it has failed/crash/error
        with open('crash.txt', 'a') as files: 
            files.write("post_"+ str(year) + "_" + str(month) + "_" + str(day) + ".csv  failed \n")


