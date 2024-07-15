import requests
import json

def payin_with_redirection(transaction_id, amount):
    url = "https://app.ligdicash.com/pay/v01/redirect/checkout-invoice/create"

    payload = {
        "commande": {
            "invoice": {
                "items": [
                    {
                        "name": "Nom de article ou service ou produits",
                        "description": "Description du service ou produits",
                        "quantity": 1,
                        "unit_price": amount,
                        "total_price": amount
                    }
                ],
                "total_amount": amount,
                "devise": "XOF",
                "description": "Descrion de la commande des produits ou services",
                "customer": "",
                "customer_firstname": "Prenom du client",
                "customer_lastname": "Nom du client",
                "customer_email": "tester@ligdicash.com"
            },
            "store": {
                "name": "NomDeMonprojet",
                "website_url": "https://monsite.com"
            },
            "actions": {
                "cancel_url": "https://monsite.com",
                "return_url": "http://localhost/api/api_public_ligdicash/status_payin_php_cURL.php",
                "callback_url": "http://localhost/api/api_public_ligdicash/status_payin_php_cURL.php"
            },
            "custom_data": {
                "transaction_id": transaction_id
            }
        }
    }

    headers = {
        "Apikey": "YNYZ3BXIFWRBBPFQ2",
        "Authorization": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZF9hcHAiOiI3NzQiLCJpZF9hYm9ubmUiOiI4OTk0MiIsImRhdGVjcmVhdGlvbl9hcHAiOiIyMDIxLTA4LTE4IDE4OjIwOjQyIn0.8rMinJMEDZeeoGNqcKxwD2VjXPC5t1__ilTJIOwFtQ4",
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        response_data = response.json()

        if "response_code" in response_data and response_data["response_code"] == "00":
            # Redirection vers l'URL de paiement si le paiement est autorisé
            redirect_url = response_data["response_text"]
            print(f"Redirection vers: {redirect_url}")
            # Ici vous pouvez rediriger l'utilisateur vers redirect_url

        else:
            # Affichage des erreurs en cas de problème avec la transaction
            print(f"response_code={response_data.get('response_code')}")
            print(f"response_text={response_data.get('response_text')}")
            print(f"description={response_data.get('description')}")

    except requests.exceptions.RequestException as e:
        print("Une erreur est survenue lors de la requête HTTP :", e)

# Exemple d'exécution
transaction_id = f"LGD{datetime.now().strftime('%Y%m%d.%H%M')}.C{random.randint(5, 100000)}"
amount = 100

payin_with_redirection(transaction_id, amount)
