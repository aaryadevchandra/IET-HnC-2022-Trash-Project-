// mongo schema

const mongoose = require('mongoose')
const schema = new mongoose.Schema({
    "lat": "string",
    "lng": "string",
    "timestamp": "string"
})

module.exports = schema;