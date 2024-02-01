from django.db import models
from django.utils.timezone import now
from django.conf import settings
import os
import pandas as pd
import numpy as np

from dataclasses import dataclass
from typing import List

from django.db import models


class FoodNutrient(models.Model):
    type = models.CharField(max_length=50)
    name = models.CharField(max_length=150,default='',null=True)
    unitname = models.CharField(max_length=150,default='',null=True)
    max = models.FloatField(null=True)
    min = models.FloatField(null=True)
    median = models.FloatField(null=True)
    amount = models.FloatField(null=True)

    def __str__(self):
        return self.name

class Food(models.Model):
    description = models.CharField(max_length=200,unique=True)
    shortname=models.CharField(max_length=100,default='',null=True)
    foodNutrients = models.ManyToManyField(FoodNutrient)

    def __str__(self):
        return self.description

class MealFoodPortions(models.Model):
    meal = models.ForeignKey('Meal', on_delete=models.CASCADE)
    food = models.ForeignKey(Food, on_delete=models.CASCADE)
    portion_percent = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"{self.portion_percent}% of {self.food.description} in {self.meal.name}"

    
class Meal(models.Model):
    name=models.CharField(max_length=100)
    foods=models.ManyToManyField(Food, blank=True,through=MealFoodPortions)

    def __str__(self):
        return self.name


class Person(models.Model):

    GENDER_CHOICES = [('M', 'Male'),('F', 'Female'), ('O', 'Other')]
    ACTIVITY_LEVELS = [\
    ('1.2',"1.2x Sedentary(office job)"),
    ('1.375',"1.4x Active(1-3 days/week)"),\
    ('1.55',"1.6x Athlete(3-5 days/week)"),\
    ('1.725',"1.7x Beast(6-7 days/week)"),\
    ('1.9',"1.9x Champion(7 days/week)")\
    ]

    AGES=[]

    for i in range(0,130):
        AGES.append((str(i),str(i)))
    
    file_path=os.path.join(settings.BASE_DIR,'static\\data\\height_list_in_to_ft_in.txt')
    print(file_path)

  

    gender = models.CharField(max_length=1,choices=GENDER_CHOICES,default="male")
    age = models.CharField(max_length=3,choices=AGES,default='30')
    weight_lbs = models.FloatField(default=160)
    height_ft = models.FloatField(max_length=100,default=5)
    height_in = models.FloatField(max_length=100,default=8)

    activity_level = models.CharField(max_length=8, choices=ACTIVITY_LEVELS, default='1.2')    
    bf = models.FloatField(default=20)

    # outputs
    BMI = models.FloatField(default=-1)
    BMR = models.FloatField(default=-1)


    def update(self):
        weight_Kg = float(self.weight_lbs )/ 2.2046
        total_height_inches=(12*float(self.height_ft)+float(self.height_in) )
        height_in_meters = (total_height_inches*2.54) / 100

        self.BMI = np.round(weight_Kg / (height_in_meters * height_in_meters),1)

        if self.gender == "M":
            weight_const = 4.536
            dc_offset = 5
            height_const = 15.88
            age_constant = -5

        elif self.gender == "F":
            dc_offset = -161
            weight_const = 4.536
            height_const = 15.88
            age_constant = -5

        elif self.gender == "O":
            dc_offset = (-161+5)/2
            weight_const =4.536
            height_const = 15.88
            age_constant = -5

        else:
            dc_offset = 0
            weight_const = 0
            height_const = 0
            age_constant = 0


        self.BMR = (
            dc_offset
            + weight_const * float(self.weight_lbs)
            + height_const * float(total_height_inches)
            + age_constant * float(self.age)
        )

        self.BMR=int(np.round(  self.BMR,0))

    def __str__(self):
        out_str = ""
        for var in vars(self):
            out_str = out_str + var + "\t" + "=" + str(getattr(self, var)) 
        return out_str

    def get_fields(self):
        out_list = []
        for var in vars(self):
            out_list.append(var)
        return out_list

    def to_dict(self):
        keys = [keyval for keyval in vars(self)]
        values = [getattr(self, key) for key in keys]

        out_dict = {key: value for key, value in zip(keys, values)}

        return out_dict


