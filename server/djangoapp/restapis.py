import requests
import json
# import related models here
from requests.auth import HTTPBasicAuth
from .models import CarDealer,DealerReview

# im using the index-promise.js from previous
# lab since the functions option does not exist anymore in IBM cloud
#
#url="http://localhost:5000"
# Create a `get_request` to make HTTP GET requests
# e.g., response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
#                                     auth=HTTPBasicAuth('apikey', api_key))

import nltk
nltk.download('vader_lexicon')

from nltk.sentiment import SentimentIntensityAnalyzer
sia = SentimentIntensityAnalyzer()

def get_request(url,**kwargs):
    
    print(f'calling restapis.get_request({url})')

    apikey=kwargs.pop('apikey',None)
    headers=kwargs.pop('headers',None)
    data=kwargs.pop('data',None)

    try:
        
        if( apikey ):
            response=requests.post(url, headers=headers,data=data, auth=HTTPBasicAuth('apikey', apikey))
        else:
            response = requests.get(url, headers={'Content-Type': 'application/json'},
                                    params=kwargs)
            
        return response.text

    except Exception as e:
        print(e)
        return ''




# Create a `post_request` to make HTTP POST requests
    
def post_request(url,**kwargs):
    

    response = requests.post(url, params=kwargs, json=payload)

            
    return response.text


# e.g., response = requests.post(url, params=kwargs, json=payload)


# Create a get_dealers_from_cf method to get dealers from a cloud function
# def get_dealers_from_cf(url, **kwargs):
# - Call get_request() with specified arguments
# - Parse JSON results into a CarDealer object list

def get_dealers_from_cf(url, **kwargs):

    results=[]
    json_result=json.loads(get_request(url,**kwargs))

    if isinstance(json_result,dict) and 'result' in json_result:
        dealers=json_result['result']
    elif isinstance(json_result,list):
        dealers=json_result
    else:
        print("unexpected format of json result")
        return []

    if json_result:
        for dealer in dealers:
            dealer_doc=dealer["doc"]

            dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                                   id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                   short_name=dealer_doc["short_name"],
                                   st=dealer_doc["st"], zip=dealer_doc["zip"])
            
            results.append(dealer_obj)
    return results

def get_dealer_reviews_from_cf(url, **kwargs):

    results=[]
    json_result=json.loads(get_request(url,**kwargs))

    if isinstance(json_result,dict) and 'result' in json_result:
        dealers=json_result['result']
    elif isinstance(json_result,list):
        dealers=json_result
    else:
        print("unexpected format of json result")
        return []

    if json_result:
        #dealers = json_result["rows"]
        for dealer in dealers:

            dealer_obj=DealerReview()

            for var in dealer_obj.get_fields():

                try:
                    setattr(dealer_obj,var,dealer["doc"][var])
                except:
                    setattr(dealer_obj,var,None)

            
            # Now set the Sentiment
            try:
                setattr(dealer_obj,'sentiment',sia.polarity_scores(dealer_obj.review) )
            except:
                setattr(dealer_obj,'sentiment',"None" )

       
            results.append(dealer_obj)
    return results


# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
# def get_dealer_by_id_from_cf(url, dealerId):
# - Call get_request() with specified arguments
# - Parse JSON results into a DealerView object list


# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
# def analyze_review_sentiments(text):
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative



