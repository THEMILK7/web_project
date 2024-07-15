from django.contrib.auth import get_user_model
from django.db import models
from django.template.defaultfilters import slugify
from quizes.models import Quiz
User = get_user_model()
# Create your models here.

class Classe(models.Model):
    name =  models.CharField(max_length=255)
    def __str__(self):
        return self.name

class Matiere(models.Model):
    name = models.CharField(max_length=255, unique=True)
    #classe = models.ForeignKey(Classe, on_delete=models.CASCADE)
    classe = models.ManyToManyField(Classe, related_name="matieres")

    def __str__(self):
        return f"{self.name} ({self.classe.name})"

class Chapitre(models.Model):
    #title = models.CharField(max_length=255, unique=True)
    #matiere = models.ForeignKey(Matiere, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, unique=True)
    matiere = models.ForeignKey(Matiere, on_delete=models.CASCADE)
    classe = models.ForeignKey(Classe, on_delete=models.CASCADE)
    last_update = models.DateField(auto_now=True)
    def __str__(self):
        return self.title
class Auteur(models.Model):
    name = models.CharField(max_length=255)
    prenom = models.CharField(max_length=255)
    email = models.EmailField(unique=True)

    def __str__(self):
        return f"{self.name} {self.prenom}"

class Cours(models.Model):
    title = models.CharField(max_length=255,unique=True, verbose_name="Titre")
    slug = models.SlugField(max_length=255, unique=True,blank=True)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True,blank=True)
    matiere = models.ForeignKey(Matiere, on_delete=models.CASCADE)
    classe = models.ForeignKey(Classe, on_delete=models.CASCADE)
    chapitre = models.ForeignKey(Chapitre, on_delete=models.CASCADE, null=True, blank=True)
    quiz=models.ForeignKey(Quiz, on_delete=models.CASCADE, null=True, blank=True)
    last_update = models.DateTimeField(auto_now=True)
    create_on = models.DateField(blank=True,null=True,verbose_name="date de creation")
    published = models.BooleanField(default=False, verbose_name="publié")
    content = models.TextField(blank=True, verbose_name="contenu")
    pdf = models.FileField(upload_to='media/pdfs/', blank=True, null=True)
    video = models.FileField(upload_to='media/video/', blank=True, null=True)

    class Meta:
        ordering = ['-create_on']
        verbose_name = "Cours"
    def __str__(self):
        return self.title
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)

        super().save(*args, **kwargs)