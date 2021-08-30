import datetime
from django.db import models
from django.utils import timezone


class Question(models.Model):
    """This model specifies the question and the duration of a poll. It includes the question text and the
    start and end date of the poll.
    """
    text = models.CharField(max_length=500)
    start_date = models.DateTimeField('starting date')
    end_date = models.DateTimeField('ending date')

    def was_published_recently(self):
        return self.start_date >= timezone.now() - datetime.timedelta(days=1)

    def __str__(self):
        return self.text


class Choice(models.Model):
    """This model specifies a singular choice of a poll. It includes the choice's text, the amount of votes the choice
    receives, and the question it is related to.
    """
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.CharField(max_length=500)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.text
