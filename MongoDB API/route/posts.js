//
//		MongoDB API - get posts
//		Created by Derek Kwan
//
//	Info: setup get post
//



const express = require('express');

const router = express.Router();

//Connect to Post Database
const Post = require('../models/Post');

//query get
router.get('/query', async (req,res) => {
    try{
        if (req.query.start != undefined && req.query.end != undefined) {
            if (req.query.text != undefined && req.query.title != undefined) {
                query = await Post.find({"title" : {"$regex" : req.query.title},"selftext" : {"$regex" : req.query.text},"created_utc" : {"$gt":req.query.start,"$lt":req.query.end}});
            }else if (req.query.text === undefined && req.query.title != undefined){
                query = await Post.find({"title" : {"$regex" : req.query.title},"created_utc" : {"$gt":req.query.start,"$lt":req.query.end}});
            }else if (req.query.text != undefined && req.query.title === undefined){
                query = await Post.find({"selftext" : {"$regex" : req.query.text},"created_utc" : {"$gt":req.query.start,"$lt":req.query.end}});
            }else {
                query = await Post.find({"created_utc" : {"$gt":req.query.start,"$lt":req.query.end}});
            }
        }else if (req.query.start === undefined && req.query.end != undefined) {
            if (req.query.text != undefined && req.query.title != undefined) {
                query = await Post.find({"title" : {"$regex" : req.query.title},"selftext" : {"$regex" : req.query.text},"created_utc" : {"$lt":req.query.end}});
            }else if (req.query.text === undefined && req.query.title != undefined){
                query = await Post.find({"title" : {"$regex" : req.query.title},"created_utc" : {"$lt":req.query.end}});
            }else if (req.query.text != undefined && req.query.title === undefined){
                query = await Post.find({"selftext" : {"$regex" : req.query.text},"created_utc" : {"$lt":req.query.end}});
            }else {
                query = await Post.find({"created_utc" : {"$lt":req.query.end}});
            }
        }else if (req.query.start != undefined && req.query.end === undefined) {
            if (req.query.text != undefined && req.query.title != undefined) {
                query = await Post.find({"title" : {"$regex" : req.query.title},"selftext" : {"$regex" : req.query.text},"created_utc" : {"$gt":req.query.start}});
            }else if (req.query.text === undefined && req.query.title != undefined){
                query = await Post.find({"title" : {"$regex" : req.query.title},"created_utc" : {"$gt":req.query.start}});
            }else if (req.query.text != undefined && req.query.title === undefined){
                query = await Post.find({"selftext" : {"$regex" : req.query.text},"created_utc" : {"$gt":req.query.start}});
            }else {
                query = await Post.find({"created_utc" : {"$gt":req.query.start}});
            }
        } else {
            if (req.query.text != undefined && req.query.title != undefined) {
                query = await Post.find({"title" : {"$regex" : req.query.title},"selftext" : {"$regex" : req.query.text} });
            }else if (req.query.text === undefined && req.query.title != undefined){
                query = await Post.find({"title" : {"$regex" : req.query.title}});
            }else if (req.query.text != undefined && req.query.title === undefined){
                query = await Post.find({"selftext" : {"$regex" : req.query.text}});
            }
        }
        res.json(query);
    }catch(err){
        res.json({message:err})
    }
});

//export route
module.exports = router;