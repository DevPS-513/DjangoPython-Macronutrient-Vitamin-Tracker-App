from django import forms 
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import CarModel,Person

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30,required=True)
    last_name = forms.CharField(max_length=30,required=True)

    class Meta:
        model=User
        fields=['username','email','first_name','last_name',
                'password1','password2']
        

class ReviewForm(forms.Form):
    name =          forms.CharField(max_length=30,required=True)
    id =            forms.CharField(max_length=30,required=True)
    content =       forms.CharField(widget=forms.Textarea,required=True)
    purchasecheck = forms.BooleanField(required=True)
    purchase_date = forms.CharField(max_length=50,required=True)

    car = forms.ModelChoiceField(queryset=CarModel.objects.all(), required=True)
    dealership=forms.CharField(max_length=50,required=True)


class PersonForm(forms.ModelForm):
    class Meta:
        model =  Person
        fields = ['gender','age','weight_lbs','height_in','activity_level','bf']
        widgets = {
            'weight_lbs': forms.NumberInput(attrs={'class': 'w-25'}),
        }