from datetime import datetime, timedelta
from django.shortcuts import get_object_or_404, redirect, render
from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import requests
import json
import random
# views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from posts.models import Classe, Cours
from users.models import Profile_Etudiant
from .forms import CourseSelectionForm
from django.http import HttpResponseRedirect
from django.urls import reverse
import os
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from posts.models import Classe, Cours
from users.models import Profile_Etudiant
from django.db import transaction
from .models import Subscription
from users.models import Profile_Etudiant
from django.contrib.auth.decorators import login_required
from .models import BaseResponse
from django.shortcuts import get_object_or_404
from .models import StatusResponse
from .forms import SubscriptionForm
from django.contrib.auth.decorators import login_required
import os

@login_required
def choose_subscription(request, cours_id):
    profile_etudiant = get_object_or_404(Profile_Etudiant, user=request.user)
    cours = get_object_or_404(Cours, pk=cours_id)

    # Vérifier si une souscription existe pour l'utilisateur actuel et le cours spécifique
    try:
        subscription = Subscription.objects.get(user=profile_etudiant, cours_id=cours_id)
        subscription_exists = True
        print("La souscription existe")
    except Subscription.DoesNotExist:
        subscription_exists = False

    if request.method == 'POST':
        form = SubscriptionForm(request.POST, instance=subscription if subscription_exists else None)
        if form.is_valid():
            subscription = form.save(commit=False)
            subscription.user = profile_etudiant
            subscription.cours_id = cours_id
            subscription.price = 100 if subscription.plan == 'STANDARD' else 150
            if subscription_exists:
                # Ajouter un jour à la date de fin existante
                print("La souscription existe, ajout d'un jour")
                subscription.end_date += timedelta(days=1)
            else:
                # Nouvelle souscription : définir la date de fin
                subscription.end_date = datetime.now() + timedelta(days=1)
            subscription.save()
            return redirect('initiate_payment', subscription_id=subscription.id)
    else:
        form = SubscriptionForm(instance=subscription if subscription_exists else None)

    return render(request, 'subscriptions/choose_subscription.html', {'form': form, 'cours': cours})

