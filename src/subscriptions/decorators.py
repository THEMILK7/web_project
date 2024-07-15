from django.shortcuts import redirect, get_object_or_404
from django.utils import timezone
from functools import wraps
from .models import Subscription
 # Assurez-vous d'importer le modèle Cours depuis votre application courses
from django.shortcuts import redirect, get_object_or_404
from django.utils import timezone
from functools import wraps
from subscriptions.models import Subscription
from users.models import Profile_Etudiant
from posts.models import Cours
def subscription_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, cours_id, *args, **kwargs):
        if request.user.is_authenticated:
            # Récupérer le Profile_Etudiant associé à l'utilisateur connecté
            profile_etudiant = get_object_or_404(Profile_Etudiant, user=request.user)
            try:
                # Filtrer les souscriptions pour l'utilisateur et le cours spécifié
                subscription = Subscription.objects.filter(user=profile_etudiant, cours_id=cours_id).latest('end_date')
                if subscription.end_date >= timezone.now():
                    return view_func(request, cours_id, *args, **kwargs)
            except Subscription.DoesNotExist:
                pass
        # Redirection vers la page de choix d'abonnement si aucune souscription n'est trouvée
        return redirect('choose_subscription', cours_id=cours_id)
    return _wrapped_view

