from django.apps import AppConfig
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

class DjangoEmbeddingsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'django_embeddings'
