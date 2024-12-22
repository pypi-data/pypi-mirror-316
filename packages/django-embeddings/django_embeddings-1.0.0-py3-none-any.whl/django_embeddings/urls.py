from django.urls import path
from .views import AnalyzedUrlView

urlpatterns = [
    path('similar-pages/', AnalyzedUrlView.as_view(), name='similar-pages'),
]
