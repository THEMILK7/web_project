from django.db import models
import random
# Create your models here.

class Quiz(models.Model):
    name =  models.CharField(max_length=120)
    topic = models.CharField(max_length=120)
    number_of_questions = models.IntegerField()
    time = models.IntegerField(help_text="nombre de minutes maximal pour remplir le quiz")

    def __str__(self) :
        return f"{self.name}-{self.topic}"
    
    def get_questions(self):
       questions = list(self.question_set.all())
       random.shuffle(questions)
       return questions[:min(self.number_of_questions, len(questions))]
    
    class Meta:
        verbose_name_plural = "Evaluation"