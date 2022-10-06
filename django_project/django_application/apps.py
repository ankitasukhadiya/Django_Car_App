from django.apps import AppConfig

class django_applicationConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'django_application'
    
    def ready(self):
        import django_application.signals
