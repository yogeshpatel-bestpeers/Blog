from django.core.management.base import BaseCommand
from Blog.models import CustomUser


class Command(BaseCommand):
    help = "Create a new user"

    def add_arguments(self, parser):
        parser.add_argument("username", type=str)
        parser.add_argument("email", type=str)
        parser.add_argument("password", type=str)

    def handle(self, *args, **kwargs):
        username = kwargs["username"]
        email = kwargs["email"]
        password = kwargs["password"]

        user = CustomUser.objects.create_user(
            username=username, email=email, password=password
        )
        user.save()
        self.stdout.write(self.style.SUCCESS(f'User "{username}" created successfully'))
