//
//		MongoDB API
//		Created by Derek Kwan
//
//	Info: Connect to the local Mongo Database and provide get request
//




//Import
const express = require('express');

const app = express();

const mongoose = require('mongoose');
const bodyParser = require('body-parser');
const cors = require('cors');
require('dotenv/config');
//convert body to json
app.use(cors());
app.use(bodyParser.json());
//Middlewares

//app.use('/posts', () => {
//    console.log("Middleware running");
//});


//connect to DB
mongoose.connect(process.env.DB_CONNECTION, {useNewUrlParser: true}, () =>
    console.log('connected to DB!')
);

//Import route 
const postsRoute = require('./route/posts');
const commentsRoute = require('./route/comments');
//middleware
app.use('/posts', postsRoute);
app.use('/comments', commentsRoute);

//Route
app.get('/', (req,res) => {
    res.send('We are on home');
});


//listen to the server
app.listen(3000);