"""IBM Cloud Function that gets all reviews for a dealership

Returns:
    List: List of reviews for the given dealership
"""
from cloudant.client import Cloudant
from cloudant.error import CloudantException
import requests

from flask import Flask, jsonify, request
import json
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


param_dict ={
    "COUCH_URL": "72144af7-975a-4c8a-b653-48177d4a207d-bluemix.cloudantnosqldb.appdomain.cloud" ,
    "IAM_API_KEY": "ySahisbUPABXdqzJc77nAytbcIFLdzMAiLeGuTPRWw5l",
    "COUCH_USERNAME": "72144af7-975a-4c8a-b653-48177d4a207d-bluemix",
}	

def main(param_dict):
    """Main Function

    Args:
        param_dict (Dict): input paramater

    Returns:
        _type_: _description_ TODO
    """


    print("params are",param_dict["COUCH_USERNAME"], param_dict["IAM_API_KEY"],param_dict['COUCH_URL'])

    try:
        client = Cloudant.iam(
            account_name=param_dict["COUCH_USERNAME"],
            api_key=param_dict["IAM_API_KEY"],url=param_dict["COUCH_URL"],
            connect=True,
        )

     #   print(f"Databases: {client.all_dbs()}")
    except CloudantException as cloudant_exception:
        print("unable to connect")
        return {"error": cloudant_exception}
    except (requests.exceptions.RequestException, ConnectionResetError) as err:
        print("connection error")
        return {"error": err}
    
    dbs_content = {}
    for db_name in client.all_dbs():
        db = client[db_name]
        dbs_content[db_name]=db.all_docs(include_docs=True)['rows']

    return {"dbs": dbs_content}




@app.route('/', methods=['GET'])
def home():
    return main(param_dict)


@app.route('/reviews', methods=['GET'])
def reviews():
    result=main(param_dict)

 

    return  {'message': result}, 201


@app.route('/reviews', methods=['POST'])
def add_reviews():
    review_data = request.get_json()

    
    try:
        client = Cloudant.iam(
            account_name=param_dict["COUCH_USERNAME"],
            api_key=param_dict["IAM_API_KEY"],url=param_dict["COUCH_URL"],
            connect=True,
        )

     #   print(f"Databases: {client.all_dbs()}")
    except CloudantException as cloudant_exception:
        print("unable to connect")
        return {"error": cloudant_exception}
    except (requests.exceptions.RequestException, ConnectionResetError) as err:
        print("connection error")
        return {"error": err}
    
    review_db=client['reviews']

    new_review=review_db.create_document(review_data)
    
        # Check if the document was saved
    if new_review.exists():
        return {'message': 'Review added successfully'}, 201
    else:
        return {'message': 'Error adding review'}, 500




app.run(port=5000,debug=True)

