import datetime
from django.db import models
from django.utils import timezone


class Question(models.Model):
    """
    This model specifies the question and the duration of a poll. It includes the question text and the start and
    the end date of the poll.
    """
    text = models.CharField(max_length=500)
    start_date = models.DateTimeField('starting date')
    end_date = models.DateTimeField('ending date')

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.start_date <= now

    def is_published(self):
        return timezone.now() >= self.start_date

    def can_vote(self):
        if self.is_published() and timezone.now() <= self.end_date:
            return True
        return False

    def __str__(self):
        return self.text


class Choice(models.Model):
    """
    This model specifies a singular choice of a poll. It includes the choice's text, the amount of votes the choice
    receives, and the question it is related to.
    """
    question = models.ForeignKey(Question, on_delete=models.CASCADE)  # Links to the Question model
    text = models.CharField(max_length=500)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.text
