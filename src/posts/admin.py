from django.contrib import admin
from posts.models import Auteur, Classe, Cours, Matiere, Chapitre

class CoursAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "published", "create_on", "last_update", "classe", "matiere", "chapitre","quiz" , "author",'pdf', 'video')
    list_editable = ("published","video","quiz")
    list_filter = ("classe", "matiere", "chapitre", "author")

admin.site.register(Cours, CoursAdmin)

class MatiereAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "display_classes")
    list_filter = ("classe",)
    filter_horizontal = ('classe',)  # Ajoute des cases à cocher pour sélectionner plusieurs classes

    def display_classes(self, obj):
        return ", ".join(classe.name for classe in obj.classe.all())
    display_classes.short_description = 'Classes'

admin.site.register(Matiere, MatiereAdmin)

class ClasseAdmin(admin.ModelAdmin):
    list_display = ("id", "name",)


admin.site.register(Classe, ClasseAdmin)

class AuteurAdmin(admin.ModelAdmin):
    list_display = ("name", "prenom", "email",)
    list_editable = ("email",)

admin.site.register(Auteur, AuteurAdmin)

class ChapitreAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "classe", "matiere","last_update",)
    list_filter = ("classe", "matiere",)

admin.site.register(Chapitre, ChapitreAdmin)



