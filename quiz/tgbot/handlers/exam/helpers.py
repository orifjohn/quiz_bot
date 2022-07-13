
def send_exam_poll(context, question, chat_id):
    # POLL OPTIONS
    options = []
    correct_option_id = 0
    for index, option, in enumerate(question.options.all().order_by("?")):
        options.append(option.title)
        if option.is_correct:
            correct_option_id = index

    message = context.bot.send_poll(chat_id,
                                    question.title, options, type="quiz", correct_option_id=correct_option_id)
    # SAVE POLL ID WITH CHAT ID
    context.bot_data.update({message.poll.id: message.chat.id})


def get_chat_id(update, context):
    chat_id = -1

    if update.message is not None:
        chat_id = update.message.chat.id
    elif update.callback_query is not None:
        chat_id = update.callback_query.message.chat.id
    elif update.poll is not None:
        chat_id = context.bot_data[update.poll.id]

    return chat_id
