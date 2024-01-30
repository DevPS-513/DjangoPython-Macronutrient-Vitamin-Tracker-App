import os
from dotenv import load_dotenv

load_dotenv()


API_CREDS = {
    "dealership_url": os.getenv("DEALERSHIP_URL", ""),
    "review_url": os.getenv("REVIEWS_URL", ""),
    "dealership_key": os.getenv("DEALERSHIP_API_KEY", ""),
}


from requests.auth import HTTPBasicAuth

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

from .forms import RegisterForm, PersonForm
from .models import  Person

import nltk

nltk.download("vader_lexicon")


def get_emoticon_from_sentiment(sentiment_dict):
    # Get compound score
    compound_score = sentiment_dict.get("compound", 0)

    # Assign emoticon based on compound score
    if compound_score >= 0.3:
        return "😊"  # Positive sentiment
    elif compound_score <= -0.3:
        return "😞"  # Negative sentiment
    else:
        return "😐"  # Neutral sentiment


# Create your views here.


def home(request):
    return render(request, "djangoapp/index.html", {})


# Create an `about` view to render a static about page
# def about(request):
# ...


def about(request):
    return render(request, "djangoapp/about.html", {})


# Create a `contact` view to return a static contact page


def contact(request):
    return render(request, "djangoapp/contact.html", {})


# Create a `login_request` view to handle sign in request
# def login_request(request):
# ...


# Create a `logout_request` view to handle sign out request
def logout_view(request):
    logout(request)
    return redirect("djangoapp:home")


# Create a `registration_request` view to handle sign up request
def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("djangoapp:home")
    else:
        form = RegisterForm()

    return render(request, "djangoapp/register.html", {"form": form})



def macroapp(request):

    context={}

    formdata=PersonForm()

    context['formdata']=formdata


    return render(request,"djangoapp/macroapp.html",context)




