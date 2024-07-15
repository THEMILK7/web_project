from django.shortcuts import render ,redirect, get_object_or_404
from .models import Quiz
from django.views.generic import ListView 
from questions.models import Question,Answer
from results.models import Result
from django.http import JsonResponse
from .forms import QuizForm
from django.contrib import messages
# Create your views here.

def quiz_detail(request, pk):
    quiz = get_object_or_404(Quiz, pk=pk)
    return render(request, 'quizes/quiz_detail.html', {'obj': quiz})


def quizzes_list(request):
    quizzes = Quiz.objects.all()  # Récupérer tous les quizzes depuis la base de données
    return render(request, 'quizzes_list.html', {'quizzes': quizzes})


class QuizListView(ListView):
    model = Quiz
    template_name = 'quizes/index.html'
    context_object_name = 'quizzes'


def quiz_view(request, id):
    quiz = get_object_or_404(Quiz, pk=id)
    return render(request, 'quizes/quiz.html', {'obj': quiz})




"""def quiz_view(request, pk):
    quiz = Quiz.objects.get(pk=pk)
    return render(request, 'quizes/quiz.html', {'obj': quiz})"""


def quiz_data_view(request, pk):
    quiz = Quiz.objects.get(pk=pk)
    questions = []
    for q in quiz.get_questions():
        answers = []
        for a in q.get_answers():
           answers.append(a.text)
        questions.append({str(q): answers})
    return JsonResponse({
        'data': questions,
        'time': quiz.time
    })

def save_quiz_view(request, pk):
   #print(request.POST)
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        questions = []
        data = request.POST
        data_ = dict(data.lists())
        data_.pop('csrfmiddlewaretoken')

        for k in data_.keys():
            print('key: ', k)
            question = Question.objects.get(text=k)
            questions.append(question)
        print(questions)

        user = request.user
        quiz = Quiz.objects.get(pk=pk)

        score = 0
        multiplier = 100 / quiz.number_of_questions
        results = []
        correct_answer = None

        for q in questions:
            a_selected = request.POST.get(q.text)
            
            if a_selected != "":
                question_answers = Answer.objects.filter(question=q)
                for a in question_answers:
                    if a_selected == a.text:
                        if a.correct:
                            score += 1
                            correct_answer = a.text
                    else:
                        if a.correct:
                            correct_answer = a.text

                results.append({str(q): {'correct_answer': correct_answer, 'answered': a_selected }})
            else: 
                results.append({str(q): 'not answered'})
        
        score_ = score * multiplier
        Result.objects.create(quiz=quiz, user=user, score = score) 

    return JsonResponse({'score': score_, 'results': results })


def add_quiz(request):
    if request.method == 'POST':
        form = QuizForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Quiz ajouté avec succès.')
            return redirect('prof_dashboard')
    else:
        form = QuizForm()
    return render(request, 'prof/add_quiz.html', {'form': form})
