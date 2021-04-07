from django.apps import AppConfig


class UnieventsConfig(AppConfig):
    name = "unievents"

    def ready(self):
        from . import signals
        from . import templates