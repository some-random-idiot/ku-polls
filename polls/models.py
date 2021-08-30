from django.db import models


class Question(models.Model):
    text = models.CharField(max_length=500)
    start_date = models.DateTimeField('starting date')
    end_date = models.DateTimeField('ending date')


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.CharField(max_length=500)
    votes = models.IntegerField(default=0)
