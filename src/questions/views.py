from django.shortcuts import render
from .forms import AnswerForm,QuestionForm
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from .models import Question,Answer
# Create your views here.

def add_question(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Question ajoutée avec succès.')
            return redirect('prof_dashboard')
    else:
        form = QuestionForm()
    return render(request, 'prof/add_question.html', {'form': form})

# Ajouter une réponse
def add_answer(request):
    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Réponse ajoutée avec succès.')
            return redirect('prof_dashboard')
    else:
        form = AnswerForm()
    return render(request, 'prof/add_answer.html', {'form': form})