from django.db.models.signals import post_save
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.auth.signals import user_logged_in, user_logged_out, user_login_failed
from django.dispatch import receiver
from .models import Customer,Logbook
import logging


@receiver(post_save, sender=User)
def create_customer(sender, instance, created, **kwargs):
    if created:
        Customer.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_customer(sender, instance, **kwargs):
    instance.customer.save()


# Track user logins according to https://stackoverflow.com/questions/37618473/how-can-i-log-both-successful-and-failed-login-and-logout-attempts-in-django
known_IPs = { 'localhost':'127.0.0.1',
              'TU office':'145.94.159.42',
              'Kaz home': '83.86.147.113',
              }

@receiver(user_logged_in)
def user_logged_in_callback(sender, request, user, **kwargs):
    ip = request.META.get('REMOTE_ADDR')
    if ip not in known_IPs.values():
        Logbook.objects.create(action='user_logged_in', ip=ip, username=user.username)

@receiver(user_logged_out)
def user_logged_out_callback(sender, request, user, **kwargs):
    ip = request.META.get('REMOTE_ADDR')
    if ip not in known_IPs.values():
        Logbook.objects.create(action='user_logged_out', ip=ip, username=user.username)


@receiver(user_login_failed)
def user_login_failed_callback(sender, credentials, **kwargs):
        Logbook.objects.create(action='user_login_failed', username=credentials.get('username', None))
