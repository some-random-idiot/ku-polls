"""Polls app's configurations."""

from django.apps import AppConfig


class PollsConfig(AppConfig):
    """Configures the polls app."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'polls'
