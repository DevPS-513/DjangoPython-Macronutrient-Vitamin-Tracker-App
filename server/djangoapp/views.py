import os
from dotenv import load_dotenv

load_dotenv()


API_CREDS = {
  'dealership_url': os.getenv('DEALERSHIP_URL',''),
  'review_url': os.getenv('REVIEWS_URL',''),

  'dealership_key': os.getenv('DEALERSHIP_API_KEY',''),

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

from .forms import RegisterForm,ReviewForm
from .models import CarDealer,CarMake,CarModel,DealerReview
from .restapis import get_request,get_dealers_from_cf,get_dealer_reviews_from_cf

import nltk
nltk.download('vader_lexicon')


def get_emoticon_from_sentiment(sentiment_dict):
    # Get compound score
    compound_score = sentiment_dict.get('compound', 0)

    # Assign emoticon based on compound score
    if compound_score >= 0.3:
        return "😊"  # Positive sentiment
    elif compound_score <= -0.3:
        return "😞"  # Negative sentiment
    else:
        return "😐"  # Neutral sentiment







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
            return redirect('djangoapp:home')
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

    from nltk.sentiment import SentimentIntensityAnalyzer
    sia = SentimentIntensityAnalyzer()
    
    dealership_url=API_CREDS['dealership_url']
    reviews_url=API_CREDS['review_url']
    dealership_key=API_CREDS['dealership_key']

    context = {'dealership': {}}
    dealership={}
    newdealership=CarDealer()
    reviews={}
    review_list=[]


    if request.method == "GET":
        id = request.GET.get('id')
        dealership_url=str(dealership_url)+r'/'+str(id)
        reviews_url=str(reviews_url)

        dealer_response=requests.get(url=str(dealership_url), auth=HTTPBasicAuth('apikey', str(dealership_key)))
        rev_response=requests.get(url=str(reviews_url), auth=HTTPBasicAuth('apikey', str(dealership_key)))

        dealership=json.loads(dealer_response.text)
        reviews=json.loads(rev_response.text)

        print("dealership['doc']",dealership['doc'])

        dealership=dealership['doc']

        

        for review in reviews:
            try:
                if(int(review['doc']['id'])==int(id)):
                    sentiment_dict=sia.polarity_scores(review['doc']['review'])
                    review['doc']['sentiment']=sentiment_dict
                    review['doc']['sentiment_emoticon']=get_emoticon_from_sentiment(sentiment_dict)


                    review_list.append(review['doc'])
            except Exception as e:
                print(e)
                
      
        for (key,value) in dealership.items():
            try:
                setattr(newdealership,key,value)
            except:
                print(" no value for ",key)

    context['dealership']=newdealership.to_dict()
    context['fieldnames']=newdealership.get_frontend_fieldnames()

    context['reviews']=review_list
    return render(request, 'djangoapp/get_dealer_details.html', context)



# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_reviews(request):
    from nltk.sentiment import SentimentIntensityAnalyzer
    sia = SentimentIntensityAnalyzer()
    reviews_url=API_CREDS['review_url']
    dealership_key=API_CREDS['dealership_key']
    context = {}
    reviews = []
        #dealerships=get_request("http://127.0.0.1:5000/api/dealership",id=1)
    if request.method == "GET" :
        response=requests.get(url=str(reviews_url), auth=HTTPBasicAuth('apikey', str(dealership_key)))
        reviews=json.loads(response.text)
    
    newreviews=[]
    for review in reviews:

        review_obj = DealerReview()
        for key,item in review['doc'].items():
            setattr(review_obj,key,item)

        setattr(review_obj,'sentiment',sia.polarity_scores(review_obj.review))
        print(sia.polarity_scores(review_obj.review))

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
    form_names = formdata.get_frontend_fieldnames()
    response=requests.models.Response()
    json_to_send='not sent'

    dealership_url=API_CREDS['dealership_url']
    reviews_url=API_CREDS['review_url']
    dealership_key=API_CREDS['dealership_key']

    dealerships = get_dealers_from_cf(dealership_url,apikey=dealership_key)

    dealer_name_to_id_map={}

    for dealer in dealerships:
        dealer_name_to_id_map[dealer.full_name]=dealer.id

    if request.method == "POST":

        post_data=request.POST.copy()
        post_data['id']=dealer_name_to_id_map[post_data['dealership']]
            
        form=ReviewForm(post_data)

        # Get the ID and car

        if form.is_valid():
            formdata=form.cleaned_data
            data = {
                "doc": {
                    "name": str(formdata["name"]),
                    "id": str(dealer_name_to_id_map[formdata['dealership']]),
                    "dealership": str(formdata['dealership']),
                    "review": str(formdata['content']),
                    "purchase": str(formdata['purchasecheck']),
                    "purchase_date": str(formdata['purchase_date']),
                    "car_make": formdata['car'].make.name,
                    "car_model": formdata['car'].type,
                    "car_year": formdata['car'].year.year,
                    # Add other fields here as needed
                }
            }


            json_to_send=json.dumps(data)
            headers = {'Content-Type': 'application/json'}


            response=requests.post(url=str(reviews_url), headers=headers,data=json_to_send,auth=HTTPBasicAuth('apikey', str(dealership_key)))




    
    cars = CarModel.objects.all()
    return render(request, 'djangoapp/addreview.html', {"emptyform": form_names, 
                                                        "formdata": json_to_send,
                                                        "response": response.text,
                                                        "cars":cars,
                                                        "dealerships": dealerships})







# Create a `add_review` view to submit a review
# def add_review(request, dealer_id):
# ...

