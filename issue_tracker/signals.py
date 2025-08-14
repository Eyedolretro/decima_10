# issue_tracker/signals.py
from django.contrib.auth.signals import user_login_failed
import logging

logger = logging.getLogger("myapp")

def log_failed_login(sender, credentials, request, **kwargs):
    username = credentials.get('username', '<unknown>')
    ip = request.META.get('REMOTE_ADDR')
    logger.warning(f"Échec login pour {username} depuis {ip}")

user_login_failed.connect(log_failed_login)
