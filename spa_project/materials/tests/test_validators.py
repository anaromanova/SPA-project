from django.core.exceptions import ValidationError
from django.test import TestCase

from spa_project.materials.validators import (
    validate_only_youtube_links,
    validate_youtube_url
)

class ValidatorsTestCase(TestCase):

    def test_only_youtube_links_valid(self):
        text = (
            "Смотрите видео: "
            "https://www.youtube.com/watch?v=dQw4w9WgXcQ "
            "и https://youtu.be/dQw4w9WgXcQ"
        )
        try:
            validate_only_youtube_links(text)
        except ValidationError:
            self.fail("validate_only_youtube_links() unexpectedly raised ValidationError")

    def test_only_youtube_links_invalid(self):
        invalids = [
            "Ссылка на Google: https://google.com",
            "http://example.org/video",
            "Видео здесь: https://vimeo.com/123456",
        ]
        for text in invalids:
            with self.assertRaises(ValidationError):
                validate_only_youtube_links(text)

    def test_validate_youtube_url_valid(self):
        valids = [
            "https://www.youtube.com/watch?v=abcdef",
            "http://youtube.com/watch?v=abcdef",
            "https://youtu.be/abcdef",
        ]
        for url in valids:
            try:
                validate_youtube_url(url)
            except ValidationError:
                self.fail(f"validate_youtube_url('{url}') unexpectedly raised ValidationError")

    def test_validate_youtube_url_invalid(self):
        invalids = [
            "https://example.com/watch?v=abcdef",
            "ftp://youtube.com/video",
            "https://youtu.be.evil.com/abcdef",
        ]
        for url in invalids:
            with self.assertRaises(ValidationError):
                validate_youtube_url(url)

