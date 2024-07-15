from django import forms
from .models import Subscription
from posts.models import Cours
class SubscriptionForm(forms.ModelForm):
    class Meta:
        model = Subscription
        fields = ['plan']


class CourseSelectionForm(forms.Form):
    course = forms.ModelChoiceField(queryset=Cours.objects.all(), label="Sélectionnez un cours")
