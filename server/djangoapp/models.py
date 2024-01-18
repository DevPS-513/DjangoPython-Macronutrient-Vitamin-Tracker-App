from django.db import models
from django.utils.timezone import now


# Create your models here.

# <HINT> Create a Car Make model `class CarMake(models.Model)`:
# - Name
# - Description
# - Any other fields you would like to include in car make model
# - __str__ method to print a car make object

class CarMake(models.Model):
    name=models.CharField(max_length=200)
    description=models.CharField(max_length=200)


    def __str__(self):
        return str(self.name)

class CarModel(models.Model):
    carmake=models.ForeignKey(CarMake,on_delete=models.CASCADE)
    dealerId=models.IntegerField()
    type=models.CharField(max_length=200)
    year=models.DateField()
    def __str__(self):
        return str(self.carmake)



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

    def __init__(self=None,
                 address=None,
                 city=None,
                 full_name=None,
                 id=None,
                 lat=None,
                 long=None,
                 short_name=None,
                 st=None,
                 zip=None,
                 state=None):
        self.id=id
        self.full_name=full_name
        self.city=city
        self.address=address      
        self.lat=lat
        self.long=long
        self.short_name=short_name
        self.st=st
        self.zip=zip
        self.state=state
        self.important_fields_names=['id','full_name','city','address','zip','st']



    def __str__(self):
        return f"Dealer name:  { self.full_name}"    

    def get_fields(self):
        return vars(self)
    
    def get_frontend_fieldnames(self):
        return {k: v for k,v in vars(self).items() if k in self.important_fields_names}

# <HINT> Create a plain Python class `DealerReview` to hold review data

class DealerReview:

    def __init__(self=None,
                 dealership=None,
                 name=None,
                 purchase=None,
                 review=None,
                 purchase_date=None,
                 car_make=None,
                 car_model=None,
                 car_year=None,
                 sentiment=None,
                 id=None):
        self.dealership=dealership
        self.name=name
        self.purchase=purchase
        self.review=review 
        self.purchase_date=purchase_date
        self.car_make=car_make
        self.car_model=car_model
        self.car_year=car_year 
        self.sentiment=sentiment
        self.id=id 
        self.important_fields_names=['id','name','dealership','purchase','review','sentiment','purchase_date','car_make']


    def __str__(self):
        return f"Reviewer name: {self.name}"
    

    def get_fields(self):
        return vars(self)
    
    def get_frontend_fieldnames(self):
        return {k: v for k,v in vars(self).items() if k in self.important_fields_names}




