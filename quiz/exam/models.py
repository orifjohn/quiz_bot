from enum import auto
from django.db import models
from question.models import Question, QuestionOption, Subject
from tgbot.models import User
# Create your models here.


class Exam(models.Model):
    title = models.CharField(max_length=256)
    content = models.TextField(max_length=2048)
    subjects = models.ManyToManyField(Subject)
    questions = models.ManyToManyField(Question, editable=False)
    questions_count = models.IntegerField(
        "Savollar soni", default=20)
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()
    duration = models.IntegerField("Imtixon vaqti (minut)", default=20)

class UserExam(models.Model):
    exam = models.ForeignKey(Exam,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    score =models.IntegerField(default=0)
    start_datetime =models.DateTimeField(auto_now_add=True)
    end_datetime =models.DateTimeField(null=True)


class UserExamAnswer(models.Model):
    option_ids = models.CharField(max_length=255)