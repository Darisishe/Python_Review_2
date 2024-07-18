from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import scrapping


def start(update, context):
    reply = 'Приветствуем!\nЧтобы начать, введите название интересующей вас станции и направление\n' \
            '(1 - на Москву, 2 - от Москвы):'
    context.bot.sendMessage(chat_id=update.effective_chat.id, text=reply)


def closestTrainRequest(update, context):
    words = update.message.text.split(' ')
    course = 'toMoscow' if words[-1] == '1' else 'fromMoscow'
    stationName = ' '.join(words[:-1])
    depTime = scrapping.closestTrain(stationName, course)

    if depTime == None:
        reply = 'Упс... Что-то пошло не так!\n' \
                'Попробуйте еще раз.'
    else:
        reply = 'Ближайший поезд отправляется в {}!'.format(depTime)
    context.bot.send_message(chat_id=update.effective_chat.id, text=reply)


updater = Updater(token='TOKEN')
dispatcher = updater.dispatcher

dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(MessageHandler(Filters.text & (~Filters.command), closestTrainRequest))

updater.start_polling()