@login_required
def initiate_payment(request, subscription_id):
    subscription = get_object_or_404(Subscription, id=subscription_id, user__user=request.user)
    profile_etudiant = subscription.user
    amount = subscription.price
    plan_name = subscription.get_plan_display()
    plan_description = f"Souscription à l'abonnement {plan_name}"

    ligdicash_url = "https://app.ligdicash.com/pay/v01/redirect/checkout-invoice/create"

    payload = {
        "commande": {
            "invoice": {
                "items": [
                    {
                        "name": plan_name,
                        "description": plan_description,
                        "quantity": 1,
                        "unit_price": amount,
                        "total_price": amount
                    }
                ],
                "total_amount": amount,
                "devise": "XOF",
                "description": plan_description,
                "customer_firstname": profile_etudiant.prenom,
                "customer_lastname": profile_etudiant.nom,
                "customer_email": request.user.email
            },
            "store": {
                "name": "NomDeMonProjet",
                "website_url": "https://localhost:8000/"
            },
            "actions": {
                "cancel_url": "http://localhost:8000/payment_failed/",
                "return_url": "http://localhost:8000/subscription_success/",
                "callback_url": "http://localhost:8000/payment_callback/"

            },
            "custom_data": {
                "transaction_id": f"LGD{datetime.now().strftime('%Y%m%d%H%M%S')}.C{random.randint(1000, 9999)}",
                "subscription_id": subscription.id
            }
        }
    }

    headers = {
        "Apikey": settings.LIGDICASH_API_KEY,
        "Authorization": f"Bearer {settings.LIGDICASH_API_TOKEN}",
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(ligdicash_url, json=payload, headers=headers)
        response_data = response.json()

        if "response_code" in response_data and response_data["response_code"] == "00":
            redirect_url = response_data["response_text"]
            return redirect(redirect_url)
        else:
            return redirect('payment_failed')

    except requests.exceptions.RequestException as e:
        print("Une erreur est survenue lors de la requête HTTP :", e)
        return redirect('payment_failed')




def save_payment_response(data, file_prefix="payment_response"):
    json_file_path = os.path.join(settings.BASE_DIR, f"{file_prefix}.json")
    txt_file_path = os.path.join(settings.BASE_DIR, f"{file_prefix}.txt")

    # Sauvegarder en fichier JSON
    with open(json_file_path, 'w') as json_file:
        json.dump(data, json_file, indent=4)

    # Sauvegarder en fichier texte
    with open(txt_file_path, 'w') as txt_file:
        txt_file.write(json.dumps(data, indent=4))



@csrf_exempt
def payment_callback(request, invoice_token):
    # Imprimer les informations dans le terminal
    print("Received payment callback data:")
    print(json.dumps(request.POST, indent=4))

    # Sauvegarder les informations dans des fichiers
    save_payment_response(request.POST)

    # Vérifier le statut du paiement via l'API de LigdiCash
    if invoice_token:
        url = f"{settings.LIGDICASH_CONFIRM_URL}?invoiceToken={invoice_token}"
        headers = {
            "Apikey": settings.LIGDICASH_API_KEY,
            "Authorization": f"Bearer {settings.LIGDICASH_API_TOKEN}",
            "Accept": "application/json",
            "Content-Type": "application/json"
        }

        try:
            response = requests.get(url, headers=headers)
            response_data = response.json()

            # Imprimer la réponse de l'API dans le terminal
            print("Response from LigdiCash API:")
            print(json.dumps(response_data, indent=4))

            # Sauvegarder la réponse de l'API dans des fichiers
            save_payment_response(response_data, file_prefix="ligdicash_response")

            # Vérifier le statut du paiement
            if response_data['status'] == 'completed':
                #subscription_id = response_data.get('custom_data', {}).get('subscription_id')
                external_id = response_data.get('external_id', '')
                if external_id:
                   parts = external_id.split(';')
                   if len(parts) > 1:
                       id_part = parts[-1].strip()
                       subscription_id = id_part
                if subscription_id:
                    print("okkkk")
                    try:
                        subscription = Subscription.objects.get(id=subscription_id)
                        subscription.end_date += timedelta(days=30)
                        subscription.save()
                        return HttpResponseRedirect(reverse('subscription_success1'))
                    except Subscription.DoesNotExist:
                        return HttpResponse(status=404)
            elif response_data['status'] == 'nocompleted':
                # Gérer le cas où le paiement est annulé et rediriger
                return HttpResponseRedirect(reverse('payment_failed'))
            elif response_data['status'] == 'pending':
                # Gérer le cas où le paiement est en attente
                return HttpResponse(status=202)
            else:
                return HttpResponse(status=400)

        except requests.exceptions.RequestException as e:
            print("Erreur lors de la requête HTTP :", e)
            return HttpResponse(status=500)

    return HttpResponse(status=400)





def payment_failed(request):
    return render(request, 'subscriptions/payment_failed.html')

from django.http import JsonResponse

def subscription_success(request):
    token = request.GET.get('token')
    token_value = ''
    if token:
        token_value = token
        return redirect('payment_callback', invoice_token=token_value)
        printf("sucesse")
    else:
        return JsonResponse({'error': 'Token missing in the request parameters.'}, status=400)


def subscription_success1(request):
    return render(request, 'subscriptions/subscription_success.html')


@login_required
def select_course(request):
    etudiant = get_object_or_404(Profile_Etudiant, user=request.user)
    classe = get_object_or_404(Classe, name=etudiant.level)

    if request.method == 'POST':
        form = CourseSelectionForm(request.POST)
        if form.is_valid():
            selected_course = form.cleaned_data['course']
            course_id = selected_course.id

            # Gérer la logique de création de souscription avec le cours sélectionné ici
            # Par exemple, créer une instance de Subscription avec selected_course

            # return render(request, 'path/to/template.html', {'selected_course_id': course_id})
            return redirect('choose_subscription', cours_id=course_id)
    else:
        form = CourseSelectionForm()

    return render(request, 'select_course/select_course.html', {'form': form})

