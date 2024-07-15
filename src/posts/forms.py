from django import forms
from .models import Cours

class CourseForm(forms.ModelForm):
    class Meta:
        model = Cours
        fields = ['title', 'slug', 'matiere', 'classe', 'chapitre', 'content', 'pdf', 'video', 'published']

class CourseDeleteForm(forms.Form):
    course_id = forms.IntegerField(widget=forms.HiddenInput)

