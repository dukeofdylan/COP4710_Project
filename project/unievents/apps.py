from django.apps import AppConfig


class UnieventsConfig(AppConfig):
    name = "unievents"

    def ready(self):
        import unievents.signals