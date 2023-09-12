from django.forms.models import ModelForm
from django import forms
from django.contrib.auth.models import User
from django_registration.forms import RegistrationFormUniqueEmail

class UserChangeForm(ModelForm):
    first_name = forms.CharField(max_length=25,required=True)
    last_name = forms.CharField(max_length=25,required=True)
    class Meta:
        model = User
        fields = ['first_name', 'last_name'] #т.е. берем только 2 поля из БД User, остальные не трогаем
