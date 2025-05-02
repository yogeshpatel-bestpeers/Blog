import requests
from django.core.management.base import BaseCommand

from Blog.models import CustomUser


class Command(BaseCommand):
    help = "Resets user password by sending a reset link"

    def add_arguments(self, parser):
        parser.add_argument("email", type=str)

    def handle(self, *args, **options):
        email = options["email"]

        try:
            response = requests.post(
                "http://127.0.0.1:8000/api/password-reset/request/",
                data={"email": email},
                timeout=30,
            )

            if response.status_code == 200:
                self.stdout.write(
                    self.style.SUCCESS(
                        f"Password reset email triggered successfully for {email}."
                    )
                )
            else:
                self.stdout.write(
                    self.style.ERROR(
                        f"API call failed: {response.status_code} {response.text}"
                    )
                )

        except requests.exceptions.RequestException as e:
            self.stdout.write(self.style.ERROR(f"Failed to contact the API: {str(e)}"))
