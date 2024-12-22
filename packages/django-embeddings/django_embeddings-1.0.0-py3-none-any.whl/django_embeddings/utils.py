import logging

from pgvector.django import CosineDistance

import re
from urllib import parse as urlparse


from .backends.st import SentenceTransformerAnalyzerBackend
from .models import (
    AnalyzedUrlEmbedding,
    UserSubmittedUrlEmbedding,
)  # Ensure correct model names

log = logging.getLogger(__name__)

"""Constants used for the ad server keyword/topic analyzer."""

# Query parameters on URLs to ignore
IGNORED_QUERY_PARAMS = (
    "q",
    "query",
    "search",
    "utm_campaign",
    "utm_medium",
    "utm_source",
    "utm_label",
    "utm_keyword",
    "utm_content",
    "utm_term",
    "utm_id",
    "ref",
)

def get_embedding(url):
    """
    Fetch content from the URL and analyze it to get the embedding.
    """
    backend_instance = SentenceTransformerAnalyzerBackend(url)
    response = backend_instance.fetch()
    if not response:
        return [None, None, None]

    processed_text = backend_instance.get_content(response)
    analyzed_embedding = backend_instance.embedding(response)
    return processed_text, analyzed_embedding, backend_instance.metadata


def get_niche_weights(url, flights=None):
    """
    Calculate the similarity distance for each advertiser based on the publisher URL.

    This only queries the advertiser weights after we know we have a publisher embedding,
    because the weight query is the most expensive part of the operation.
    """
    normalized_url = normalize_url(url)
    log.debug("Getting embedding for URL: %s", normalized_url)
    publisher_embedding = AnalyzedUrlEmbedding.objects.filter(
        analyzed_url__url=normalized_url
    ).first()

    if not publisher_embedding:
        log.debug("Can't use niche targeting. No embedding for URL: %s", normalized_url)
        return {}

    # Removed references to AnalyzedAdvertiserUrlEmbedding

    return {}


def normalize_url(url):
    """
    Normalize a URL.

    Currently, this means:
    - Removing ignored query paramters
    """
    parts = urlparse.urlparse(url)

    query_params = urlparse.parse_qs(parts.query, keep_blank_values=True)
    for param in IGNORED_QUERY_PARAMS:
        if param in query_params:
            query_params.pop(param)

    # The _replace method is a documented method even though it appears "private"
    parts = parts._replace(query=urlparse.urlencode(query_params, True))

    return urlparse.urlunparse(parts)


def normalize_title(title):
    """
    Remove trailing non-word characters from title.

    Generally useful for cleaning up Sphinx docs.
    """
    if not title:
        return title
    return re.sub(r"\W+$", "", title)
