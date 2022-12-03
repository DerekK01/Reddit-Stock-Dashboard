//
//		MongoDB API - get comments
//		Created by Derek Kwan
//
//	Info: setup get comments
//


const express = require('express');

const router = express.Router();

//Connect to Comment Database
const Post = require('../models/Comment');

//query get
router.get('/query', async (req,res) => {
    try{
        if (req.query.start != undefined && req.query.end != undefined) {
            if (req.query.text != undefined) {
                query = await Post.find({"body" : {"$regex" : req.query.text},"created_utc" : {"$gt":req.query.start,"$lt":req.query.end}});
            }else {
                query = await Post.find({"created_utc" : {"$gt":req.query.start,"$lt":req.query.end}});
            }
        }else if (req.query.start === undefined && req.query.end != undefined) {
            if (req.query.text != undefined) {
                query = await Post.find({"body" : {"$regex" : req.query.text},"created_utc" : {"$lt":req.query.end}});
            }else {
                query = await Post.find({"created_utc" : {"$lt":req.query.end}});
            }
        }else if (req.query.start != undefined && req.query.end === undefined) {
            if (req.query.text != undefined) {
                query = await Post.find({"body" : {"$regex" : req.query.text},"created_utc" : {"$gt":req.query.start}});
            }else {
                query = await Post.find({"created_utc" : {"$gt":req.query.start}});
            }
        } else {
            if (req.query.text != undefined) {
                query = await Post.find({"body" : {"$regex" : req.query.text} });
            }
        }
        res.json(query);
    }catch(err){
        res.json({message:err})
    }
});


//Export route
module.exports = router;