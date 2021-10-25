"""KU Poll's models."""

import datetime

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Question(models.Model):
    """
    This model specifies the question and the duration of a poll.

    It includes the question text, the start date, and the end date of the poll.
    """

    text = models.CharField(max_length=500)
    start_date = models.DateTimeField('starting date')
    end_date = models.DateTimeField('ending date')

    def __str__(self):
        """Return the model's description."""
        return self.text

    def was_published_recently(self):
        """Check if a poll was published recently."""
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.start_date <= now

    def is_published(self):
        """Check if a poll is published."""
        return timezone.now() >= self.start_date

    def can_vote(self):
        """Check if a poll is within the voting period."""
        if self.is_published() and timezone.now() <= self.end_date:
            return True
        return False


class Choice(models.Model):
    """
    This model specifies a singular choice of a poll.

    It includes the choice's text, the amount of votes the choice receives, and the question it is related to.
    """

    question = models.ForeignKey(Question, on_delete=models.CASCADE)  # Links to a Question model
    text = models.CharField(max_length=500)

    def __str__(self):
        """Return the model's description."""
        return self.text

    @property
    def votes(self):
        count = Vote.objects.filter(choice=self).count()
        return count


class Vote(models.Model):
    """Represents a vote made by a user."""

    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)

    def __str__(self):
        return f"Voted by {self.user.username} for {self.choice.text}"
