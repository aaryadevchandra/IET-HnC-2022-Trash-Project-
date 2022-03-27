const getMongoHandle = require('./getMongoHandle.js')
const cors = require('cors');
const express = require('express');
const app = express();

app.use(cors())
app.use(express.json())
app.listen(3000)


// api for receiving trash ka location
app.post('/sendtrashlocation', async (req, res)=>{
    console.log('dev work' + req.body.lat); // req.body is a json object with two keys - lat,lng

    // will return mongoose model
    const locationModel = await getMongoHandle();
    
    //creating new mongo instance by using returned model model
    const newLocationModelInstance = new locationModel({'lat': req.body.lat, 'lng': req.body.lng, 'timestamp': req.body.timestamp})
    
    // saving the above created instance in mongo
    const instanceSaveVar = await newLocationModelInstance.save();
    console.log('new object' + instanceSaveVar); 
    res.sendStatus(200);
})