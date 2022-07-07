import datetime

from django.utils import timezone
from telegram import ParseMode, Update,ReplyKeyboardRemove
from telegram.ext import CallbackContext

from tgbot.handlers.exam import static_text
from tgbot.models import User
from exam.models import Exam
from question.models import Question
from tgbot.handlers.exam import keyboards


def exam_start(update: Update, context: CallbackContext) -> None:
    exams = Exam.objects.all()
    inline_keyboard = keyboards.exam_keyboard(exams)
    update.message.reply_text(
        text=static_text.exam_start, reply_markup=inline_keyboard)


def exam_callback(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    data = update.callback_query.data.split("-")
    exam_id = data[2]
    query.answer()
    query.delete_message()
    query.message.reply_text(static_text.exam_start_after_click,reply_markup=ReplyKeyboardRemove())
    question = Question.objects.all().first()
    options = []
    for option in question.options.all():
        options.append(option.title)
    query.message.reply_poll(question.title,options,correct_option_id=1)
