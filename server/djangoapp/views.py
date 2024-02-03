import os
from requests.auth import HTTPBasicAuth
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse,HttpRequest
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
import pandas as pd 


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

    # keep this
    today_obj, created = Day.objects.get_or_create(name="Today",date=datetime.now().date())

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

    # convert to a datafrmae
        
    Day_df=pd.DataFrame(data=None,columns=['Description','Calories','Protein','fat','carbs','Vitamin A'])


    for food in today_obj.foods.all():
        
        Day_df_row=pd.DataFrame({'Description':food.description,'Calories':food.calories,\
                              'Protein':food.get_nutrient('protein'),'fat':food.get_nutrient('fat'),\
                                'carbs':food.get_nutrient('carb'),
                                'Vitamin A':food.get_vitamin_by_letter('A'),
                               'Vitamin C':food.get_vitamin_by_letter('C'), 
                               'Vitamin D':food.get_vitamin_by_letter('D')},index=[0])
        Day_df=pd.concat([Day_df,Day_df_row],axis=0)
    


    unit_dict={'g':1,'mg':0.001,'mcg':0.000001,'IU':0.0000000003,'kcal':1,'µg':0.000001}

    # now get the summation of every column
    totals=[]
    for i,nutrient in enumerate(['Calories','Protein','fat','carbs','Vitamin A','Vitamin C','Vitamin D']):
        totals.append(0)
        for val in Day_df[nutrient]:
            if(type(val)==str):
                values=val.split(' ')
                if len(values)>1:
                    totals[i]=totals[i]+float(values[0])*unit_dict[values[1]]
            else:
                totals[i]=totals[i]+float(val)

    daily_recommended_intake=["Recommended",person.BMR,int(.75*person.weight_lbs),'','',int(900),90,20]

    totals_df=pd.DataFrame({'Description':['Total',daily_recommended_intake[0]],\
                            'Calories':[totals[0],daily_recommended_intake[1]],\
                            'Protein(g)':[totals[1],daily_recommended_intake[2]],\
                                'fat':[totals[2],daily_recommended_intake[3]],\
                                'carbs':[totals[3],daily_recommended_intake[4]],\
                                'Vitamin A(mcg)':[totals[4],daily_recommended_intake[5]],
                                  'Vitamin C(mcg)':[totals[5],daily_recommended_intake[6]],
                                    'Vitamin D(mcg)':[totals[6],daily_recommended_intake[7]] })

    Day_df_html=Day_df.to_html(index=False,float_format="{:,.2f}".format)

    

    totals_df_html=totals_df.to_html(index=False,float_format="{:,.2f}".format)
    #      <td> {{food.description}}  </td>
    #  <td> {{food.calories}}  </td>
    #  <td> {{ food|get_nutrient:"protein" }}  </td>
    #  <td> {{ food|get_nutrient:"carb"  }}  </td>
    #  <td> {{ food|get_nutrient:"fat" }}  </td>
    #  <td> {{ food|get_vitamin_by_letter:"A" }}  </td>
    #  <td> {{ food|get_vitamin_by_letter:"D" }}  </td>
    #  <td> {{ food|get_vitamin_by_letter:"C" }}  </td>


    df = pd.DataFrame({
        'Jan': ['3', '6', 'Rec.'],
        'Feb': ['4', '8', 'Wait.'],
        'Mar': ['1', '8', 'Satus.']
    })

    # Convert the DataFrame to HTML
    df_html = df.to_html(index=False)


    context = {
        'person': person if personform.is_valid() else 'Not POST',
        'formdata': personform,
        'foodform': foodform,
        'today_object': today_obj,
        'Day_df_html':Day_df_html,
        'totals_df_html':totals_df_html,
        'sample_df':df_html
    }

    return render(request, "djangoapp/macroapp.html", context)


