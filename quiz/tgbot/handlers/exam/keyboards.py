from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram import ReplyKeyboardMarkup, InlineKeyboardMarkup

from tgbot.handlers.onboarding.manage_data import SECRET_LEVEL_BUTTON
from tgbot.handlers.onboarding.static_text import EXAM_TITLE, BATTLE_TITLE



def exam_keyboard(exams) -> InlineKeyboardMarkup:
    buttons = []
    for exam in exams:
        buttons.append([InlineKeyboardButton(
            exam.title, callback_data=f'exam-start-{exam.id}'),])


    return InlineKeyboardMarkup(buttons)
