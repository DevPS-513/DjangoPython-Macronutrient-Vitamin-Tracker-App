from django.db import models
from django.utils.timezone import now
from django.conf import settings
import os
import pandas as pd

# Create your models here.

# <HINT> Create a Car Make model `class CarMake(models.Model)`:
# - Name
# - Description
# - Any other fields you would like to include in car make model
# - __str__ method to print a car make object


class CarMake(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=200)

    def __str__(self):
        return str(self.name)


class CarModel(models.Model):
    make = models.ForeignKey(CarMake, on_delete=models.CASCADE)
    dealerId = models.IntegerField()
    name = models.CharField(max_length=200, default="civic")

    type = models.CharField(max_length=200)
    year = models.DateField()

    def __str__(self):
        return str(self.make)


class Person(models.Model):

    GENDER_CHOICES = [('M', 'Male'),('F', 'Female'), ('O', 'Other')]
    ACTIVITY_LEVELS = [\
    ('1.2',"1.2x Sedentary(office job)"),
    ('1.375',"1.4x Lightly active(light sport 1-3 times/week)"),\
    ('1.55',"1.6x Moderately active(3-5 days/week)"),\
    ('1.725',"1.7x Very active(hard exercise 6-7 days/week)"),\
    ('1.9',"1.9x Extremely active(hard excercise and physical job)")\
]
    
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
    age = models.FloatField(default=None)
    weight_lbs = models.FloatField(default=None)
    height_in = models.CharField(max_length=100,choices=HEIGHTS)
    activity_level = models.CharField(max_length=8, choices=ACTIVITY_LEVELS, default='1.2')    
    bf = models.FloatField(default=-1)

    # outputs
    BMI = models.FloatField(default=-1)
    BMR = models.FloatField(default=-1)

    #self.ideal_weight_avg = None
    #self.ideal_weight_min = None
    #self.ideal_weight_max = None

    #self.muscular_peak_lbs = None
    #self.muscular_mid_lbs = None
    #self.muscular_light_lbs = None

    #self.muscular_peak_bf = None
    #self.muscular_mid_bf = None
    #self.muscular_light_bf = None


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


# <HINT> Create a Car Model model `class CarModel(models.Model):`:
# - Many-To-One relationship to Car Make model (One Car Make has many Car Models, using ForeignKey field)
# - Name
# - Dealer id, used to refer a dealer created in cloudant database
# - Type (CharField with a choices argument to provide limited choices such as Sedan, SUV, WAGON, etc.)
# - Year (DateField)
# - Any other fields you would like to include in car model
# - __str__ method to print a car make object


# <HINT> Create a plain Python class `CarDealer` to hold dealer data


class CarDealer:
    def __init__(
        self=None,
        address=None,
        city=None,
        full_name=None,
        id=None,
        lat=None,
        long=None,
        short_name=None,
        st=None,
        zip=None,
        state=None,
    ):
        self.id = id
        self.full_name = full_name
        self.city = city
        self.address = address
        self.lat = lat
        self.long = long
        self.short_name = short_name
        self.st = st
        self.zip = zip
        self.state = state
        self.important_fields_names = [
            "id",
            "full_name",
            "city",
            "address",
            "zip",
            "st",
        ]

    def __str__(self):
        return f"Dealer name:  { self.full_name}"

    def get_fields(self):
        return vars(self)

    def get_frontend_fieldnames(self):
        return {k: v for k, v in vars(self).items() if k in self.important_fields_names}

    def to_dict(self):
        return vars(self)


# <HINT> Create a plain Python class `DealerReview` to hold review data


class DealerReview:
    def __init__(
        self=None,
        dealership=None,
        name=None,
        purchase=None,
        review=None,
        purchase_date=None,
        car_make=None,
        car_model=None,
        car_year=None,
        sentiment=None,
        id=None,
    ):
        self.dealership = dealership
        self.name = name
        self.purchase = purchase
        self.purchase_date = purchase_date
        self.car_make = car_make
        self.car_model = car_model
        self.car_year = car_year
        self.sentiment = sentiment
        self.id = id
        self.review = review

        self.important_fields_names = [
            "name",
            "id",
            "dealership",
            "purchase_date",
            "car_make",
            "car_year",
            "review",
        ]

    def __str__(self):
        return f"Reviewer name: {self.name}"

    def get_fields(self):
        return vars(self)

    def get_frontend_fieldnames(self):
        return {k: v for k, v in vars(self).items() if k in self.important_fields_names}
