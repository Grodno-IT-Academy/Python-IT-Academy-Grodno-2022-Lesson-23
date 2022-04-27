import datetime

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.
class Question(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    question_text = models.CharField(max_length=255)
    update_date = models.DateTimeField('date last updated', auto_now=True)
    pub_date = models.DateTimeField('date published', default=timezone.now)
    def __str__(self):
        return self.question_text
    # check if pulished recently
    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=255)
    votes = models.IntegerField(default=0)
    def __str__(self):
        return self.choice_text
