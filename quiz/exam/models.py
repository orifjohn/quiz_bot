from enum import auto
from django.db import models
from question.models import Question, QuestionOption
from tgbot.models import User
# Create your models here.


class Exam(models.Model):
    title = models.CharField(max_length=256)
    content = models.TextField(max_length=2048)
    questions = models.ManyToManyField(Question)
    questions_count = models.IntegerField(
        "Savollar soni", default=20)
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()
    duration = models.IntegerField("Imtixon vaqti (minut)", default=20)

    class Meta:
        verbose_name = "Imtixon"
        verbose_name_plural = "Imtixonlar"

    def create_user_exam(self, user):
        userexam = UserExam.objects.create(exam=self, user=user)
        userexam.questions.set(self.questions.all(
        ).order_by("?")[:self.questions_count])
        return userexam


class UserExam(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    questions = models.ManyToManyField(Question)  # editable=False
    score = models.IntegerField(default=0)
    start_datetime = models.DateTimeField(auto_now_add=True)
    end_datetime = models.DateTimeField(null=True)
    is_finished = models.BooleanField(default=False)

    def update_score(self):
        UserExam.objects.filter(id=self.id).update(
            score=UserExamAnswer.objects.filter(is_correct=True, user_answer=self).count())

    def create_answers(self):
        exam_answers = []
        for question in self.questions.all().order_by("?"):
            exam_answers.append(UserExamAnswer(
                user_answer=self, question=question))
        UserExamAnswer.objects.bulk_create(exam_answers)

    def last_unanswered_question(self):
        user_exam_answer = self.answer.all().exclude(answered=True).first()
        return user_exam_answer.question if user_exam_answer else None

    def last_unanswered(self):
        user_exam_answer = self.answer.all().exclude(answered=True).first()
        return user_exam_answer


class UserExamAnswer(models.Model):
    user_answer = models.ForeignKey(
        UserExam, on_delete=models.CASCADE, related_name="answer")
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    option_ids = models.CharField(max_length=255, null=True)
    answered = models.BooleanField(default=False)
    is_correct = models.BooleanField(default=False)
