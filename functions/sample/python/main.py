"""IBM Cloud Function that gets all reviews for a dealership

Returns:
    List: List of reviews for the given dealership
"""
from cloudant.client import Cloudant
from cloudant.error import CloudantException
import requests


param_dict ={
    "COUCH_URL": "72144af7-975a-4c8a-b653-48177d4a207d-bluemix.cloudantnosqldb.appdomain.cloud" ,
    "IAM_API_KEY": "ySahisbUPABXdqzJc77nAytbcIFLdzMAiLeGuTPRWw5l",
    "COUCH_USERNAME": "72144af7-975a-4c8a-b653-48177d4a207d-bluemix",
}
	
#https://72144af7-975a-4c8a-b653-48177d4a207d-bluemix.cloudantnosqldb.appdomain.cloud

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

        print(f"Databases: {client.all_dbs()}")
    except CloudantException as cloudant_exception:
        print("unable to connect")
        return {"error": cloudant_exception}
    except (requests.exceptions.RequestException, ConnectionResetError) as err:
        print("connection error")
        return {"error": err}

    return {"dbs": client.all_dbs()}

main(param_dict)

