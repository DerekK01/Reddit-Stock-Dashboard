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


## Authors

Derek Kwan


## Version History

* 0.1
    * Initial Release

## License

This project is licensed under the MIT License - see the LICENSE.md file for details

## Acknowledgments

* [postDownloader](https://github.com/Watchful1/Sketchpad/blob/master/postDownloader.py)
