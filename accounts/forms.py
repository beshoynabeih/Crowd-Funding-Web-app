from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
import re
from project.models import Project, Denote
from django_countries.data import COUNTRIES
from django_countries.widgets import CountrySelectWidget

from django.forms import DateInput


class SignUpForm(UserCreationForm):
    email=forms.EmailField()
    phone =  forms.RegexField(label='Phone', regex=r'^\+?1?\d{9,15}$')
    img = forms.ImageField(label='Profile image', required=False,)

    class Meta:
        model = User
        fields = {'username', 'password1', 'password2' , 'first_name', 'last_name', 'email', 'phone', 'img'}


class UserForm(forms.ModelForm):
    # birthdate=forms.DateField()
    birthdate = forms.CharField()
    facebook_profile = forms.EmailField()
    phone = forms.CharField(max_length=11)
    country = forms.ChoiceField(choices=sorted(COUNTRIES.items()))

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'phone',
                  'birthdate', 'country', 'facebook_profile']
        widgets = {
            'country': CountrySelectWidget(),
            # 'birthdate': DateInput(attrs={'type': 'date'}),
        }


# 'birthday': forms.TextInput(attrs={'class': 'datepicker'})
#  user = models.ForeignKey(User, on_delete=models.CASCADE)
#     title = models.CharField(max_length=70)
#     details = models.TextField()
#     category = models.ForeignKey(Category, on_delete=models.CASCADE)
#     total_target = models.DecimalField(max_digits=10, decimal_places=2)
#     start_date = models.DateField()
#     end_date = models.DateField()

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'details', 'total_target', 'start_date', 'end_date']

        # fields=['title','details','total_target','start_date','end_date']
        widgets = {
            'start_date': DateInput(attrs={'type': 'date'}),
            'end_date': DateInput(attrs={'type': 'date'}),
        }


class DenoteForm(forms.ModelForm):
    class Meta:
        model = Denote
        # fields=['project','amount']
        fields = ['amount']