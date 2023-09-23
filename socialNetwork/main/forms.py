from django.forms.models import ModelForm
from django import forms
from django.contrib.auth.models import User
from .models import News
from django.contrib.auth import get_user_model
from django_registration.forms import RegistrationForm
CustomUser = get_user_model()

class CustomCreationForm(RegistrationForm):
    class Meta(RegistrationForm.Meta):
        model = CustomUser
class UserChangeForm(ModelForm):
    first_name = forms.CharField(max_length=25,required=True, widget=forms.TextInput(attrs={'placeholder': 'Иван','class': 'form-input'}), label='Имя')
    last_name = forms.CharField(max_length=25,required=True,widget=forms.TextInput(attrs={'placeholder': 'Иванов','class': 'form-input'}),label='Фамилия')
    residence = forms.CharField(max_length=20, required=False, widget=forms.TextInput(attrs={'id': 'residence', 'placeholder': 'Москва', 'list': 'residence-help', 'class' : 'form-input'}),label='Место проживания')
    about = forms.CharField(max_length=150, required=False, widget=forms.Textarea(attrs={'placeholder': 'Расскажи о себе...', 'class': 'form-area'}),label='')
    birthday = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-input'}), label='Дата рождения')
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'about', 'birthday', 'residence'] #т.е. берем только 2 поля из БД User, остальные не трогаем

class UserNewsForm(ModelForm):
    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(UserNewsForm, self).__init__(*args, **kwargs) # вызываем init родительского класса
    news = forms.CharField(max_length=500, required=True, widget=forms.Textarea(attrs={'placeholder': 'Добавьте новость...', 'class': 'form-area', 'style': 'height: 120px;'}), label='')
    class Meta:
        model = News
        fields = ['news',]

    def save(self, commit=True):
        news = super(UserNewsForm, self).save(commit=False)
        news.user = self.user
        if commit:
            news.save()
        return news

class UserAvatarForm(ModelForm):
    avatar = forms.ImageField(
        widget=forms.ClearableFileInput(
            attrs={'class': 'avatar'},
        )
    )
    class Meta:
        model = CustomUser
        fields = ['avatar']


