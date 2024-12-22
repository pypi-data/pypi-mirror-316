import datetime
import logging
from urllib.parse import urlparse
from django.conf import settings

from django.core.exceptions import ValidationError
from django.core.validators import URLValidator
from django.utils import timezone
from pgvector.django import CosineDistance
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import AnalyzedUrlEmbedding, UserSubmittedUrlEmbedding, EmbeddingType  # Ensure correct model names
from .tasks import analyze_user_url  # Import Celery task
from .utils import normalize_title, normalize_url

log = logging.getLogger(__name__)

class BaseAnalyzedView(APIView):
    ANALYZER_MODEL = settings.ANALYZER_MODEL
    RECENTLY_ANALYZED_THRESHOLD_DAYS = 7
    MAX_RESULTS = 10
    MAX_DISTANCE = 0.55

    permission_classes = [AllowAny]

    def _get_urls(self, embedding):
        raise NotImplementedError("Must define _get_urls")

    def get(self, request):
        """Return a list of similar URLs and scores based on querying the AnalyzedURL embedding for an incoming URL."""
        url = request.query_params.get("url")

        if not url:
            log.error("URL parameter is missing")
            return Response(
                {"error": "url is required"}, status=status.HTTP_400_BAD_REQUEST
            )

        # Validate the URL
        url_validator = URLValidator(schemes=("http", "https"))
        try:
            url_validator(url)
        except ValidationError:
            log.error("Invalid URL: %s", url)
            return Response(
                {"error": "enter a valid URL"}, status=status.HTTP_400_BAD_REQUEST
            )

        # Get an existing analysis record if there is one
        normalized_url = normalize_url(url)
        existing_record = UserSubmittedUrlEmbedding.objects.filter(
            url=normalized_url,
            embedding_type__model=self.ANALYZER_MODEL,
        ).first()

        # If there's no recent record, queue it for processing
        if (
            not existing_record
            or not existing_record.last_analyzed_date
            or existing_record.last_analyzed_date
            < timezone.now()
            - datetime.timedelta(days=self.RECENTLY_ANALYZED_THRESHOLD_DAYS)
        ):
            log.info("Queueing URL for analysis: %s", normalized_url)
            analyze_user_url.enqueue(normalized_url)  # Use enqueue method
            return Response(
                {"status": "queued for analysis"}, status=status.HTTP_202_ACCEPTED
            )

        if existing_record.status != UserSubmittedUrlEmbedding.STATUS_SUCCESS:
            log.error("Failed to fetch content from URL: %s", normalized_url)
            return Response(
                {"error": "Not able to fetch content from URL"},
                status=status.HTTP_400_BAD_REQUEST,
            )


        unfiltered_data = self._get_urls(existing_record.vector)
        log.info("Found %s similar pages", len(unfiltered_data))

        # Filter urls to ensure each domain is unique
        unique_domains = set()
        data = []
        for dat in unfiltered_data:
            domain = urlparse(dat.url).netloc
            if domain not in unique_domains:
                unique_domains.add(domain)
                data.append(dat)

        return Response(
            {
                "count": len(data),
                "results": [
                    {
                        "url": dat.url,
                        "title": normalize_title(dat.title),
                        "description": dat.description,
                        "distance": dat.distance,
                    }
                    for dat in data[: self.MAX_RESULTS]
                ],
            }
        )


class AnalyzedUrlView(BaseAnalyzedView):
    """
    Returns a list of publisher pages that match an advertisers URL.

    Example: http://localhost:8000/api/v1/similar-pages/?url=https://www.gitbook.com/
    """

    def _get_urls(self, embedding):
        return (
            AnalyzedUrlEmbedding.objects.filter(
                embedding_type__model=self.ANALYZER_MODEL,
            )
            .exclude(vector=None)
            .annotate(distance=CosineDistance("vector", embedding))
            .filter(distance__lte=self.MAX_DISTANCE)
            .order_by("distance")[:50]
        )
