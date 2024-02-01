from django.contrib import admin

# Register your models here.
from .models import Food, Meal, FoodNutrient, Person

admin.site.register(Food)
admin.site.register(Meal)
admin.site.register(FoodNutrient)
admin.site.register(Person)


