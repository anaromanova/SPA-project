from django.apps import AppConfig


class MaterialsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "spa_project.materials"

    def ready(self):
        import spa_project.materials.signals  # noqa