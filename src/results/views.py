from django.shortcuts import render
from itertools import groupby
from .models import Result

def results_list(request):
    results = Result.objects.all().select_related('quiz', 'user').order_by('quiz__name', '-score')
    
    grouped_results = {}
    for quiz_name, group in groupby(results, key=lambda x: x.quiz.name):
        grouped_results[quiz_name] = list(group)
    
    return render(request, 'results_list.html', {'grouped_results': grouped_results})
