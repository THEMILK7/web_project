from django.contrib import admin
from django.contrib import admin
from .models import Profile_Etudiant, Profile_Professeur

# Register your models here.
class Profile_EtudiantAdmin(admin.ModelAdmin):
    list_display = ('user', 'nom', 'prenom', 'phone', 'level')
    search_fields = ('user__username', 'nom', 'prenom', 'phone')
    list_filter = ('level',)

admin.site.register(Profile_Etudiant, Profile_EtudiantAdmin)

class Profile_ProfesseurAdmin(admin.ModelAdmin):
    list_display = ('user', 'nom', 'prenom', 'specialite','teacher_id')
    search_fields = ('user__username', 'nom', 'prenom', 'specialite','teacher_id')
    list_filter = ('specialite',)

admin.site.register(Profile_Professeur, Profile_ProfesseurAdmin)