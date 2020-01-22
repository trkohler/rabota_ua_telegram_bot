from telegram.ext import Updater, CommandHandler
import logging

import scrap

TOKEN = 'your token'
titles = scrap.titles
lines = scrap.lines_with_salaries

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


def start(update, context):
    text = 'Я бот, который скрапит сайт rabota.ua и доставляет тебе обновления.️\n\n' \
           'Воспользуйся командой /give_me ️\n'
    update.message.reply_text(text)

def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def give_me(update, context):
    jobs_list = scrap.create_custom_rabota(titles, lines)
    text = ''
    for i in jobs_list:
        text_part = f'👉  {i["title"]} \n' \
                    f'Ссылка: {i["link"]} \n'
        if i['salary'] > 0:
            text_part += f'Зарплату обещают {i["salary"]} грн  👯‍♀️\n\n'
        else:
            text_part += 'Зарплата не указана. 🤷‍♂️\n\n'
        text += text_part
    update.message.reply_text(text)


def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('give_me', give_me))
    updater.start_polling()
    print(updater.job_queue.jobs())
    updater.idle()


if __name__ == '__main__':
    main()
