from django.contrib import admin
from .models import CarMake,CarModel


# CarModelInline class
class CarModelInline(admin.StackedInline):
    model = CarModel
    extra = 3  # how many rows to show


# CarModelAdmin class
class CarModelAdmin(admin.ModelAdmin):
    list_display = ('make', 'dealerId', 'type', 'year')  # fields to display in list view
    search_fields = ('make', 'dealerId', 'type', 'year') # fields to search in search box

# CarMakeAdmin class with CarModelInline
class CarMakeAdmin(admin.ModelAdmin):
    inlines = [CarModelInline]
# Register models here
admin.site.register(CarModel, CarModelAdmin)
admin.site.register(CarMake, CarMakeAdmin)
