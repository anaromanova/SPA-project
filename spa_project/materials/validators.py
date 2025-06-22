import re
from urllib.parse import urlparse
from django.core.exceptions import ValidationError

URL_PATTERN = re.compile(r'https?://[^\s]+', re.IGNORECASE)

def validate_only_youtube_links(value):
    """
    Проверяет, что в переданном тексте нет ссылок,
    кроме youtube.com и youtu.be.
    """
    urls = URL_PATTERN.findall(value or "")
    for url in urls:
        host = urlparse(url).netloc.lower()
        if not (host.endswith("youtube.com") or host == "youtu.be"):
            raise ValidationError(
                "Найдена недопустимая ссылка «{0}»: "
                "можно использовать только YouTube-видео.".format(url)
            )

def validate_youtube_url(value):
    """
    Проверяет, что URL — это ссылка на YouTube.
    """
    parsed = urlparse(value)
    scheme = parsed.scheme.lower()
    host = parsed.netloc.lower()

    if scheme not in ("http", "https") or not (host.endswith("youtube.com") or host == "youtu.be"):
        raise ValidationError("Поле «видео» должно содержать ссылку на YouTube.")

