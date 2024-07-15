from django import forms
from allauth.account.forms import SignupForm
from .models import Profile_Etudiant
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm
from allauth.account.forms import LoginForm
from .models import Profile_Professeur

class CustomSignupForm(SignupForm):
    nom = forms.CharField(max_length=30, label='Nom')
    prenom = forms.CharField(max_length=30, label='Prénom')
    phone = forms.CharField(max_length=15, label='Numéro de Téléphone')
    level = forms.CharField(max_length=50, label='Niveau d\'Étude')

    def save(self, request):
        user = super(CustomSignupForm, self).save(request)
        # Créer un profil étudiant associé à l'utilisateur
        Profile_Etudiant.objects.create(
            user=user,
            nom=self.cleaned_data['nom'],
            prenom=self.cleaned_data['prenom'],
            phone=self.cleaned_data['phone'],
            level=self.cleaned_data['level']
        )
        return user
# forms.py

# users/forms.py

class ProfLoginForm(AuthenticationForm):
    teacher_id = forms.CharField(max_length=36, label="Teacher ID")



# forms.py


