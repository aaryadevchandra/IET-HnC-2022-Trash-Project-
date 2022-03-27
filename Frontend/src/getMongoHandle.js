const mongoose  = require('mongoose')
//importing trash location schema
const schema = require('./trashSchema.js')

// all encompassing function that allows us to get an instance of the mongodb object
const getMongoHandle = async () => {

    // mongodb uri (please change username and password in production)
    const DBURI = 'mongodb+srv://Aaryadev:aurora1127@cluster0.jvar5.mongodb.net/iet-trash-project?retryWrites=true&w=majority';
    mongoose.connect(DBURI, (err, db)=>{
        if(err) console.log(err);
        else {
            console.log('Connected to DB');
        }
    });

    //creating mongo model using schema
    const locationModel = mongoose.model('Trashlocation', schema);
    return locationModel;
}

module.exports = getMongoHandle;