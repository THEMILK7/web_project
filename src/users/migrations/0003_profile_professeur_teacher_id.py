# Generated by Django 5.0.6 on 2024-07-05 12:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_rename_profile_profile_etudiant_profile_professeur'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile_professeur',
            name='teacher_id',
            field=models.CharField(editable=False, max_length=36, null=True, unique=True),
        ),
    ]
