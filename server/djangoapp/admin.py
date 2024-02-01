from django.contrib import admin

# Register your models here.
from .models import Food, Meal, FoodNutrient, Person

# Make it so that when adding a meal I can also Add foods to it
class FoodInLine(admin.TabularInline):
    model = Meal.foods.through

class MealAdmin(admin.ModelAdmin):
    inlines = [
        FoodInLine,
    ]

    def display_foods(self,obj):
        return ",".join([food.description for food in obj.foods.all()]) 
    display_foods.short_description = 'Foods in Meal'

admin.site.register(Food)
admin.site.register(Meal, MealAdmin)
admin.site.register(FoodNutrient)
admin.site.register(Person)


