import os
from dotenv import load_dotenv

load_dotenv()


API_CREDS = {
  'dealership_url': os.getenv('DEALERSHIP_URL'),
  'review_url': os.getenv('REVIEWS_URL'),

  'dealership_key': os.getenv('DEALERSHIP_API_KEY')

}


from requests.auth import HTTPBasicAuth
from .models import CarDealer,DealerReview


from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
# from .models import related models
# from .restapis import related methods
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json
import requests

from .forms import RegisterForm
from .models import CarDealer,CarMake,CarModel,DealerReview
from .restapis import get_request,get_dealers_from_cf,get_dealer_reviews_from_cf

import nltk
nltk.download('vader_lexicon')
from nltk.sentiment import SentimentIntensityAnalyzer
sia = SentimentIntensityAnalyzer()

with open(r"C:\localkeys\IBM_Watson_Credential.txt", 'r') as f:
    watson_api_keys = json.load(f)

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.

def home(request):
    return render(request, 'djangoapp/index.html', {})


# Create an `about` view to render a static about page
# def about(request):
# ...

def about(request):
    return render(request, 'djangoapp/about.html', {})


# Create a `contact` view to return a static contact page

def contact(request):
    return render(request, 'djangoapp/contact.html', {})


# Create a `login_request` view to handle sign in request
# def login_request(request):
# ...

# Create a `logout_request` view to handle sign out request
def logout_view(request):
    logout(request)
    return redirect('djangoapp:home')
# Create a `registration_request` view to handle sign up request
def register(request):

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user= form.save()
            login(request,user)
            return redirect('djangoapp/home')
    else:
        form = RegisterForm()

    return render(request,'djangoapp/register.html',{"form":form})


# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    dealership_url=API_CREDS['dealership_url']
    dealership_key=API_CREDS['dealership_key']
    context = {}
        #dealerships=get_request("http://127.0.0.1:5000/api/dealership",id=1)
    if request.method == "GET" :
        dealerships = get_dealers_from_cf(dealership_url,apikey=dealership_key)
    elif request.method =="POST":
        id = request.POST.get('id')
        dealerships = get_dealers_from_cf(dealership_url, id=id)
    else:
        dealerships = []

    context['dealerships']=dealerships
    print(dealerships)

    DealerProperties=CarDealer()

    context['fieldnames']=DealerProperties.get_frontend_fieldnames()

    print('fieldnames are \n\n',context['fieldnames'],'\n')

    return render(request, 'djangoapp/dealershiplist.html', context)


# Create a `get_dealer_details` view to render the reviews of a dealer
# def get_dealer_details(request, dealer_id):
# ...

# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealer_details(request):


    
    dealership_url=API_CREDS['dealership_url']
    reviews_url=API_CREDS['review_url']
    dealership_key=API_CREDS['dealership_key']


    context = {}
        #dealerships=get_request("http://127.0.0.1:5000/api/dealership",id=1)    
    dealer_reviews={}
    if request.method == "GET":
        id = request.GET.get('id')
        dealerships = get_dealers_from_cf(dealership_url, id=id,apikey=dealership_key)
        dealer_reviews=get_dealer_reviews_from_cf(reviews_url, id=id,apikey=dealership_key)

        print()
    else:
        dealerships ={'not':'found'}

    if(len(dealerships)==1):
        dealerships=list(dealerships)[0]

    context['dealer']=dealerships
    context['reviews']=dealer_reviews

    # Get all reviews for this dealer

 
    return render(request, 'djangoapp/get_dealer_details.html', context)



# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_reviews(request):
    reviews_url=API_CREDS['review_url']
    dealership_key=API_CREDS['dealership_key']
    context = {}
    reviews = []
        #dealerships=get_request("http://127.0.0.1:5000/api/dealership",id=1)
    if request.method == "GET" :
        response=requests.get(reviews_url, auth=HTTPBasicAuth('apikey', dealership_key))
        reviews=json.loads(response.text)
    
    newreviews=[]
    for review in reviews:

        review_obj = DealerReview()
        for key,item in review['doc'].items():
            setattr(review_obj,key,item)
            
        newreviews.append(review_obj)


    context['reviews']=newreviews

    ReviewProperties=DealerReview()
    print(type(reviews),len(reviews),"\n")
    print(reviews[0],type(reviews[0]))

    context['fieldnames']=ReviewProperties.get_frontend_fieldnames()

    print("\n","fieldnames are","\n",context['fieldnames'])

    return render(request, 'djangoapp/reviewlist.html', context)


def add_review(request):
    formdata = DealerReview()
    emptyform = vars(formdata)

    print(request.POST)

    if request.method == "POST":
        id = request.POST.get('id')
        print("id is ", id)
        reviews = []
        for var in emptyform.keys():
            try:
                print(var)
                print( request.POST.get(var))
                setattr(formdata, var, request.POST.get(var))
            except Exception as e:
                print("error")
                setattr(formdata, var, "None")



        formdata = vars(formdata)  # Update formdata with the saved data
    else:
        reviews = []

 

    return render(request, 'djangoapp/addreview.html', {"emptyform": emptyform, "formdata": formdata})



def test_nlu(request):
    context = {}
    
    reply='Initialized_to_None'

    if(request.method == 'GET'):


        reply=sia.polarity_scores("I love you") 


    return render(request, 'djangoapp/testnlu.html', {"watsonreply": reply})






# Create a `add_review` view to submit a review
# def add_review(request, dealer_id):
# ...

