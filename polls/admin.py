"""Specifies models to be added to the administration page."""

from django.contrib import admin
from .models import *

admin.site.register(Question)
admin.site.register(Choice)
admin.site.register(Vote)
