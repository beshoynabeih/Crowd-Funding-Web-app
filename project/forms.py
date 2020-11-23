from django import forms
from project.models import Project, ProjectPicture
from django.forms.widgets import DateInput
from django.core.files.images import get_image_dimensions
from project.models import UserProfile

class ProjectForm(forms.ModelForm):
    images = forms.ImageField(widget=forms.FileInput(attrs={'multiple': True}), required=False)
    
    class Meta:
        model = Project
        fields = ['title', 'details', 'total_target', 'start_date', 'end_date', 'tags', 'category']
        widgets = {
            'start_date': DateInput(attrs={'type': 'date'}),
            'end_date': DateInput(attrs={'type': 'date'})
        }

    class UserProfileForm(forms.ModelForm):
      class Meta:
        model = UserProfile

      def clean_avatar(self):
        avatar = self.cleaned_data['avatar']

        try:
            w, h = get_image_dimensions(avatar)

            #validate dimensions
            max_width = max_height = 100
            if w > max_width or h > max_height:
                raise forms.ValidationError(
                    u'Please use an image that is '
                     '%s x %s pixels or smaller.' % (max_width, max_height))

            #validate content type
            main, sub = avatar.content_type.split('/')
            if not (main == 'image' and sub in ['jpeg', 'pjpeg', 'gif', 'png']):
                raise forms.ValidationError(u'Please use a JPEG, '
                    'GIF or PNG image.')

            #validate file size
            if len(avatar) > (20 * 1024):
                raise forms.ValidationError(
                    u'Avatar file size may not exceed 20k.')

        except AttributeError:
            """
            Handles case when we are updating the user profile
            and do not supply a new avatar
            """
            pass

        return avatar
