/**
 * Get all dealerships
 */
const express = require('express');
const app=express()
const PORT = 5000;
const bodyParser = require('body-parser');

const { CloudantV1 } = require('@ibm-cloud/cloudant');
const { IamAuthenticator } = require('ibm-cloud-sdk-core');


const params = require("C:\\localkeys\\IBM_Cloud_Key.json");


function get_dealerships(params) {

    const authenticator = new IamAuthenticator({ apikey: params.IAM_API_KEY })
    const cloudant = CloudantV1.newInstance({
      authenticator: authenticator
    });
    cloudant.setServiceUrl(params.COUCH_URL);

    let dbListPromise = getDbs(cloudant);

    return  getAllRecords(cloudant,"dealerships");
}

function get_reviews(params) {

    const authenticator = new IamAuthenticator({ apikey: params.IAM_API_KEY })
    const cloudant = CloudantV1.newInstance({
      authenticator: authenticator
    });
    cloudant.setServiceUrl(params.COUCH_URL);

    let dbListPromise = getDbs(cloudant);

    return  getAllRecords(cloudant,"reviews");
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

        let filterProperty;
        let filterValue;
    
        for (let prop in req.query) {
            filterProperty = prop;
            filterValue = req.query[prop];
        }
    

        if(filterValue){
        filterValue=filterValue.replace(/"/g,'');
        filterValue=filterValue.replace(/`/g,'');
        }

        if(filterProperty){
            filterProperty=filterProperty.replace(/"/g,'');
            filterProperty=filterProperty.replace(/`/g,'');
            }

        get_dealerships(params)
        .then(result => {
            if (filterProperty && filterValue ) {

                let filteredResult = result.result.filter(dealership=> dealership.doc[filterProperty] == filterValue);
                console.log(filteredResult)  
                res.status(200).send(filteredResult);
            } else {
                res.status(200).send(result);
            }
        })
        .catch(err=>res.status(500).send(err));

    });

    app.get('/api/review',(req,res)=> {

        let filterProperty;
        let filterValue;
    
        for (let prop in req.query) {
            filterProperty = prop;
            filterValue = req.query[prop];
        }
    

        if(filterValue){
        filterValue=filterValue.replace(/"/g,'');
        filterValue=filterValue.replace(/`/g,'');
        }

        if(filterProperty){
            filterProperty=filterProperty.replace(/"/g,'');
            filterProperty=filterProperty.replace(/`/g,'');
            }

        console.log(filterProperty)
        console.log(filterValue)

        get_reviews(params)
        .then(result => {
            if (filterProperty && filterValue ) {
                console.log(result.result)
                let filteredResult = result.result.filter(review=> review.doc[filterProperty] == filterValue);
                    res.status(200).send(filteredResult);
            } else {
                res.status(200).send(result);
            }
        })
        .catch(err=>res.status(500).send(err));

    });