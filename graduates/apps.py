from django.apps import AppConfig


class GraduatesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'graduates'
    def ready(self):
        import graduates.signals
