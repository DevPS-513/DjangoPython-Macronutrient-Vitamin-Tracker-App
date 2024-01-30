from django.db import models
from django.utils.timezone import now
from django.conf import settings
import os
import pandas as pd


class Person(models.Model):

    GENDER_CHOICES = [('M', 'Male'),('F', 'Female'), ('O', 'Other')]
    ACTIVITY_LEVELS = [\
    ('1.2',"1.2x Sedentary(office job)"),
    ('1.375',"1.4x Active(1-3 times/week)"),\
    ('1.55',"1.6x  Athlete(3-5 days/week)"),\
    ('1.725',"1.7x Beast(6-7 days/week)"),\
    ('1.9',"1.9x Champion(7/week all-day)")\
    ]

    AGES=[]

    for i in range(0,130):
        AGES.append((str(i),str(i)))
    
    file_path=os.path.join(settings.BASE_DIR,'static\\data\\height_list_in_to_ft_in.txt')
    print(file_path)
    HEIGHTS = []

    height_df=pd.read_csv(file_path,header=None,index_col=None)

    for i in height_df.index.values:
        HEIGHTS.append((height_df.iloc[i,0],height_df.iloc[i,1]))
        if(i==0):
            print("looks like")
            print(HEIGHTS)
  

    gender = models.CharField(max_length=1,choices=GENDER_CHOICES,default="male")
    age = models.CharField(max_length=3,choices=AGES)
    weight_lbs = models.FloatField(default=None)
    height_in = models.CharField(max_length=100,choices=HEIGHTS)
    activity_level = models.CharField(max_length=8, choices=ACTIVITY_LEVELS, default='1.2')    
    bf = models.FloatField(default=-1)

    # outputs
    BMI = models.FloatField(default=-1)
    BMR = models.FloatField(default=-1)


    def update(self):
        weight_Kg = self.weight_lbs / 2.2046
        height_in_meters = (self.height_in / 2.54) / 100

        self.BMI = weight_Kg / (height_in_meters * height_in_meters)

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


        self.BMR = (
            dc_offset
            + weight_const * self.weight_lbs
            + height_const * self.height_in
            + age_constant * self.age
        )

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


