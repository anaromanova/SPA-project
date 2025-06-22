from django.db import models
from django.conf import settings
from .validators import validate_only_youtube_links, validate_youtube_url


class Course(models.Model):
    title = models.CharField(max_length=255)
    preview = models.ImageField(upload_to='course_previews/', blank=True, null=True)
    description = models.TextField("Описание курса",
                                   blank=True,
                                   validators=[validate_only_youtube_links],
                                   help_text="Запрещены ссылки, кроме YouTube.")
    user = models.ForeignKey(
                settings.AUTH_USER_MODEL,
                on_delete = models.CASCADE,
                related_name = 'courses',
                null=False, blank=False,
                                )

    def __str__(self):
        return self.title


class Lesson(models.Model):
    course = models.ForeignKey(Course, related_name='lessons', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField(
        "Материалы урока",
        blank=True,
        validators=[validate_only_youtube_links],
        help_text="Запрещены ссылки, кроме YouTube."
    )
    preview = models.ImageField(upload_to='lesson_previews/', blank=True, null=True)
    video_url = models.URLField(
        "Ссылка на видео",
        validators=[validate_youtube_url],
        help_text="Сюда можно вставить только YouTube-ссылку."
    )
    user = models.ForeignKey(
                settings.AUTH_USER_MODEL,
               on_delete = models.CASCADE,
                related_name = 'lessons',
                null=False, blank=False,
                                )

    def __str__(self):
        return f"{self.title} ({self.course.title})"


class Subscription(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='subscriptions'
    )
    course = models.ForeignKey(
        'Course',
        on_delete=models.CASCADE,
        related_name='subscribers'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'course')
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.user} → {self.course}'

