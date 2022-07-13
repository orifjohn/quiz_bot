
from django.utils import timezone
from telegram import ParseMode, Update, ReplyKeyboardRemove
from telegram.ext import CallbackContext

from tgbot.handlers.exam import static_text
from tgbot.models import User
from exam.models import Exam, UserExam
from question.models import Question
from tgbot.handlers.exam import keyboards
from tgbot.handlers.exam import helpers


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

        helpers.send_exam_poll(context, question, user.user_id)

    elif action_type == "back":
        exam_start(update, context)


def poll_handler(update: Update, context: CallbackContext) -> None:
    # GETTING USER 
    user_id = helpers.get_chat_id(update, context)
    user = User.objects.get(user_id=user_id)
    
    # CHECKING ANSWER
    is_correct = False
    for index, option in enumerate(update.poll.options):
        if option.voter_count >= 1:
            if index == update.poll.correct_option_id:
                is_correct = True
            break
        
    # SAVE ANSWER
    user_exam = UserExam.objects.filter(user=user, is_finished=False).last()
    answer_question = user_exam.last_unanswered()
    answer_question.is_correct = is_correct
    answer_question.answered = True
    answer_question.save()
    
    question = user_exam.last_unanswered_question()

    helpers.send_exam_poll(context, question, user.user_id)
