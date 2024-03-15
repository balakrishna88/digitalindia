from django import forms
from django_summernote.widgets import SummernoteWidget
from .models import EducationPost

class EducationPostForm(forms.ModelForm):
    class Meta:
        model = EducationPost
        fields = ['title', 'category', 'subcategory', 'content']
        widgets = {
            'content': SummernoteWidget(),  # Use SummernoteWidget for the content field
        }
