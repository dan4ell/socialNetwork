from django.forms.models import ModelForm
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django_registration.forms import RegistrationForm
CustomUser = get_user_model()

class CustomCreationForm(RegistrationForm):
    class Meta(RegistrationForm.Meta):
        model = CustomUser
class UserChangeForm(ModelForm):
    first_name = forms.CharField(max_length=25,required=True)
    last_name = forms.CharField(max_length=25,required=True)
    about = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Расскажи о себе...'}))
    birthday = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'about', 'birthday'] #т.е. берем только 2 поля из БД User, остальные не трогаем
