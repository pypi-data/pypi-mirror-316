from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class SageLanguageConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "sage_language"
    verbose_name = _("Language")

    def ready(self):
        from . import checks
