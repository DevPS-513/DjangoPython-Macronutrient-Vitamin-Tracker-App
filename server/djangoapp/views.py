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
from .forms import RegisterForm

from .restapis import get_request,get_dealers_from_cf


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
    context = {}
    if request.method == "GET":

        dealerships=get_request("http://127.0.0.1:5000/api/dealership",state="Texas")


        return render(request, 'djangoapp/dealershiplist.html', {"dealerships": dealerships})


# Create a `get_dealer_details` view to render the reviews of a dealer
# def get_dealer_details(request, dealer_id):
# ...

# Create a `add_review` view to submit a review
# def add_review(request, dealer_id):
# ...

