from django.contrib import admin
from .models import Result
# Register your models here.


class ResultAdmin(admin.ModelAdmin):
    list_display = ('user', 'quiz', 'score')  # Colonnes à afficher dans la liste d'admin
    list_filter = ('quiz', 'user')  # Filtres pour simplifier la recherche
    search_fields = ('user__username', 'quiz__name')  # Champs de recherche
    ordering = ('-score',)  # Trier par score décroissant
    list_per_page = 25  # Nombre de résultats par page

admin.site.register(Result, ResultAdmin)

