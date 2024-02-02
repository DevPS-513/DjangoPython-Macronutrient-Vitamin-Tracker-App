import os
from requests.auth import HTTPBasicAuth
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse,HttpRequest
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json
import requests

from .forms import RegisterForm, PersonForm, FoodForm
from .models import  Person,Food,Meal,Day

from django.forms import inlineformset_factory

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
    
    person=Person()
    personform=PersonForm()
    foodform=FoodForm()

    today_obj, created = Day.objects.get_or_create(date=datetime.now().date())

    if request.method == 'POST':
        form_type = request.POST.get('form_type')
        if form_type == 'person_form':
            personform = PersonForm(request.POST)
            if personform.is_valid():
                person = Person(**personform.cleaned_data)
                person.update()
        elif form_type == 'day_form':
            foodform = FoodForm(request.POST)
            if foodform.is_valid():
                today_obj.foods.add(foodform.cleaned_data['description'])
                today_obj.save()
    else:
        personform = PersonForm()
        foodform = FoodForm()

    context = {
        'person': person if personform.is_valid() else 'Not POST',
        'formdata': personform,
        'foodform': foodform,
        'today_object': today_obj
    }

    return render(request, "djangoapp/macroapp.html", context)


