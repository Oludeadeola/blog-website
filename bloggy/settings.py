from datetime import timedelta
from pathlib import Path

import dj_database_url
import os

from bloggy.environment import ENV

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = ENV.str("SECRET_KEY")
DEBUG = ENV.bool("DEBUG", False)
ALLOWED_HOSTS = []
INSTALLED_APPS = [
    "admin_auto_filters.apps.AdminAutoFiltersConfig",
    "admin_interface.apps.AdminInterfaceConfig",
    "colorfield",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "debug_toolbar.apps.DebugToolbarConfig",
    "django.contrib.staticfiles",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "allauth.socialaccount.providers.facebook",
    "allauth.socialaccount.providers.twitter",
    "allauth.socialaccount.providers.twitter_oauth2",
    "elasticsearch_dsl",
    "django_elasticsearch_dsl",
    "django_elasticsearch_dsl_drf",
    "commons.apps.CommonsConfig",
    "anymail.apps.AnymailBaseConfig",
    "auths.apps.AuthsConfig",
    "blog.apps.BlogConfig",
    "django_filters",
    "rest_framework_simplejwt.token_blacklist",
]
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "allauth.account.middleware.AccountMiddleware",
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]
ELASTICSEARCH_DSL = {"default": {"hosts": "localhost:9200"}}
ROOT_URLCONF = "bloggy.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "bloggy.wsgi.application"

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
    ...,
]

# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {"default": dj_database_url.config()}

# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
    {
        "NAME": "auths.validators.CustomPasswordValidator",
    },
]

# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = "static/"

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

REST_FRAMEWORK = {
    "DEFAULT_RENDERER_CLASSES": ["rest_framework.renderers.JSONRenderer"],
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ],
}
AUTH_USER_MODEL = "auths.User"
EMAIL_BACKEND = "anymail.backends.brevo.EmailBackend"
SERVER_EMAIL = ENV.str("SERVER_EMAIL")
DEFAULT_FROM_EMAIL = ENV.str("DEFAULT_FROM_EMAIL")
ANYMAIL = {
    "BREVO_API_KEY": ENV.str("BREVO_API_KEY"),
    "IGNORE_UNSUPPORTED_FEATURES": True,
}

SOCIALACCOUNT_PROVIDERS = {
    "facebook": {"APP": {"client_id": "", "secret": "", "key": ""}},
    "twitter": {},
}

# Logging #
# LOGGING = {
#     'version': 1,
#     'filters': {
#         'require_debug_true': {
#             '()': 'django.utils.log.RequireDebugTrue',
#         }
#     },
#     'handlers': {
#         'console': {
#             'level': 'DEBUG',
#             'filters': ['require_debug_true'],
#             'class': 'logging.StreamHandler',
#         }
#     },
#     'loggers': {
#         'django.db.backends': {
#             'level': 'DEBUG',
#             'handlers': ['console'],
#             'propagate': False,
#         }
#     }
# }

#  JWT
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(
        minutes=ENV.int("ACCESS_TOKEN_LIFETIME", default=4320)
    ),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=ENV.int("REFRESH_TOKEN_LIFETIME")),
    "ROTATE_REFRESH_TOKENS": ENV.bool("ROTATE_REFRESH_TOKENS"),
    "BLACKLIST_AFTER_ROTATION": ENV.bool("BLACKLIST_AFTER_ROTATION"),
    "UPDATE_LAST_LOGIN": ENV.bool("UPDATE_LAST_LOGIN"),
    "SIGNING_KEY": ENV.str("SIGNING_KEY"),
    "USER_ID_FIELD": "uuid",
}
AUTH_TOKEN_TIMEOUT = ENV.int("AUTH_TOKEN_TIMEOUT")
AUTH_TOKEN_SECRET = ENV.str("AUTH_TOKEN_SECRET")
