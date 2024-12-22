from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django_embeddings.views import AnalyzedUrlView  # Corrected import

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('django_embeddings.urls')),  # Include the URLs from django_embeddings
    path('api-auth/', include('rest_framework.urls')),  # Added rest_framework URLs
    path('api/v1/similar-pages/', AnalyzedUrlView.as_view(), name='similar-pages-api'),
    path('similar-pages/', TemplateView.as_view(template_name='similar_pages.html'), name='similar-pages'),
]
