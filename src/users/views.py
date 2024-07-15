from django.shortcuts import render

# Create your views here.
# users/views.py
# users/views.py
from allauth.account.models import EmailConfirmationHMAC
from allauth.account.utils import send_email_confirmation
from django.template.loader import render_to_string
from django.utils.crypto import get_random_string
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.urls import reverse
from allauth.account.views import LoginView
from .forms import ProfLoginForm
from django.shortcuts import render
from allauth.account.views import LoginView
from .forms import ProfLoginForm
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.views.generic import FormView

class ProfLoginView(LoginView):
    form_class = ProfLoginForm
    template_name = 'accounts/prof_login.html'  # Chemin vers votre template prof_login.html
    success_url = reverse_lazy('prof_dashboard')
    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        teacher_id = form.cleaned_data['teacher_id']
        user = authenticate(self.request, username=username, password=password)

        if user is not None and user.profile_professeur.teacher_id == teacher_id:
            login(self.request, user)
            return redirect('home')  # Redirige vers le tableau de bord des professeurs
        else:
            # Gestion de l'échec de l'authentification
            return render(self.request, self.template_name, {'form': form, 'message': "Invalid credentials"})

    def form_invalid(self, form):
        # Afficher les erreurs de formulaire directement dans le HTML
        return render(self.request, self.template_name, {'form': form, 'message': 'Informations de connexion incorrectes.'})



