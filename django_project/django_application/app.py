from dataclasses import fields
from email.policy import default
from enum import auto
from django.apps import AppConfig

class CarConfig(AppConfig):
    default_auto_field = 'django.db.models.BigIntegerField'
    name = 'car'

    def ready(self):
        import car.signals