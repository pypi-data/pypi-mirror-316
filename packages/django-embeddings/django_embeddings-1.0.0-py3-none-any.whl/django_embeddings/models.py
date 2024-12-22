from django.db import models
from django.utils.translation import gettext_lazy as _
from django_extensions.db.models import TimeStampedModel
from pgvector.django import VectorField
from simple_history.models import HistoricalRecords
from .validators import KeywordsValidator

class EmbeddingType(models.Model):
    name = models.CharField(max_length=255, unique=True)
    model = models.CharField(max_length=255)
    dimensions = models.PositiveIntegerField()

    def __str__(self):
        return self.name

class UserSubmittedUrlEmbedding(TimeStampedModel):
    STATUS_SUCCESS = "Success"
    STATUS_QUEUED = "Queued"
    STATUS_ERROR = "Error"
    STATUS_PROCESSING = "Processing"
    STATUSES = (
        (STATUS_SUCCESS, _(STATUS_SUCCESS)),
        (STATUS_QUEUED, _(STATUS_QUEUED)),
        (STATUS_ERROR, _(STATUS_ERROR)),
        (STATUS_PROCESSING, _(STATUS_PROCESSING)),
    )

    url = models.URLField(
        db_index=True,
        max_length=1024,
        help_text=_(
            "URL of the page to analyze after certain query parameters are stripped away"
        ),
    )

    status = models.CharField(
        max_length=50,
        choices=STATUSES,
        default=STATUS_QUEUED,
        help_text=_("Status of the analysis"),
    )

    last_analyzed_date = models.DateTimeField(
        db_index=True,
        default=None,
        null=True,
        blank=True,
        help_text=_("Last time the ad server analyzed this URL"),
    )

    embedding_type = models.ForeignKey(
        EmbeddingType,
        on_delete=models.CASCADE,
        related_name="user_submitted_embeddings",
        null=True,
        blank=True,
    )
    vector = VectorField(default=None, null=True, blank=True)

    class Meta:
        unique_together = ("url", "embedding_type")

    def __str__(self):
        return f"UserSubmittedURL: '{self.url}' - '{self.embedding_type}'"


class AnalyzedUrl(TimeStampedModel):
    """Analyzed keywords for a given URL."""

    url = models.URLField(
        db_index=True,
        max_length=1024,
        help_text=_(
            "URL of the page being analyzed after certain query parameters are stripped away"
        ),
    )

    keywords = models.JSONField(
        _("Keywords for this URL"),
        blank=True,
        null=True,
        validators=[KeywordsValidator()],
    )

    last_analyzed_date = models.DateTimeField(
        db_index=True,
        default=None,
        null=True,
        blank=True,
        help_text=_("Last time the ad server analyzed this URL"),
    )

    title = models.TextField(
        _("Title of the page"),
        default=None,
        null=True,
        blank=True,
    )

    description = models.TextField(
        _("Description of the page"),
        default=None,
        null=True,
        blank=True,
    )

    domain = models.CharField(
        max_length=255,
        help_text=_("Domain where this URL appears"),
        null=True,
        blank=True,
    )

    visits_since_last_analyzed = models.PositiveIntegerField(
        default=0,
        help_text=_(
            "Number of times ads have been served for this URL since it was last analyzed"
        ),
    )

    class Meta:
        unique_together = ("url", "domain")

    def __str__(self):
        """Simple override."""
        return f"{self.keywords} on {self.url}"

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

class AnalyzedUrlEmbedding(TimeStampedModel):
    analyzed_url = models.ForeignKey(
        AnalyzedUrl,
        on_delete=models.CASCADE,
        related_name="embeddings",
    )
    embedding_type = models.ForeignKey(
        EmbeddingType,
        on_delete=models.CASCADE,
        related_name="analyzed_embeddings",
    )
    vector = VectorField(default=None, null=True, blank=True)

    history = HistoricalRecords()

    class Meta:
        unique_together = ("analyzed_url", "embedding_type")

    @property
    def url(self):
        return self.analyzed_url.url

    @property
    def title(self):
        return self.analyzed_url.title

    @property
    def description(self):
        return self.analyzed_url.description

    def __str__(self):
        return f"Embedding: '{self.analyzed_url.url}' - '{self.embedding_type}'"
