from django.core.management.base import BaseCommand
from djangoapp.models import Food, Meal ,FoodNutrient,Nutrient
from django.conf import settings
import json as json
import os

print(settings.BASE_DIR)
class Command(BaseCommand):
    help = 'Loads food data from JSON file into database'

    def handle(self, *args, **options):
        path_to_food_db = os.path.join(settings.BASE_DIR, r'djangoapp\static\all_simplified_entries.json')
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

                # remove any fields from food nutrient that is not in the model
                # 
                dummy1=FoodNutrient()
                field_names1 = [f.name for f in dummy1._meta.get_fields()]
                dummy2=Nutrient()
                field_names2 = [f.name for f in dummy2._meta.get_fields()]

                # any fields not present in the nutrient, or the nutrient amount, dont use. 
                field_names=list(field_names1)+list(field_names2)

                delete_list1=[] # to delete from foodnutrient
                delete_list2=[] # to delete from nutrient
                # first remove any fields we do not need
                for name1 in foodnutrient.keys():
                    if name1 not in field_names1:
                        delete_list1.append(name1)

                for name2 in foodnutrient["nutrient"].keys():
                    if name2 not in field_names2:
                        delete_list2.append(name2)

                # now add any nutrients that does not currently exist.
                
                for name1 in delete_list1:
                    del foodnutrient[name1]

                for name2 in delete_list2:
                    del foodnutrient["nutrient"][name2]

                nutrient_obj, created = Nutrient.objects.get_or_create(**foodnutrient["nutrient"])

                del foodnutrient["nutrient"]

                food_nutrient_obj, created = FoodNutrient.objects.get_or_create(**foodnutrient,nutrient=nutrient_obj,food=food_obj)

                # now add the amount and unit

                food_obj.amount=food["foodPortions"]["amount"]
                food_obj.unitName=food["foodPortions"]["unitname"]
                food_obj.calories=food["foodPortions"]["kcal"]
                food_obj.save()
                

            food_obj.save()

