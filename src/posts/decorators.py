# decorators.py
from django.shortcuts import redirect
from functools import wraps

def require_teacher_login(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated or not hasattr(request.user, 'profile_professeur'):
            return redirect('prof_login')  # Redirige vers la page de login des professeurs
        return view_func(request, *args, **kwargs)
    return _wrapped_view
