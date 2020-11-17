from django import forms
from project.models import Project, ProjectPicture
from django.forms.widgets import DateInput

class ProjectForm(forms.ModelForm):
    images = forms.ImageField(widget=forms.FileInput(attrs={'multiple': True}), required=False)
    
    class Meta:
        model = Project
        fields = ['title', 'details', 'total_target', 'start_date', 'end_date', 'tags', 'category']
        widgets = {
            'start_date': DateInput(attrs={'type': 'date'}),
            'end_date': DateInput(attrs={'type': 'date'}),
        }
