from django.db import models
from users.models import Profile_Etudiant
from decimal import Decimal
from django.db import models
from users.models import Profile_Etudiant
from posts.models import Cours,Classe
class Subscription(models.Model):
    PLAN_CHOICES = (
        ('STANDARD', 'Standard'),
        ('PREMIUM', 'Premium'),
    )
    user = models.ForeignKey(Profile_Etudiant, on_delete=models.CASCADE)
    plan = models.CharField(max_length=10, choices=PLAN_CHOICES)
    price = models.FloatField()
    #price = models.DecimalField(max_digits=6, decimal_places=2)
    cours_id = models.IntegerField(null=True, blank=True)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField()
    #cours = models.ForeignKey(Cours, on_delete=models.CASCADE, null=True, blank=True)


    def save(self, *args, **kwargs):
        # Définir le prix en fonction du plan choisi
        if self.plan == 'STANDARD':
            self.price = Decimal('100.00')
        elif self.plan == 'PREMIUM':
            self.price = Decimal('150.00')

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user} - {self.plan}"



from typing import Dict, Any, Optional, List

class BaseResponse:
    """
    Cette classe définit un objet BaseResponse qui représente une réponse de base de l'API.

    Attributes
    ----------
    response_code : str
        Code de réponse de la requête, "00" ou "01".
    token : str
        Token de la requête.
    response_text : str
        Texte de réponse de la requête.
    description : str
        Description de la réponse.
    wiki : List[str]
        Liste des liens wiki liés à la réponse.
    custom_data : Dict[str, Any], optional
        Données personnalisées de la réponse, par défaut {}.
    customdata : Dict[str, Any], optional
        Autre version de custom_data, par défaut {}.
    """

    def __init__(
            self,
            response_code: str,
            token: str,
            response_text: str,
            description: str,
            wiki: List[str],
            customdata: Dict[str, Any] = {},
            custom_data: Dict[str, Any] = {},
            *args,
            **kwargs
    ):
        """
        Initialise une instance de BaseResponse avec les données fournies.

        Parameters
        ----------
        response_code : str
            Code de réponse de la requête, "00" ou "01".
        token : str
            Token de la requête.
        response_text : str
            Texte de réponse de la requête.
        description : str
            Description de la réponse.
        wiki : List[str]
            Liste des liens wiki liés à la réponse.
        custom_data : Dict[str, Any], optional
            Données personnalisées de la réponse, par défaut {}.
        customdata : Dict[str, Any], optional
            Autre version de custom_data, par défaut {}.
        """
        self.response_code = response_code
        self.token = token
        self.response_text = response_text
        self.description = description
        self.custom_data = custom_data or customdata
        self.wiki = wiki

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "BaseResponse":
        """
        Crée une instance de BaseResponse à partir d'un dictionnaire de données.

        Parameters
        ----------
        data : Dict[str, Any]
            Le dictionnaire de données pour créer l'instance.

        Returns
        -------
        BaseResponse
            Une instance de BaseResponse avec les données fournies.
        """
        return cls(**data)

class StatusResponse(BaseResponse):
    """
    Classe représentant une réponse de statut pour une transaction.
    Hérite de la classe BaseResponse

    Attributes
    ----------
    response_code : str
        Code de réponse de la demande de paiement, "00" ou "01".
    token : str
        Token de la transaction.
    response_text : str
        Texte de réponse de la transaction.
    description : str
        Description de la demande de paiement.
    custom_data : Dict[str, Any], optionnel
        Données associées à la transaction.
    wiki : List[str]
        Dictionnaire d'erreur ou lien menant vers le dictionnaire d'erreur.
    montant : int
        Montant de la transaction.
    status : str
        Statut de la transaction.
    operator_id : str
        ID de l'opérateur de la transaction.
    operator_name : str
        Nom de l'opérateur de la transaction.
    external_id : str
        ID externe de la transaction.
    customer : Optional[str]
        Numéro utilisé pour la transaction.
    amount : int
        Montant de la transaction.
    transaction_id : str
        ID de la transaction.
    date : Optional[str]
        Date de la transaction.
    request_id : Optional[str]
        ID de la demande.
    """

    def __init__(
            self,
            response_code: str,
            token: str,
            response_text: str,
            description: str,
            custom_data: Dict[str, Any],
            wiki: List[str],
            montant: int,
            amount: int,
            status: str,
            operator_id: str,
            operator_name: str,
            external_id: str,
            transaction_id: str,
            date: Optional[str] = None,
            customer: Optional[str] = None,
            request_id: Optional[str] = None,
    ):
        """
        Initialise une instance de StatusResponse.

        Parameters
        ----------
        response_code : str
            Code de réponse de la demande de paiement, "00" ou "01".
        token : str
            Token de la transaction.
        response_text : str
            Texte de réponse de la transaction.
        description : str
            Description de la demande de paiement.
        custom_data : Dict[str, Any], optionnel
            Données associées à la transaction.
        wiki : List[str]
            Dictionnaire d'erreur ou lien menant vers le dictionnaire d'erreur.
        montant : int
            Montant de la transaction.
        status : str
            Statut de la transaction.
        operator_id : str
            ID de l'opérateur de la transaction.
        operator_name : str
            Nom de l'opérateur de la transaction.
        external_id : str
            ID externe de la transaction.
        transaction_id : str
            ID de la transaction.
        date : Optional[str], optionnel
            Date de la transaction.
        customer : Optional[str], optionnel
            Numéro utilisé pour la transaction.
        request_id : Optional[str], optionnel
            ID de la demande.
        """
        super().__init__(response_code, token, response_text, description, custom_data, wiki)
        self.montant = montant
        self.amount = amount
        self.status = status
        self.operator_id = operator_id
        self.operator_name = operator_name
        self.external_id = external_id
        self.transaction_id = transaction_id
        self.customer = customer
        self.date = date
        self.request_id = request_id

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "StatusResponse":
        """
        Construit une instance de la classe StatusResponse à partir d'un dictionnaire.

        Parameters
        ----------
        data : Dict[str, Any]
            Dictionnaire contenant les données pour construire l'instance.

        Returns
        -------
        StatusResponse
            L'instance construite à partir des données.
        """
        return cls(**data)
