import logging
import sqlite3
from telegram.ext import Application, MessageHandler, filters, Updater, ConversationHandler
from telegram.ext import CommandHandler
from telegram import ReplyKeyboardMarkup
from datetime import *
from config import BOT_TOKEN


#logging.basicConfig(
#    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
#)
#
#logger = logging.getLogger(__name__)


async def start(update, context):
    """Отправляет сообщение когда получена команда /start"""
    user = update.effective_user
    reply_keyboard = [['/teacher', '/student']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
    await update.message.reply_html(
        rf"Привет {user.mention_html()}! Я бот для создания квизов/тестов. Кто ты ученик или учитель?", reply_markup=markup
    )


async def help_command(update, context):
    """Отправляет сообщение когда получена команда /help"""
    await update.message.reply_text("Я пока не умею помогать... Я только ваше эхо.")


async def teacher(update, context):
    reply_keyboard = [['/createquiz', '/creategroup', '/results']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
    await update.message.reply_html(
        rf"Что хочешь сделать? Нажми /createquiz для создания нового квиза. "
        rf"Нажми /creategroup для создания новой группы. "
        rf"Нажми /results для просмотра результата.", reply_markup=markup
    )


async def student(update, context):
    usernow = update.effective_user.first_name
    usersdb = []
    connection = sqlite3.connect('data/group.db')
    cursor = connection.cursor()
    cursor.execute('SELECT user FROM Users')
    user = cursor.fetchall()
    for user in user:
        usersdb.append(user[0])
    if usernow in usersdb:
        await update.message.reply_text("rhjcfdxbr")
        return quiz
    connection.close()


async def quiz(update, context):
    q = []
    connection = sqlite3.connect('data/quiz.db')
    cursor = connection.cursor()
    cursor.execute(f'SELECT * FROM {namequiz}')
    user = cursor.fetchall()
    for user in user:
        q.append(user)
        await update.message.reply_text(user)
    print(q)
    connection.close()


async def create_a_quiz(update, context):
    reply_keyboard = [['/Newquiz', '/deletequize']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    await update.message.reply_html(rf"Нажми /Newquiz для создания квиза. "
                                    rf"Нажми /deletequize для удаления квиза.", reply_markup=markup)


async def Newquiz(update, context):
    await update.message.reply_text(rf"Введите название квиза.")
    return newnamequiz


async def newnamequiz(update, context):
    global namequiz
    namequiz = update.message.text
    await update.message.reply_text(rf"Введите впорос")
    return newquestion


async def newquestion(update, context):
    global namequstion
    namequstion = update.message.text
    await update.message.reply_text(rf"Введите правильный ответ")
    return answer1


async def answer1(update, context):
    global a1
    a1 = update.message.text
    await update.message.reply_text(rf"Введите ответ2")
    return answer2


async def answer2(update, context):
    global a2
    a2 = update.message.text
    await update.message.reply_text(rf"Введите ответ3")
    return answer3


async def answer3(update, context):
    global a3
    a3 = update.message.text
    await update.message.reply_text(rf"Введите ответ4")
    return answer4


async def answer4(update, context):
    a4 = update.message.text
    connection = sqlite3.connect('data/quiz.db')
    cursor = connection.cursor()
    cursor.execute(f"""
                    CREATE TABLE IF NOT EXISTS {namequiz}(
                    id INTEGER PRIMARY KEY,
                    question TEXT NOT NULL,
                    answer1 TEXT NOT NULL,
                    answer2 TEXT NOT NULL,
                    answer3 TEXT NOT NULL,
                    answer4 TEXT NOT NULL
                    )
                    """)
    cursor.execute(f'''INSERT INTO {namequiz} (question, answer1, answer2, answer3, answer4) VALUES (?, ?, ?, ?, ?)''', (namequstion, a1, a2, a3, a4))
    connection.commit()
    connection.close()
    await update.message.reply_text(rf"Следующий вопрос. Выйти из режима ввод вопроса нажмите /cancel.")
    return newquestion


async def deletequize(update, context):
    await update.message.reply_text(rf"Введите название квиза, которой надо удалить.")
    return deleteq


async def deleteq(update, context):
    quizname = update.message.text
    connection = sqlite3.connect('data/quiz.db')
    cursor = connection.cursor()
    cursor.execute(f'''DROP TABLE {quizname}''')
    connection.commit()
    connection.close()
    await update.message.reply_text(rf"Введите название квиза, которой надо удалить."
                                    rf"Выйти из режима ввод вопроса нажмите /cancel.")
    return deleteq


async def cancel(update, context):
    reply_keyboard = [['/createquiz', '/creategroup', '/results']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
    await update.message.reply_html(
        rf"Что хочешь сделать? Нажми /createquiz для создания нового квиза. "
        rf"Нажми /creategroup для создания новой группы. "
        rf"Нажми /results для просмотра результата.", reply_markup=markup
    )
    return ConversationHandler.END


async def create_a_group(update, context):
    reply_keyboard = [['/Newgroup', '/deletegroup']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
    await update.message.reply_html(rf" Я эхо-бот. Напишите мне что-нибудь, и я пришлю это назад!", reply_markup=markup)


async def Newgroup(update, context):
    await update.message.reply_text(rf"Введите нового пользователя группы.")
    return adduser


async def adduser(update, context):
    username = update.message.text
    connection = sqlite3.connect('data/group.db')
    cursor = connection.cursor()
    # Добавляем нового пользователя
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Users (
    id INTEGER PRIMARY KEY,
    user TEXT NOT NULL
    )
    ''')
    cursor.execute(f'''INSERT INTO Users (user) VALUES (?)''', (username, ))
    connection.commit()
    connection.close()
    await update.message.reply_text(rf"Введите нового пользователя группы."
                                    rf"Выйти из режима ввод вопроса нажмите /cancel.")
    return adduser


async def deletegroup(update, context):
    await update.message.reply_text(rf"Введите пользователя группы, которого надо удалить из списка.")
    return deleteuser


async def deleteuser(update, context):
    username = update.message.text
    connection = sqlite3.connect('data/group.db')
    cursor = connection.cursor()
    cursor.execute(f'''DELETE FROM Users WHERE user = ?''', (username, ))
    connection.commit()
    connection.close()
    await update.message.reply_text(rf"Введите другого пользователя группы, которого надо удалить из списка."
                                    rf"Выйти из режима ввод вопроса нажмите /cancel.")
    return deleteuser


async def results(update, context):
    await update.message.reply_text("Я пока не умею помогать... Я только ваше эхо.")


def main():
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("teacher", teacher))
    application.add_handler(CommandHandler("student", student))
    application.add_handler(CommandHandler("createquiz", create_a_quiz))

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('Newquiz', Newquiz)],

        states={
            newnamequiz: [MessageHandler(filters.TEXT & ~filters.COMMAND, newnamequiz)],
            newquestion: [MessageHandler(filters.TEXT & ~filters.COMMAND, newquestion)],
            answer1: [MessageHandler(filters.TEXT & ~filters.COMMAND, answer1)],
            answer2: [MessageHandler(filters.TEXT & ~filters.COMMAND, answer2)],
            answer3: [MessageHandler(filters.TEXT & ~filters.COMMAND, answer3)],
            answer4: [MessageHandler(filters.TEXT & ~filters.COMMAND, answer4)],
        },

        fallbacks=[CommandHandler("cancel", cancel)],
    )
    application.add_handler(conv_handler)

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('deletequize', deletequize)],

        states={
            deleteq: [MessageHandler(filters.TEXT & ~filters.COMMAND, deleteq)],
        },

        fallbacks=[CommandHandler("cancel", cancel)],
    )
    application.add_handler(conv_handler)

    application.add_handler(CommandHandler("creategroup", create_a_group))

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('Newgroup', Newgroup)],

        states={
            adduser: [MessageHandler(filters.TEXT & ~filters.COMMAND, adduser)],
        },

        fallbacks=[CommandHandler("cancel", cancel)],
    )
    application.add_handler(conv_handler)

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('deletegroup', deletegroup)],

        states={
            deleteuser: [MessageHandler(filters.TEXT & ~filters.COMMAND, deleteuser)],
        },

        fallbacks=[CommandHandler("cancel", cancel)],
    )
    application.add_handler(conv_handler)

    application.add_handler(CommandHandler("results", results))
    application.run_polling()


if __name__ == '__main__':
    main()