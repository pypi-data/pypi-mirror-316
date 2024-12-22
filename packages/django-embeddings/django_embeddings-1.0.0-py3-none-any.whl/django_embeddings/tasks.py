"""Tasks for analyzing URLs for topics and keywords."""

import datetime
import logging
from urllib.parse import urlparse

from django.utils import timezone
from django_tasks import task
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings

from .models import AnalyzedUrl, AnalyzedUrlEmbedding, UserSubmittedUrlEmbedding, EmbeddingType
from .utils import get_embedding, normalize_url, normalize_title  # Import normalize_title

log = logging.getLogger(__name__)

ANALYZER_MODEL = settings.ANALYZER_MODEL

@task
def analyze_url(url, force=False):
    """
    Analyze a given URL.

    - Creates or updates an entry in AnalyzedUrls table
    - Discovers keywords and topics for a URL
    """
    normalized_url = normalize_url(url)
    domain = urlparse(normalized_url).netloc

    # Check if we've recently analyzed the URL
    # If we have, skip it
    existing_record = AnalyzedUrl.objects.filter(
        url=normalized_url
    ).first()

    if (
        existing_record
        and not force
        and existing_record.last_analyzed_date
        and existing_record.last_analyzed_date
        > (timezone.now() - datetime.timedelta(days=7))
    ):
        log.warning("URL recently analyzed. Skipping.")
        return

    log.debug("Analyzing url: %s", normalized_url)

    _text, embedding, metadata = get_embedding(normalized_url)

    if not embedding:
        log.warning("No embedding found for: %s", normalized_url)
        return

    analyzed_url, created = AnalyzedUrl.objects.get_or_create(
        url=normalized_url,
        defaults={
            "last_analyzed_date": timezone.now(),
            "title": normalize_title(metadata.title) if metadata else "",
            "description": metadata.description if metadata else "",
            "domain": domain,
        },
    )

    if not created:
        # Don't update date if it doesn't exist
        analyzed_url.last_analyzed_date = timezone.now()
        analyzed_url.title = normalize_title(metadata.title) if metadata else ""
        analyzed_url.description = metadata.description if metadata else ""
        analyzed_url.domain = domain
        analyzed_url.save()

    if embedding:
        try:
            embedding_type = EmbeddingType.objects.get(model=ANALYZER_MODEL)
        except ObjectDoesNotExist:
            embedding_type = EmbeddingType.objects.create(name=ANALYZER_MODEL, model=ANALYZER_MODEL, dimensions=384)
            log.info(f"Created new EmbeddingType with model '{ANALYZER_MODEL}'.")

        analyzed_embedding, created = AnalyzedUrlEmbedding.objects.get_or_create(
            analyzed_url=analyzed_url,
            defaults={
                "vector": embedding,
                "embedding_type": embedding_type,
            },
        )

        if not created:
            analyzed_embedding.vector = embedding
            analyzed_embedding.save()


@task
def analyze_user_url(url, model="v1", force=False):
    """
    Analyze a user-submitted URL.

    - Creates and/or updates an entry in UserSubmittedUrlEmbedding table
    - Stores embeddings
    """
    normalized_url = normalize_url(url)

    # Check if we've recently analyzed the URL
    # If we have, skip it
    existing_record = UserSubmittedUrlEmbedding.objects.filter(
        url=normalized_url,
        embedding_type__model=ANALYZER_MODEL,
    ).first()

    if (
        existing_record
        and not force
        and not existing_record.status == UserSubmittedUrlEmbedding.STATUS_ERROR
        and existing_record.last_analyzed_date
        > (timezone.now() - datetime.timedelta(days=7))
    ):
        log.warning("URL recently analyzed. Skipping.")
        return

    log.debug("Analyzing user url: %s", normalized_url)

    try:
        embedding_type = EmbeddingType.objects.get(model=model)
    except ObjectDoesNotExist:
        embedding_type = EmbeddingType.objects.create(name=model, model=model, dimensions=384)
        log.info(f"Created new EmbeddingType with model '{model}'.")

    user_url, _created = UserSubmittedUrlEmbedding.objects.get_or_create(
        url=normalized_url,
        embedding_type=embedding_type,
        defaults={
            "status": UserSubmittedUrlEmbedding.STATUS_PROCESSING,
        },
    )

    _text, embedding, _metadata = get_embedding(normalized_url)

    if embedding:
        user_url.vector = embedding
        user_url.status = UserSubmittedUrlEmbedding.STATUS_SUCCESS
    else:
        user_url.status = UserSubmittedUrlEmbedding.STATUS_ERROR

    # Update the last analyzed date even on an error
    user_url.last_analyzed_date = timezone.now()
    user_url.save()


@task
def daily_analyze_urls(days=30, min_visits=100, force=False):
    """Analyze URLs that have not been analyzed since `days` number of days."""
    dt_cutoff = timezone.now() - datetime.timedelta(days=30)

    analyzed_urls = AnalyzedUrl.objects.filter(
        last_analyzed_date__lt=dt_cutoff, visits_since_last_analyzed__gte=min_visits
    ).select_related()

    log.debug("URLs to analyze: %s", analyzed_urls.count())
    for analyzed_url in analyzed_urls:
        analyze_url.apply_async(
            args=[analyzed_url.url, force],
            queue="analyzer",
        )
