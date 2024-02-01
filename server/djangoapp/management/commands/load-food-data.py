from django.core.management.base import BaseCommand
from djangoapp.models import Food, Meal ,FoodNutrient
from django.conf import settings
import json as json
import os

print(settings.BASE_DIR)
class Command(BaseCommand):
    help = 'Loads food data from JSON file into database'

    def handle(self, *args, **options):
        path_to_food_db = os.path.join(settings.BASE_DIR, r'djangoapp\static\all_simplified_entries2.json')
        food_db=json.load(open(path_to_food_db, 'r'))

        for f,food in enumerate(food_db):

            food_obj, created = Food.objects.get_or_create(description=food["description"])
            print("food..",food["description"],"..get_or_create..",created)

            for n,foodnutrient in enumerate(food["foodNutrients"]):

     
                try:
                    foodnutrient["name"]=foodnutrient["nutrient"]["name"]
                    foodnutrient["unitname"]=foodnutrient["nutrient"]["unitName"]
                    
                except:
                    foodnutrient["name"]=None
                    foodnutrient["unitname"]=None             

                # remove any fields not in the model
                dummy=FoodNutrient()
                field_names = [f.name for f in dummy._meta.get_fields()]
                delete_list=[]

                # first remove any fields we do not need
                for name1 in foodnutrient.keys():
                    if name1 not in field_names:
                        delete_list.append(name1)

                # now 
                
                for name1 in delete_list:
                    del foodnutrient[name1]
                food_nutrient_obj, created = FoodNutrient.objects.get_or_create(**foodnutrient)
                
                food_nutrient_obj.save()
                food_obj.foodNutrients.add(food_nutrient_obj)  
                                   
            
            try:
                food_obj.shortname=food_obj.description.split(',')[0]
            except:
                food_obj.shortname=food_obj.description
            food_obj.save()

