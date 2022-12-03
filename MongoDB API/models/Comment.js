const mongoose = require('mongoose');

//Data format
const PostSchema = mongoose.Schema({
    score: String,
    created_utc: Number,
    id: String,
    author: String,
    body: String,
    permalink: String,
}, { versionKey: false });

//set the collection name
//mongoose.model(name, schema, collectionName);
module.exports = mongoose.model('Reddit_Comment', PostSchema, 'Reddit_Comment');