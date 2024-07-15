"""
Django settings for miniapp project.

Generated by 'django-admin startproject' using Django 5.0.6.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

from pathlib import Path
import os
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-7+m&skhwlos!=%ojh!8rnryrqa29q4%8rh-ts=1c$r!@kqurj#'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',  # Nécessaire pour django-allauth
    'allauth',
    'allauth.account',
    'allauth.socialaccount',  # Si vous voulez la connexion sociale
    'posts',
    'users',
    'subscriptions',
    'questions',
    'quizapp',
    'quizes',
    'results'
]
#AUTH_USER_MODEL = 'users.Profile_Etudiant'

ACCOUNT_FORMS = {
    'signup': 'users.forms.CustomSignupForm',
}

SITE_ID = 1  # ID de votre site dans la table django_sites

# Configurez les variables spécifiques à django-allauth
AUTHENTICATION_BACKENDS = [
    # Needed for login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

# Configurez les paramètres de courriel
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'hasbendjango@gmail.com'
EMAIL_HOST_PASSWORD = 'yfix huep dmcv qkaq'
DEFAULT_FROM_EMAIL = 'hasbendjango@gmail.com'  # L'adresse email par défaut
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'  # Activation de la vérification d'email
ACCOUNT_AUTHENTICATION_METHOD = 'email'  # Méthode d'authentification par email uniquement
ACCOUNT_EMAIL_REQUIRED = True  # L'email est requis
ACCOUNT_UNIQUE_EMAIL = True  # Les adresses email doivent être uniques

# Pour activer la vérification d'email asynchrone avec django-allauth
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 7

# Configurez le chemin de redirection après la connexion ou la déconnexion
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',
]

ROOT_URLCONF = 'miniapp.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'miniapp.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'miniapp',
        'USER': 'miniappadmin',
        'PASSWORD': '12345678',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-US'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

#STATIC_URL = 'static/'
# URL pour accéder aux fichiers statiques
STATIC_URL = '/static/'

# Répertoires où Django cherchera les fichiers statiques en développement
STATICFILES_DIRS = [
    BASE_DIR / "static",
    ]

# Répertoire où collecter les fichiers statiques pour la production
STATIC_ROOT = BASE_DIR / "staticfiles"


# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# settings.py

LIGDICASH_API_KEY = 'MAGPMLT3QFJLIPUDN'
LIGDICASH_API_TOKEN = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZF9hcHAiOjE1MDA5LCJpZF9hYm9ubmUiOjg5OTQyLCJkYXRlY3JlYXRpb25fYXBwIjoiMjAyNC0wNC0wOCAwODozMjoyNCJ9.NRcyHfFO8OyaXOaklZ2DJ2Arf-gV8OXGfMIELQzdw88'
LIGDICASH_CALLBACK_URL = 'http://localhost:8000/payment_callback/'
LIGDICASH_CONFIRM_URL = 'https://app.ligdicash.com/pay/v01/redirect/checkout-invoice/confirm/'

CSRF_TRUSTED_ORIGINS = [
    'http://localhost:8000',  # Remplacez par l'URL de votre serveur local
]
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

