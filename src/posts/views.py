from django.shortcuts import render

# Create your views here.
# views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from users.models import Profile_Etudiant
from posts.models import Classe
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Cours
from .forms import CourseForm, CourseDeleteForm
from .decorators import require_teacher_login
from django.shortcuts import render, get_object_or_404
from .models import Chapitre, Cours
from django.shortcuts import render, get_object_or_404
from .models import Classe
from .models import Matiere
import os
import random
from subscriptions.decorators import subscription_required


def get_random_image0(subject):
    base_dir = 'static/images/'
    subject_dir = os.path.join(base_dir, subject)
    if os.path.exists(subject_dir) and os.listdir(subject_dir):
        return random.choice(os.listdir(subject_dir))
    return None

def get_random_image1(subject, chapter):
    base_dir = 'static/images/'
    subject_dir = os.path.join(base_dir, subject.lower())
    chapter_dir = os.path.join(subject_dir, chapter)
    if os.path.exists(chapter_dir) and os.listdir(chapter_dir):
        return random.choice(os.listdir(chapter_dir))
    return None
def classe_detail(request, classe_id):
    classe = get_object_or_404(Classe, pk=classe_id)
    matieres = classe.matieres.all()

    matieres_with_images = []
    for matiere in matieres:
        image_url = get_random_image0(matiere.name.lower())
        matieres_with_images.append({
            'name': matiere.name,
            'image_url': image_url
        })

    return render(request, 'classe/classe_detail.html', {'classe': classe, 'matieres': matieres,'matieres_with_images': matieres_with_images})
def matiere_detail(request, matiere_id):
    matiere = get_object_or_404(Matiere, id=matiere_id)
    chapitres = matiere.chapitre_set.all()  # Récupère tous les chapitres associés à la matière

    chapitres_with_images = []
    for chapitre in chapitres:
        image_url = get_random_image1(matiere.name, chapitre.title)
        chapitres_with_images.append({
            'chapitre': chapitre,
            'image_url': image_url
        })

    context = {
        'matiere': matiere,
        'chapitres_list': chapitres,
        'chapitres_with_images': chapitres_with_images,}

    return render(request, 'matiere/matiere_detail.html', {'matiere': matiere, 'chapitres_list': chapitres,'chapitres_with_images': chapitres_with_images,})

def chapitre_detail(request, chapitre_id):
    chapitre = get_object_or_404(Chapitre, pk=chapitre_id)
    cours_list = Cours.objects.filter(chapitre=chapitre)
    context = {'chapitre': chapitre, 'cours_list': cours_list}
    return render(request, 'chapitre/chapitre_detail.html', {'chapitre': chapitre, 'cours_list': cours_list})
@subscription_required
def cours_detail(request, cours_id):
    cours = get_object_or_404(Cours, pk=cours_id)
    quiz_id = cours.quiz_id if cours.quiz else None
    return render(request, 'cours/cours_detail.html', {'cours': cours, 'quiz_id':quiz_id})

@require_teacher_login

def prof_dashboard(request):
    courses = Cours.objects.filter(author=request.user)
    return render(request, 'prof/prof_dashboard.html', {'courses': courses})

@require_teacher_login
def add_course(request):
    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES)
        if form.is_valid():
            course = form.save(commit=False)
            course.author = request.user
            course.save()
            messages.success(request, 'Cours ajouté avec succès.')
            return redirect('prof_dashboard')
    else:
        form = CourseForm()
    return render(request, 'prof/add_course.html', {'form': form})

@require_teacher_login
def delete_course(request):
    if request.method == 'POST':
        form = CourseDeleteForm(request.POST)
        if form.is_valid():
            course_id = form.cleaned_data['course_id']
            course = get_object_or_404(Cours, id=course_id, author=request.user)
            course.delete()
            messages.success(request, 'Cours supprimé avec succès.')
            return redirect('prof_dashboard')
    return redirect('prof_dashboard')



#@login_required
def home(request):
    if request.user.is_authenticated:
        try:
            #etudiant = Profile_Etudiant.objects.get(user=request.user)
            # Récupérer l'ID de la classe en fonction du nom de l'étudiant
            #classe = get_object_or_404(Classe, name=etudiant.level)
            #return redirect('classe_detail', classe_id=classe.id)
            return render(request, 'home/home.html')
        except Profile_Etudiant.DoesNotExist:
            return render(request, 'home/home.html', {'message': 'Profile étudiant introuvable'})
    else:
        return render(request, 'home/home.html')
@login_required
def courses(request):
    if request.user.is_authenticated:
        try:
            etudiant = Profile_Etudiant.objects.get(user=request.user)
            # Récupérer l'ID de la classe en fonction du nom de l'étudiant
            classe = get_object_or_404(Classe, name=etudiant.level)
            return redirect('classe_detail', classe_id=classe.id)
        except Profile_Etudiant.DoesNotExist:
            return render(request, 'home/home.html', {'message': 'Profile étudiant introuvable'})
    else:
        print("okkk")
        return render(request, 'home/home.html')

# Ajoutez d'autres vues ici si nécessaire


