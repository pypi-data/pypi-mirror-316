from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin

from .models import AnalyzedUrlEmbedding, UserSubmittedUrlEmbedding, AnalyzedUrl, EmbeddingType
from .tasks import analyze_url  # Import analyze_url from tasks.py

@admin.action(description='Re-analyze selected URLs')
def reanalyze_urls(modeladmin, request, queryset):
    for url in queryset:
        url.last_analyzed_date = None
        url.save()
        # Trigger the analysis task
        analyze_url.enqueue(url.url)  # Use django_tasks enqueue method

class AnalyzedUrlEmbeddingInline(admin.TabularInline):
    model = AnalyzedUrlEmbedding
    extra = 0

@admin.register(AnalyzedUrlEmbedding)
class AnalyzedUrlEmbeddingAdmin(SimpleHistoryAdmin):
    """Django admin configuration for analyzed URLs."""

    list_display = (
        "analyzed_url",
        "embedding_type",
    )
    list_per_page = 500
    list_select_related = ("analyzed_url",)
    raw_id_fields = ("analyzed_url",)
    search_fields = ("analyzed_url__url", "model")


@admin.register(UserSubmittedUrlEmbedding)
class UserSubmittedUrlEmbeddingAdmin(admin.ModelAdmin):
    """Django admin configuration for user submitted URLs."""

    date_hierarchy = "last_analyzed_date"
    list_display = (
        "url",
        "embedding_type",
        "status",
        "last_analyzed_date",
    )
    list_per_page = 500
    list_filter = ("status",)
    search_fields = ("url", "model")


@admin.register(EmbeddingType)
class EmbeddingTypeAdmin(admin.ModelAdmin):
    """Django admin configuration for embedding types."""

    list_display = ("name", "model", "dimensions")
    search_fields = ("name", "model")


@admin.register(AnalyzedUrl)
class AnalyzedUrlAdmin(admin.ModelAdmin):
    list_display = ('url', 'domain', 'last_analyzed_date', 'title', 'get_embedding_type')
    search_fields = ('url', 'domain', 'title')
    actions = [reanalyze_urls]
    inlines = [AnalyzedUrlEmbeddingInline]  # Add inline for AnalyzedUrlEmbedding

    def get_embedding_type(self, obj):
        embedding = obj.embeddings.first()
        return embedding.embedding_type if embedding else None
    get_embedding_type.short_description = 'Embedding Type'
