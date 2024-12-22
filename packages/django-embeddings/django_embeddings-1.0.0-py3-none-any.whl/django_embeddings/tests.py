import requests
import responses
from django.test import TestCase

from .backends.competitors import CompetitorAnalyzerBackend
from .models import UserSubmittedUrlEmbedding, AnalyzedUrl, AnalyzedUrlEmbedding


class TestCompetitorAnalyzerBackend(TestCase):
    def setUp(self):
        self.url = "https://example.com"
        self.analyzer = CompetitorAnalyzerBackend(self.url, raise_if_found=True)

    @responses.activate
    def test_analyzer_no_competitors_found(self):
        responses.add(
            responses.GET,
            self.url,
            body="""
                <html>
                <head>
                </head>
                <body>
                    <main>
                    <p>Nothing</p>
                    </main>
                </body>
                </html>
                """,
        )

        self.assertEqual(
            self.analyzer.analyze(requests.get(self.url)),
            [],
        )

    @responses.activate
    def test_competitors_found(self):
        responses.add(
            responses.GET,
            self.url,
            body="""
                <html>
                <head>
                    <script async src="https://cdn.carbonads.com/carbon.js" id="_carbonads_js"></script>
                </head>
                <body>
                    <main></main>
                </body>
                </html>
                """,
        )
        with self.assertRaises(RuntimeError):
            self.analyzer.analyze(requests.get(self.url))


class UserSubmittedUrlEmbeddingTestCase(TestCase):
    def setUp(self):
        UserSubmittedUrlEmbedding.objects.create(url="http://example.com", status="Queued")

    def test_user_submitted_url_embedding(self):
        url_embedding = UserSubmittedUrlEmbedding.objects.get(url="http://example.com")
        self.assertEqual(url_embedding.status, "Queued")

class AnalyzedUrlTestCase(TestCase):
    def setUp(self):
        AnalyzedUrl.objects.create(url="http://example.com", domain="example.com")

    def test_analyzed_url(self):
        analyzed_url = AnalyzedUrl.objects.get(url="http://example.com")
        self.assertEqual(analyzed_url.domain, "example.com")

class AnalyzedUrlEmbeddingTestCase(TestCase):
    def setUp(self):
        analyzed_url = AnalyzedUrl.objects.create(url="http://example.com", domain="example.com")
        AnalyzedUrlEmbedding.objects.create(analyzed_url=analyzed_url, model="test-model")

    def test_analyzed_url_embedding(self):
        analyzed_url_embedding = AnalyzedUrlEmbedding.objects.get(analyzed_url__url="http://example.com")
        self.assertEqual(analyzed_url_embedding.model, "test-model")
