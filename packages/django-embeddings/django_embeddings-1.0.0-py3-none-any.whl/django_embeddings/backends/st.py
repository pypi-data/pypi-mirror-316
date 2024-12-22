import logging
import os
import re

import trafilatura
from .base import BaseAnalyzerBackend  # Adjusted import path
from sentence_transformers import SentenceTransformer
from trafilatura.settings import use_config


log = logging.getLogger(__name__)  # noqa


class SentenceTransformerAnalyzerBackend(BaseAnalyzerBackend):
    """
    Quick and dirty analyzer that uses the SentenceTransformer library
    """

    MODEL_NAME = os.getenv("SENTENCE_TRANSFORMERS_MODEL", "multi-qa-MiniLM-L6-cos-v1")
    MODEL_HOME = os.getenv("SENTENCE_TRANSFORMERS_HOME", "/tmp/sentence_transformers")

    def preprocess_text(self, text):
        # Simple text preprocessing: normalize unicode, remove punctuation, and normalize whitespace
        text = re.sub(r'\s+', ' ', text)  # Normalize whitespace
        text = re.sub(r'[^\w\s]', '', text)  # Remove punctuation
        return text.lower()[: self.MAX_INPUT_LENGTH]

    def analyze_response(self, resp):  # pylint: disable=unused-argument
        # Disable the analysis for now
        return []

    def get_content(self, *args):
        # TODO: Backport trafilatura to the base class
        # It will change the results of scraped content,
        # so it's a backwards incompatible change.
        newconfig = use_config()
        newconfig.set("DEFAULT", "DOWNLOAD_TIMEOUT", "3")
        self.downloaded = trafilatura.fetch_url(self.url, config=newconfig)
        if self.downloaded:
            self.metadata = trafilatura.extract_metadata(self.downloaded)
            self.result = trafilatura.extract(
                self.downloaded, include_comments=False, include_tables=False
            )
            return self.preprocess_text(self.result)
        return None

    def embed_response(self, resp) -> list:
        """Analyze an HTTP response and return a list of keywords/topics for the URL."""
        model = SentenceTransformer(self.MODEL_NAME, cache_folder=self.MODEL_HOME)
        text = self.get_content(resp)
        if text:
            # log.info("Postprocessed text: %s", text[:500])
            embedding = model.encode(text)
            return embedding.tolist()

        return None
