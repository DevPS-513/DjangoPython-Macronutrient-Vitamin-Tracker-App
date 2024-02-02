from django import template
register = template.Library()

@register.filter
def get_nutrient(food, nutrient_name):
    nutrient_name = nutrient_name.lower()
    for nutrient in food.foodnutrient_set.all():
        if nutrient_name in str(nutrient.nutrient.name).lower():
            return nutrient.amount
    return 0
