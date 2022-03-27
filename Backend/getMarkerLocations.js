// FOR DEV CHANDAN

const getMongoHandle = require('./getMongoHandle.js')

const getMarkerLocations = async () => {

    const model = getMongoHandle();
    let arr = (await model).find();
    arr.exec().then((res)=>console.log(res))
}

module.exports = getMarkerLocations;