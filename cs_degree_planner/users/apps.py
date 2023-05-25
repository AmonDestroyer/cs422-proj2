from django.apps import AppConfig

class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'

    def ready(self):
        from .signals import handle_user_created, post_save, User
        post_save.connect(handle_user_created, sender=User)