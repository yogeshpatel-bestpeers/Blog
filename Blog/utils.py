from django.conf import settings
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import send_mail
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode
from django.core.mail import send_mail
from django.conf import settings
from celery import shared_task

@shared_task
def send_custom_email(subject, message, recipient_email):
    print("This is a task from utils.py")
    send_mail(
        subject=subject,
        message=message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[recipient_email],
        fail_silently=False,
    )



def generate_password_reset_link(user, request):
    print("request", request)
    token_generator = PasswordResetTokenGenerator()
    token = token_generator.make_token(user)
    uid = urlsafe_base64_encode(str(user.pk).encode())

    reset_path = reverse(
        "custom_password_reset_confirm",
        kwargs={"uidb64": uid, "token": token},
    )
    reset_url = request.build_absolute_uri(reset_path)
    return reset_url


login_url = "/blog/login/"
home_url = "/blog/home/"
category_url = "/blog/Category/"
userprofile_url = "/blog/userblog/"
blog_page = "blogpage"
