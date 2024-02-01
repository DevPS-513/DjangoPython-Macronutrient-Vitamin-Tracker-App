import os
from requests.auth import HTTPBasicAuth
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse,HttpRequest
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect

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


# Create your views here.


def home(request):
    return render(request, "djangoapp/index.html", {})

def about(request):
    return render(request, "djangoapp/about.html", {})

def contact(request):
    return render(request, "djangoapp/contact.html", {})

def logout_view(request):
    logout(request)
    return redirect("djangoapp:home")

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


def macroapp(request: HttpRequest):    
    
    if(request.method=='POST'):
        personform=PersonForm(request.POST)
        if(personform.is_valid()):
            person=Person(**personform.cleaned_data)
            person.update()

            context={'person': person,'formdata':personform}
    else:
        personform=PersonForm()
        context={'person': {'Not POST'},'formdata':personform}

            

    return render(request,"djangoapp/macroapp.html",context)




