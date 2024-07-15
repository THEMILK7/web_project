# users/urls.py
from django.urls import path
from .views import ProfLoginView

urlpatterns = [
    path('prof-login/', ProfLoginView.as_view(), name='prof_login'),
]
