from django.db import models
from django.contrib.auth.models import User
import uuid
from django.contrib.auth.models import AbstractUser
class Profile_Etudiant(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nom = models.CharField(max_length=30)
    prenom = models.CharField(max_length=30)
    phone = models.CharField(max_length=15, unique=True)
    level = models.CharField(max_length=10)
    pass

    def __str__(self):
        return f'{self.nom} {self.prenom}'

def generate_teacher_id():
    return str(uuid.uuid4().int)[:16]  # Génère un identifiant unique de 16 chiffres
class Profile_Professeur(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nom = models.CharField(max_length=30)
    prenom = models.CharField(max_length=30)
    specialite = models.CharField(max_length=10)
    teacher_id = models.CharField(max_length=36, unique=True, editable=False, null=True)

    def save(self, *args, **kwargs):
        if not self.teacher_id:
            self.teacher_id = generate_teacher_id()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.nom} {self.prenom}"