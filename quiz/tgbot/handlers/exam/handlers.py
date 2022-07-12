
from django.utils import timezone
from telegram import ParseMode, Update, ReplyKeyboardRemove
from telegram.ext import CallbackContext

from tgbot.handlers.exam import static_text
from tgbot.models import User
from exam.models import Exam
from question.models import Question
from tgbot.handlers.exam import keyboards


def exam_start(update: Update, context: CallbackContext) -> None:
    """
    TODO:
    - Pagination
    """
    exams = Exam.objects.all()
    inline_keyboard = keyboards.exam_keyboard(exams)

    if update.callback_query:
        update.callback_query.message.edit_text(
            text=static_text.exam_start, reply_markup=inline_keyboard,
            parse_mode=ParseMode.HTML
        )
    else:
        update.message.reply_text(
            text=static_text.exam_start, reply_markup=inline_keyboard)


def exam_callback(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    data = update.callback_query.data.split("-")
    exam_id = data[2]

    query.answer()
    exam = Exam.objects.get(id=exam_id)
    text = f"{exam.title}\n\n<i>{exam.content}</i>\n\n<b>Imtixonni boshlaymizmi?</b>"
    context.bot.edit_message_text(
        text=text,
        chat_id=update.callback_query.message.chat_id,
        message_id=update.callback_query.message.message_id,
        parse_mode=ParseMode.HTML,
        reply_markup=keyboards.exam_start_confirmation(exam)
    )


def exam_confirmation(update: Update, context: CallbackContext) -> None:
    user, _ = User.get_user_and_created(update, context)

    query = update.callback_query
    data = update.callback_query.data.split("-")
    exam_id = data[2]
    action_type = data[3]

    query.answer()
    if action_type == "start":
        exam = Exam.objects.get(id=exam_id)
        user_exam = exam.create_user_exam(user)
        user_exam.create_answers()
        question = user_exam.last_unanswered_question()

        query.delete_message()
        query.message.reply_text(
            static_text.exam_start_after_click, reply_markup=ReplyKeyboardRemove())
        options = []
        correct_option_id = 0
        for index, option, in enumerate(question.options.all().order_by("?")):
            options.append(option.title)
            if option.is_correct:
                correct_option_id = index
        query.message.reply_poll(
            question.title, options, type="quiz", correct_option_id=correct_option_id)

    elif action_type == "back":
        exam_start(update, context)
