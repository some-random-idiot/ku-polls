"""Specifies which model should be added to the administration page."""

from django.contrib import admin
from .models import Question

admin.site.register(Question)
