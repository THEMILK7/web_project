from django.urls import path
from .views import QuizListView,quiz_view,quiz_data_view,save_quiz_view, quizzes_list, quiz_detail
from results.views import results_list

app_name = 'quizes'

urlpatterns = [
    path('devoirs/', QuizListView.as_view(), name="quiz-index"),
    path('quiz/<int:id>/',quiz_view, name="quiz_view"),
    path('<pk>/data/',quiz_data_view, name="quiz-data-view"),
    path('<pk>/save/',save_quiz_view, name="save-view"),
    path('result/results/', results_list, name='results-list'),
    path('quiz/<int:pk>/', quiz_detail, name='quiz_detail'),

]


