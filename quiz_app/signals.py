from django.contrib.auth.signals import user_logged_out
from django.dispatch import receiver
from django.contrib import messages

@receiver(user_logged_out)
def logout_message(sender, request, user, **kwargs):
    messages.success(request, "You have been logged out successfully.")
