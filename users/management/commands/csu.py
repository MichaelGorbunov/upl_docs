from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):

    def handle(self, *args, **options):
        User = get_user_model()
        user = User.objects.create(
            username="SuperUser",
            email="admin@webstore.ru",
            first_name="SUser",
            last_name="ADMIN",
        )
        user.set_password("123456789")
        user.is_staff = True
        user.is_superuser = True
        user.save()
