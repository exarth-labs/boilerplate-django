from django.apps import AppConfig


class AccountsConfig(AppConfig):
    name = 'src.services.accounts'
    verbose_name = 'Account'
    verbose_name_plural = 'Accounts'
    default_auto_field = 'django.db.models.BigAutoField'

    def ready(self):
        import src.services.accounts.signals #noqa
