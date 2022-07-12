from django.db import models

# Create your models here.

SINGLE = "single"
MULTIPLE = "multiple"
QUESTION_CHOICE = (
    (SINGLE, "Bittalik savollar"),
    (MULTIPLE, "Ko'p savollar"),
)


class Question(models.Model):
    title = models.CharField(max_length=256)
    content = models.TextField(max_length=2048)
    type = models.CharField(
        max_length=16, choices=QUESTION_CHOICE, default=SINGLE)
    time = models.IntegerField(
        "Savolar uchun mo'ljallangan vaqt(sekund)", default=10)


class QuestionOption(models.Model):
    title = models.CharField(max_length=256)
    is_correct = models.BooleanField(default=False)
    questions = models.ForeignKey(Question,related_name="options", on_delete=models.CASCADE)


