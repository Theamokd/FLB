from django.apps import AppConfig


class ProfilesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "flb.profiles"

    def ready(self):
        import flb.profiles.signals  # noqa
