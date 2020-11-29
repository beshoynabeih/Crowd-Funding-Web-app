from django import forms
# from .models import UserProfile
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
import re
from project.models import Project, Denote
from django_countries.data import COUNTRIES
from django_countries.widgets import CountrySelectWidget

from django.forms import DateInput


# from django.contrib.auth.models import User
from .models import MyUser

class UserProfile(UserCreationForm):
    email = forms.EmailField(required=True)
    class Meta:
        model = MyUser
        fields = ('first_name', 'last_name', 'email', "password1", "password2", 'avatar', 'phone', 'date_of_birth')

    # def save(self, commit=True):
    #     user = super(UserCreationForm, self).save(commit=False)
    #     user.email = self.cleaned_data["email"]
    #     if commit:
    #         user.save()
    #     return user


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


class UserForm(forms.ModelForm):
    # birthdate=forms.DateField()
    date_of_birth = forms.CharField()
    facebook_profile = forms.URLField(max_length=150)
    phone = forms.CharField(max_length=11)
    country = forms.ChoiceField(choices=sorted(COUNTRIES.items()))

    class Meta:
        model = MyUser
        fields = ['first_name', 'last_name', 'phone',
                  'date_of_birth', 'country', 'facebook_profile']
        widgets = {
            'country': CountrySelectWidget(),
            # 'birthdate': DateInput(attrs={'type': 'date'}),
        }


class DenoteForm(forms.ModelForm):
    class Meta:
        model = Denote
        # fields=['project','amount']
        fields = ['amount']