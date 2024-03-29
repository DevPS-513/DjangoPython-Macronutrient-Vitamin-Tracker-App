from django import forms 
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Person,Food,Day,Meal

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30,required=True)
    last_name = forms.CharField(max_length=30,required=True)

    class Meta:
        model=User
        fields=['username','email','first_name','last_name',
                'password1','password2']
       

class PersonForm(forms.ModelForm):
    class Meta:
        model =  Person
        fields = ['gender','age','weight_lbs','height_ft','height_in','activity_level','bf']
        widgets = {
            'weight_lbs': forms.NumberInput(attrs={'style': 'height: 30px;'}),
        }

class FoodForm(forms.ModelForm):
    
    description = forms.ModelChoiceField(queryset=Food.objects.all(), empty_label="Select a food")

    class Meta:
        model = Food
        fields = ['description']




#DayFormSet = forms.inlineformset_factory(Day, Food, form=DayForm, extra=1)