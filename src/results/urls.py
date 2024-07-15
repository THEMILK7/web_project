from django.urls import path
from .views import results_list

urlpatterns = [
    path('results/', results_list, name='results-list'),
]
