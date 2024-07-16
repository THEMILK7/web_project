"""
URL configuration for miniapp project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from users.views import ProfLoginView
#from django.urls import include
from django.urls import path, include
from django.urls import path
from posts.views import prof_dashboard, add_course, delete_course,about_us
from posts import views
from quizes.views import add_quiz
from questions.views import add_question,add_answer
from subscriptions.views import choose_subscription, initiate_payment,payment_callback,payment_failed,subscription_success,subscription_success1,select_course
#from django.urls import path
from allauth.account import views as allauth_views
from quizes.views import quiz_view,quiz_data_view,quiz_detail,quizzes_list,save_quiz_view,QuizListView
from results.views import results_list
urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/login/', allauth_views.LoginView.as_view(), name='account_login'),  # Exemple de chemin direct pour la vue de login
    path('accounts/signup/', allauth_views.SignupView.as_view(), name='account_signup'),  # Exemple de chemin direct pour la vue de sig
    path('accounts/logout', allauth_views.LogoutView.as_view(), name='account_logout'),
    path('accounts/', include('allauth.urls')),
    path('accounts/prof/login/', ProfLoginView.as_view(), name='prof_login'),
    path('prof/dashboard/', prof_dashboard, name='prof_dashboard'),
    path('prof/add_course/', add_course, name='add_course'),
    path('prof/add_quiz/', add_quiz, name='add_quiz'),
    path('prof/add_question/', add_question, name='add_question'),
    path('prof/add_answer/', add_answer, name='add_answer'),
    path('prof/delete_course/', delete_course, name='delete_course'),
    #path('accounts/', include('allauth.urls')),
    path('classe/<int:classe_id>/', views.classe_detail, name='classe_detail'),
    path('matiere/<int:matiere_id>/', views.matiere_detail, name='matiere_detail'),
    path('chapitre/<int:chapitre_id>/', views.chapitre_detail, name='chapitre_detail'),
    path('cours/<int:cours_id>/', views.cours_detail, name='cours_detail'),
    path('choose/<int:cours_id>/', choose_subscription, name='choose_subscription'),
    path('initiate_payment/<int:subscription_id>/', initiate_payment, name='initiate_payment'),
    path('payment_callback/<str:invoice_token>/', payment_callback, name='payment_callback'),
    path('payment_failed/', payment_failed, name='payment_failed'),
    path('subscription_success/', subscription_success, name='subscription_success'),
    path('subscription_success1/', subscription_success1, name='subscription_success1'),
    path('', views.home, name='home'),
    path('about_us/', about_us, name='about_us'),# Ajout de la vue d'accueil
    path('courses/', views.courses, name='courses'),
    path('select_course/', select_course, name='select_course'),# Ajout de la vue d'accueil
    path('',include("quizes.urls")),
    path('',include("results.urls")),
    path('quiz/<int:id>/', quiz_view, name='quiz_view')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
