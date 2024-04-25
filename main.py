import logging
import sqlite3
from telegram.ext import Application, MessageHandler, filters, Updater, ConversationHandler
from telegram.ext import CommandHandler
from telegram import ReplyKeyboardMarkup
from config import BOT_TOKEN


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)

logger = logging.getLogger(__name__)


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
    await update.message.reply_text("Я пока не умею помогать...")


async def teacher(update, context):
    reply_keyboard = [['/createquiz', '/creategroup', '/results']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
    await update.message.reply_html(
        rf"Что хочешь сделать? Нажми /createquiz для создания нового квиза. "
        rf"Нажми /creategroup для создания новой группы. "
        rf"Нажми /results для просмотра результата.", reply_markup=markup
    )


async def student(update, context):
    reply_keyboard = [['Пройти викторину', 'Посмотреть результаты']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
    await update.message.reply_html('Выберите, что вы хотите сделать', reply_markup=markup)
    return studentсhoice


async def studentсhoice(update, context):
    reply_keyboard = []
    a = update.message.text
    if a == 'Пройти викторину':
        usernow = update.effective_user.username
        usersdb = []
        connection = sqlite3.connect('data/group.db')
        cursor = connection.cursor()
        cursor.execute('SELECT user, quizz FROM Users')
        user = cursor.fetchall()
        for user in user:
            usersdb.append(user[0])
            reply_keyboard.append([user[1]])
        if usernow in usersdb:
            markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
            await update.message.reply_text('Выбери квиз', reply_markup=markup)
            return quwest1
        connection.close()
    elif a == 'Посмотреть результаты':
        return ConversationHandler.END
        return results


async def quwest1(update, context):
    global qname
    global qu
    qname = update.message.text
    connection = sqlite3.connect('data/quiz.db')
    cursor = connection.cursor()
    cursor.execute(f'SELECT * FROM {qname}')
    qu = cursor.fetchall()
    st = qu[0]
    reply_keyboard = [[str(st[2]), str(st[3]), str(st[4]), str(st[5])]]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
    await update.message.reply_text(str(st[1]), reply_markup=markup)
    connection.close()
    return quwest2


async def quwest2(update, context):
    a = update.message.text
    global r
    r = 0
    connection = sqlite3.connect('data/quiz.db')
    cursor = connection.cursor()
    cursor.execute(f'SELECT answer1 FROM {qname}')
    ta = cursor.fetchall()
    if a == str(*ta[0]):
        r += 1
    connection.close()
    st = qu[1]
    reply_keyboard = [[str(st[2]), str(st[3]), str(st[4]), str(st[5])]]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
    await update.message.reply_text(str(st[1]), reply_markup=markup)
    return quwest3


async def quwest3(update, context):
    a = update.message.text
    connection = sqlite3.connect('data/quiz.db')
    cursor = connection.cursor()
    cursor.execute(f'SELECT answer1 FROM {qname}')
    ta = cursor.fetchall()
    if a == str(*ta[1]):
        r = 1
    connection.close()
    st = qu[2]
    reply_keyboard = [[str(st[2]), str(st[3]), str(st[4]), str(st[5])]]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
    await update.message.reply_text(str(st[1]), reply_markup=markup)
    return quwest4


async def quwest4(update, context):
    a = update.message.text
    connection = sqlite3.connect('data/quiz.db')
    cursor = connection.cursor()
    cursor.execute(f'SELECT answer1 FROM {qname}')
    ta = cursor.fetchall()
    if a == str(*ta[2]):
        r = 1
    connection.close()
    st = qu[3]
    reply_keyboard = [[str(st[2]), str(st[3]), str(st[4]), str(st[5])]]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
    await update.message.reply_text(str(st[1]), reply_markup=markup)
    return quwest5


async def quwest5(update, context):
    a = update.message.text
    connection = sqlite3.connect('data/quiz.db')
    cursor = connection.cursor()
    cursor.execute(f'SELECT answer1 FROM {qname}')
    ta = cursor.fetchall()
    if a == str(*ta[3]):
        r = 1
    connection.close()
    st = qu[4]
    reply_keyboard = [[str(st[2]), str(st[3]), str(st[4]), str(st[5])]]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
    await update.message.reply_text(str(st[1]), reply_markup=markup)
    return quwest6


async def quwest6(update, context):
    a = update.message.text
    connection = sqlite3.connect('data/quiz.db')
    cursor = connection.cursor()
    cursor.execute(f'SELECT answer1 FROM {qname}')
    ta = cursor.fetchall()
    if a == str(*ta[4]):
        r = 1
    connection.close()
    st = qu[5]
    reply_keyboard = [[str(st[2]), str(st[3]), str(st[4]), str(st[5])]]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
    await update.message.reply_text(str(st[1]), reply_markup=markup)
    return quwest7


async def quwest7(update, context):
    a = update.message.text
    connection = sqlite3.connect('data/quiz.db')
    cursor = connection.cursor()
    cursor.execute(f'SELECT answer1 FROM {qname}')
    ta = cursor.fetchall()
    if a == str(*ta[5]):
        r = 1
    connection.close()
    st = qu[6]
    reply_keyboard = [[str(st[2]), str(st[3]), str(st[4]), str(st[5])]]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
    await update.message.reply_text(str(st[1]), reply_markup=markup)
    return quwest8


async def quwest8(update, context):
    a = update.message.text
    connection = sqlite3.connect('data/quiz.db')
    cursor = connection.cursor()
    cursor.execute(f'SELECT answer1 FROM {qname}')
    ta = cursor.fetchall()
    if a == str(*ta[6]):
        r = 1
    connection.close()
    st = qu[7]
    reply_keyboard = [[str(st[2]), str(st[3]), str(st[4]), str(st[5])]]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
    await update.message.reply_text(str(st[1]), reply_markup=markup)
    return quwest9


async def quwest9(update, context):
    a = update.message.text
    connection = sqlite3.connect('data/quiz.db')
    cursor = connection.cursor()
    cursor.execute(f'SELECT answer1 FROM {qname}')
    ta = cursor.fetchall()
    if a == str(*ta[7]):
        r = 1
    connection.close()
    st = qu[8]
    reply_keyboard = [[str(st[2]), str(st[3]), str(st[4]), str(st[5])]]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
    await update.message.reply_text(str(st[1]), reply_markup=markup)
    return quwest10


async def quwest10(update, context):
    a = update.message.text
    connection = sqlite3.connect('data/quiz.db')
    cursor = connection.cursor()
    cursor.execute(f'SELECT answer1 FROM {qname}')
    ta = cursor.fetchall()
    if a == str(*ta[8]):
        r = 1
    connection.close()
    st = qu[9]
    reply_keyboard = [[str(st[2]), str(st[3]), str(st[4]), str(st[5])]]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
    await update.message.reply_text(str(st[1]), reply_markup=markup)
    return resultq


async def resultq(update, context):
    a = update.message.text
    username = update.effective_user.first_name
    connection = sqlite3.connect('data/quiz.db')
    cursor = connection.cursor()
    cursor.execute(f'SELECT answer1 FROM {qname}')
    ta = cursor.fetchall()
    if a == str(*ta[9]):
        r = 1
    connection.close()
    connection = sqlite3.connect('data/result.db')
    cursor = connection.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Users (
        id INTEGER PRIMARY KEY,
        user TEXT NOT NULL,
        quizname TEXT NOT NULL,
        quizres TEXT NOT NULL
        )
        ''')
    cursor.execute(f'''INSERT INTO Users (user, quizname, quizres) VALUES (?, ?, ?)''', (username, qname, r))
    connection.close()
    await update.message.reply_text(f'Поздравляю, вы прошли квиз!')
    return ConversationHandler.END


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
    await update.message.reply_text(rf"Введите квиза в котором должны учавствовать пользователи")
    return addq


async def addq(update, context):
    global qname
    qname = update.message.text
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
    user TEXT NOT NULL,
    quizz TEXT NOT NULL
    )
    ''')
    cursor.execute(f'''INSERT INTO Users (user, quizz) VALUES (?, ?)''', (username, qname))
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
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('student', student)],

        states={
            studentсhoice: [MessageHandler(filters.TEXT & ~filters.COMMAND, studentсhoice)],
            quwest1: [MessageHandler(filters.TEXT & ~filters.COMMAND, quwest1)],
            quwest2: [MessageHandler(filters.TEXT & ~filters.COMMAND, quwest2)],
            quwest3: [MessageHandler(filters.TEXT & ~filters.COMMAND, quwest3)],
            quwest4: [MessageHandler(filters.TEXT & ~filters.COMMAND, quwest4)],
            quwest5: [MessageHandler(filters.TEXT & ~filters.COMMAND, quwest5)],
            quwest6: [MessageHandler(filters.TEXT & ~filters.COMMAND, quwest6)],
            quwest7: [MessageHandler(filters.TEXT & ~filters.COMMAND, quwest7)],
            quwest8: [MessageHandler(filters.TEXT & ~filters.COMMAND, quwest8)],
            quwest9: [MessageHandler(filters.TEXT & ~filters.COMMAND, quwest9)],
            quwest10: [MessageHandler(filters.TEXT & ~filters.COMMAND, quwest10)],
            resultq: [MessageHandler(filters.TEXT & ~filters.COMMAND, resultq)],
        },

        fallbacks=[CommandHandler("cancel", cancel)],
    )
    application.add_handler(conv_handler)
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
            addq: [MessageHandler(filters.TEXT & ~filters.COMMAND, addq)],
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