# Reddit Stock Dashboard

The project is inspired by the GME event on Jan 28, 2021.  An analysis on GME short squeeze was posted on subreddit Wallstreetbets which trend for multiple weeks. The short squeeze ultimatly happened with an 800% to the up side. 

## Description

This project aims to show the correlation between stock prices and the reddit users sentiment. The dashboard display the amount of time each stock symbol are mentioned everyday. The top 10 stock are also shown in a table, which can be used to identify any trending stock. 


![Sample](https://github.com/DerekK01/Reddit-Stock-Dashboard/blob/master/Sample%20Screenshot.png)

## Getting Started

### Requirement

* MongoDB
* REST API
* Dash module from Plotly
* Pushshift API

### Installing

* Install all the requirements.txt

### Executing program
* Install and run MongoDB on your devices.
```
sudo systemctl start mongod
```
* Run Reddit Scrapper/RedditScrapDateWrapper.py
* Run the REST API (MongoDB API/app.js)
```
npm start
```
* Run  Dash Webpage/app.py 

### MongoDB API Usage

Connection: ```http://localhost:3000/```

Access post database: ```http://localhost:3000/posts/```

Access comment database: ```http://localhost:3000/comments/```

Post  database query: ```http://localhost:3000/posts/query?```

Usable filter:
* Start: Start date in Epoch utc (exclusive)
* End: End date in Epoch utc (exclusive)
* Title: Post Title keyword search
* Text: Post content search 

Eg. To search for a end time 1639250000 to start time 1639239486 with a title keyword “Short” and a text keyword “SE” will be
```http://localhost:3000/posts/query?end=1639250000&title=Short&text=SE&start=1639239486```


Comment database query: ```http://localhost:3000/comments/query?```

Usable filter:
* Start: Start date in Epoch utc (exclusive)
* End: End date in Epoch utc (exclusive)
* Text: Comment content search 

Eg. To search for a end time 1639320343 to start time 1639320350 with a keyword “Put”
```http://localhost:3000/comments/query?end=1639320350&text=Put &start=1639320343```





## Authors

Derek Kwan


## Version History

* 0.1
    * Initial Release

## License

This project is licensed under the MIT License - see the LICENSE.md file for details

## Acknowledgments

* [postDownloader](https://github.com/Watchful1/Sketchpad/blob/master/postDownloader.py)
