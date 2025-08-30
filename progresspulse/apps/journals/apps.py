from django.apps import AppConfig

class JournalsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.journals'  # Change this to the full path
    verbose_name = 'Journals'