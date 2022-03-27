const getMongoHandle = require('./getMongoHandle.js')
const cors = require('cors');
const express = require('express');
const app = express();

app.use(cors())
app.use(express.json())
app.listen(3004)

const getMarkerLocations = async () => {

    const model = getMongoHandle();
    let arr = (await model).find();
    let returnvar = arr.exec();
    return returnvar;
}

app.post('/marker', (req, res)=>{
    let markerQuery = getMarkerLocations();

    markerQuery.then((results)=>{
        console.log(results);
        res.send(results)})

})



module.exports = getMarkerLocations;
