from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.contrib.auth.signals import user_logged_in, user_logged_out, user_login_failed
from django.dispatch import receiver
from .models import Customer,Logbook


@receiver(post_save, sender=User)
def create_customer(sender, instance, created, **kwargs):
    if created:
        Customer.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_customer(sender, instance, **kwargs):
    instance.customer.save()


@receiver(user_logged_in)
def user_logged_in_callback(sender, request, user, **kwargs):
    ip = request.META.get('REMOTE_ADDR')
    Logbook.objects.create(action='user_logged_in', ip=ip, username=user.username)


@receiver(user_logged_out)
def user_logged_out_callback(sender, request, user, **kwargs):
    ip = request.META.get('REMOTE_ADDR')
    Logbook.objects.create(action='user_logged_out', ip=ip, username=user.username)


@receiver(user_login_failed)
def user_login_failed_callback(sender, credentials, **kwargs):
    Logbook.objects.create(action='user_login_failed', username=credentials.get('username', None))
