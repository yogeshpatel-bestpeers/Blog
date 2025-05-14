from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.timezone import now

from .models import Comment, CustomUser, Notification
from .utils import send_custom_email

@receiver(post_save, sender=CustomUser)
def create_profile(sender, instance, created, **kwargs):
    if created:
        if created:
            print('singal created')
            send_custom_email.delay(
                subject="Welcome to the Blogger!",
                message="Your account has been created successfully.",
                recipient_email=instance.email,
            )


@receiver(post_save, sender=Comment)
def on_comment(sender, instance, created, **kwargs):
    print(created)
    if created:
        if instance.user.id != instance.blog.user.id:
            Notification.objects.create(
                user=instance.blog.user,
                message=f"{instance.user.username} commented: {instance.content}",
                timestamp=now(),
            )
