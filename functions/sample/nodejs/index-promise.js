/**
 * Get all dealerships
 */
const express = require('express');
const app=express()
const PORT = 8080;
const bodyParser = require('body-parser');

const { CloudantV1 } = require('@ibm-cloud/cloudant');
const { IamAuthenticator } = require('ibm-cloud-sdk-core');

const params={
    COUCH_URL: "https://72144af7-975a-4c8a-b653-48177d4a207d-bluemix.cloudantnosqldb.appdomain.cloud/" ,
    IAM_API_KEY: "ySahisbUPABXdqzJc77nAytbcIFLdzMAiLeGuTPRWw5l",
    COUCH_USERNAME: "72144af7-975a-4c8a-b653-48177d4a207d-bluemix",
}


function get_dealerships(params) {

    const authenticator = new IamAuthenticator({ apikey: params.IAM_API_KEY })
    const cloudant = CloudantV1.newInstance({
      authenticator: authenticator
    });
    cloudant.setServiceUrl(params.COUCH_URL);

    let dbListPromise = getDbs(cloudant);

    return  getAllRecords(cloudant,"dealerships");
}






function getDbs(cloudant) {
     return new Promise((resolve, reject) => {
         cloudant.getAllDbs()
             .then(body => {
                console.log(body.result)
                 resolve({ dbs: body.result });

             })
             .catch(err => {
                  console.log(err);
                 reject({ err: err });
             });
     });
 }
 
 
 /*
 Sample implementation to get the records in a db based on a selector. If selector is empty, it returns all records. 
 eg: selector = {state:"Texas"} - Will return all records which has value 'Texas' in the column 'State'
 */
 function getMatchingRecords(cloudant,dbname, selector) {
     return new Promise((resolve, reject) => {
         cloudant.postFind({db:dbname,selector:selector})
                 .then((result)=>{
                   resolve({result:result.result.docs});
                 })
                 .catch(err => {
                    console.log(err);
                     reject({ err: err });
                 });
          })
 }
 
                        
 /*
 Sample implementation to get all the records in a db.
 */



 function getAllRecords(cloudant,dbname) {
     return new Promise((resolve, reject) => {
         cloudant.postAllDocs({ db: dbname, includeDocs: true, limit: 10 })            
             .then((result)=>{
               resolve({result:result.result.rows});
             })
             .catch(err => {
                console.log(err);
                reject({ err: err });
             });
         })
 }



 app.listen(
    PORT,
    () => console.log(`its alive on http://localhost:${PORT}`)
    
    )


    app.get('/api/dealership',(req,res)=> {

        let state = req.query.state;
        if(state){
        state=state.replace(/"/g,'');
        state=state.replace(/`/g,'');
        }


        get_dealerships(params)
        .then(result => {
            if (state) {

                let filteredResult = result.result.filter(dealership=> dealership.doc.state === state);
                    res.status(200).send(filteredResult);
            } else {
                res.status(200).send(result);
            }
        })
        .catch(err=>res.status(500).send(err));

    });


    app.get('/api/review',(req,res)=> {

        let dealerID = req.query.dealerID;
        console.log(dealerID)


        get_reviews(params)
        .then(result => {
            if (state) {

                let filteredResult = result.result.filter(dealership=> dealership.doc.state === state);
                    res.status(200).send(filteredResult);
            } else {
                res.status(200).send(result);
            }
        })
        .catch(err=>res.status(500).send(err));

    });