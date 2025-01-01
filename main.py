import logging
import json
import os.path
import sqlite3
from telegram.ext import Application, MessageHandler, filters, Updater, ConversationHandler
from telegram.ext import CommandHandler
from telegram import ReplyKeyboardMarkup
from config import BOT_TOKEN


##logging.basicConfig(
##    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
##)
##
##logger = logging.getLogger(__name__)


async def start(update, context):
    """Отправляет сообщение когда получена команда /start"""
    user = update.effective_user
    textpr = f'Привет {user.mention_html()}! \nЯ бот для создания тестов. \nКто ты ученик или учитель? \n'
    reply_keyboard = [['/teacher', '/student']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
    await update.message.reply_html(rf"{textpr}", reply_markup=markup)


async def help_command(update, context):
    """Отправляет сообщение когда получена команда /help"""
    await update.message.reply_text("Я пока не умею помогать...")


async def teacher(update, context):
    usernow = update.effective_user.username
    us = []
    if os.path.exists('data/teachers.json'):
        with open('data/teachers.json', 'r', encoding='utf-8') as outfile:
            res = json.load(outfile)
            for i in res:
                us.append(i)
            if usernow not in us:
                res[usernow] = []
                result = {
                    'quiznow': '',
                    'quizes': [],
                    'groups': [],
                    'groupnow': '',
                    'count': 0
                }
                res[usernow].append(result)
                with open('data/teachers.json', 'w', encoding='utf-8') as outfile:
                    json.dump(res, outfile, ensure_ascii=False)
    else:
        data = {}
        data[usernow] = []
        result = {
            'quiznow': '',
            'quizes': [],
            'groups': [],
            'groupnow': '',
            'count': 0
        }
        data[usernow].append(result)
        with open('data/teachers.json', 'w', encoding='utf-8') as outfile:
            json.dump(data, outfile, ensure_ascii=False)
    textb = '''
        Что хочешь сделать?\n
        Нажми /createtest для создания нового теста.\n
        Нажми /viewtests для просмотра существующих тестов.\n
        Нажми /creategroup для создания новой группы.\n
        Нажми /viewgroups для просмотра существующих групп.\n
        Нажми /results для просмотра результата.\n
    '''
    reply_keyboard = [['/createtest'], ['/viewtests'], ['/creategroup'], ['/viewgroups'], ['/results']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
    await update.message.reply_html(rf"{textb}", reply_markup=markup)


async def student(update, context):
    usernow = update.effective_user.username
    us = []
    if os.path.exists('data/students.json'):
        with open('data/students.json', 'r', encoding='utf-8') as outfile:
            data = json.load(outfile)
            for i in data:
                us.append(i)
            if usernow not in us:
                data[usernow] = []
                result = {
                    'quiznow': '',
                    'quizes': [],
                    'groups': [],
                    'groupnow': '',
                    'count': 0
                }
                data[usernow].append(result)
                with open('data/students.json', 'w', encoding='utf-8') as outfile:
                    json.dump(data, outfile, ensure_ascii=False)
    else:
        res = {}
        res[usernow] = []
        result = {
            'quiznow': '',
            'quizes': [],
            'groups': [],
            'groupnow': '',
            'count': 0
        }
        res[usernow].append(result)
        with open('data/students.json', 'w', encoding='utf-8') as outfile:
            json.dump(res, outfile, ensure_ascii=False)
    reply_keyboard = [['/Taketest'], ['/Viewresults']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
    await update.message.reply_html('Выберите, что вы хотите сделать', reply_markup=markup)


async def studentсhoice(update, context):
    reply_keyboard = []
    usernow = update.effective_user.username
    with open('data/students.json', 'r+', encoding='utf-8') as outfile:
        resq = json.load(outfile)
        usern = resq[usernow]
        sl = usern[0]
        sl['count'] = 0
    with open('data/students.json', 'w', encoding='utf-8') as outfile:
        json.dump(resq, outfile, ensure_ascii=False)
    connection = sqlite3.connect('data/group.db')
    cursor = connection.cursor()
    cursor.execute('SELECT quizz FROM Users WHERE user = ?', (usernow, ))
    userr = cursor.fetchall()
    for user in userr:
        if [user[0]] not in reply_keyboard:
            reply_keyboard.append([user[0]])
    if reply_keyboard != []:
        markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
        await update.message.reply_text('Выбери тест', reply_markup=markup)
        return quwest1
    elif reply_keyboard == []:
        await update.message.reply_text('Нет тестов')
        reply_keyboard = [['/Taketest'], ['/Viewresults']]
        markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
        await update.message.reply_html('Выберите, что вы хотите сделать', reply_markup=markup)
        return ConversationHandler.END
    connection.close()


async def stedentresult(update, context):
    reply_keyboard = []
    usernow = update.effective_user.username
    connection = sqlite3.connect('data/group.db')
    cursor = connection.cursor()
    cursor.execute('SELECT quizz FROM Users WHERE user = ?', (usernow, ))
    userr = cursor.fetchall()
    for user in userr:
        if [user[0]] not in reply_keyboard:
            reply_keyboard.append([user[0]])
    if reply_keyboard != []:
        markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
        await update.message.reply_text('Выбери тест', reply_markup=markup)
        return result
    elif reply_keyboard == []:
        await update.message.reply_text('Нет тестов')
        reply_keyboard = [['/Taketest'], ['/Viewresults']]
        markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
        await update.message.reply_html('Выберите, что вы хотите сделать', reply_markup=markup)
        return ConversationHandler.END
    connection.close()


async def result(update, context):
    usernamer = update.effective_user.username
    qnameres = update.message.text
    if os.path.exists('data/result.db'):
        connection = sqlite3.connect('data/result.db')
        cursor = connection.cursor()
        cursor.execute('SELECT quizname FROM Users WHERE user = ?', (usernamer, ))
        r = cursor.fetchall()
        qres = []
        for i in r:
            if i[0] not in qres:
                qres.append(i[0])
        if qnameres in qres:
            cursor.execute('SELECT quizres FROM Users WHERE user = ? AND quizname = ?', (usernamer, qnameres))
            r = cursor.fetchall()
            t = r[0][0]
            connection.close()
            await update.message.reply_text(rf'Ваш результат: {t / 10 * 100}%')
        else:
            await update.message.reply_html('Вы ещё не проходили тест')
            reply_keyboard = [['/Taketest'], ['/Viewresults']]
            markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
            await update.message.reply_html('Выберите, что вы хотите сделать', reply_markup=markup)
            return ConversationHandler.END
        reply_keyboard = [['/Taketest'], ['/Viewresults']]
        markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
        await update.message.reply_html('Выберите, что вы хотите сделать', reply_markup=markup)
        return ConversationHandler.END
    else:
        await update.message.reply_html('ошибка')
        reply_keyboard = [['/Taketest'], ['/Viewresults']]
        markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
        await update.message.reply_html('Выберите, что вы хотите сделать', reply_markup=markup)
        return ConversationHandler.END


async def quwest1(update, context):
    r = 0
    resqu = []
    qname = update.message.text
    username = update.effective_user.username
    if os.path.exists('data/result.db'):
        connection = sqlite3.connect('data/result.db')
        cursor = connection.cursor()
        cursor.execute('SELECT quizname FROM Users WHERE user = ?', (username, ))
        resn = cursor.fetchall()
        for i in resn:
            resqu.append(i[0])
        connection.close()
    if qname in resqu:
            await update.message.reply_text('Вы уже прошли тест')
            reply_keyboard = [['/Taketest'], ['/Viewresults']]
            markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
            await update.message.reply_html('Выберите, что вы хотите сделать', reply_markup=markup)
            return ConversationHandler.END
    else:
        connection2 = sqlite3.connect('data/result.db')
        cursor2 = connection2.cursor()
        cursor2.execute(f'''
                            CREATE TABLE IF NOT EXISTS Users (
                            id INTEGER PRIMARY KEY,
                            user TEXT NOT NULL,
                            quizname TEXT NOT NULL,
                            quizres INT NOT NULL
                            )
                            ''')
        cursor2.execute(f'''INSERT INTO Users (user, quizname, quizres) VALUES (?, ?, ?)''', (username, qname, r))
        connection2.commit()
        connection2.close()
        connection3 = sqlite3.connect('data/quiz.db')
        cursor3 = connection3.cursor()
        cursor3.execute(f'SELECT * FROM {qname}')
        qu = cursor3.fetchall()
        st = qu[0]
        reply_keyboard = [[str(st[2])], [str(st[3])], [str(st[4])], [str(st[5])]]
        markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
        await update.message.reply_text(str(st[1]), reply_markup=markup)
        connection3.close()
        with open('data/students.json', 'r+', encoding='utf-8') as outfile:
            resq = json.load(outfile)
            usern = resq[username]
            sl = usern[0]
            sl['quiznow'] = qname
            sl['quizes'] = qu
        with open('data/students.json', 'w', encoding='utf-8') as outfile:
            json.dump(resq, outfile, ensure_ascii=False)
    return quwest2


async def quwest2(update, context):
    username = update.effective_user.username
    with open('data/students.json', 'r', encoding='utf-8') as outfile:
        resq = json.load(outfile)
        usern = resq[username]
        sl = usern[0]
        qname = sl.get('quiznow')
        qu = sl.get('quizes')
        res = sl.get('count')
    a = update.message.text
    connection = sqlite3.connect('data/quiz.db')
    cursor = connection.cursor()
    cursor.execute(f'SELECT answer1 FROM {qname}')
    ta = cursor.fetchall()
    if a == str(*ta[res]):
        connection = sqlite3.connect('data/result.db')
        cursor = connection.cursor()
        cursor.execute('SELECT quizres FROM Users WHERE user = ? AND quizname = ?', (username, qname))
        r = cursor.fetchall()
        t = r[0][0] + 1
        cursor.execute('UPDATE Users SET quizres = ? WHERE user = ?', (t, username))
        connection.commit()
        connection.close()
    connection.close()
    if res == 9:
        connection = sqlite3.connect('data/result.db')
        cursor = connection.cursor()
        cursor.execute('SELECT quizres FROM Users WHERE user = ? AND quizname = ?', (username, qname))
        r = cursor.fetchall()
        t = r[0][0]
        connection.close()
        await update.message.reply_text(rf'Поздравляю, вы прошли квиз!'
                                        rf'Ваш результат: {t / 10 * 100}%')
        reply_keyboard = [['/Taketest'], ['/Viewresults']]
        markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
        await update.message.reply_html('Выберите, что вы хотите сделать', reply_markup=markup)
        return ConversationHandler.END
    else:
        st = qu[res + 1]
        reply_keyboard = [[str(st[2])], [str(st[3])], [str(st[4])], [str(st[5])]]
        markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
        await update.message.reply_text(str(st[1]), reply_markup=markup)
        res += 1
        sl['count'] = res
        with open('data/students.json', 'w', encoding='utf-8') as outfile:
            json.dump(resq, outfile, ensure_ascii=False)
        return quwest2


async def viewgroups(update, context):
    reply_keyboard = []
    grname = []
    outgr = ''
    connection = sqlite3.connect('data/group.db')
    cursor = connection.cursor()
    cursor.execute('SELECT groupname FROM Users')
    groups = cursor.fetchall()
    for i in range(len(groups)):
        if groups[i][0] not in grname:
            grname.append(groups[i][0])
            outgr += groups[i][0] + '\n'
            reply_keyboard.append([groups[i][0]])
    await update.message.reply_text(rf'{outgr}')
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    await update.message.reply_text(rf'Выберите группу,в которой хотите посмотреть пользователей', reply_markup=markup)
    return viewgroup


async def viewgroup(update, context):
    groupname = update.message.text
    textout = '''
    Нажми /deltestforgroup для того, чтобы убрать тест для группы.
    Нажми /deluserfromgroup для удаления пользователя из группы.
    '''
    name = []
    outtextname = ''
    connection = sqlite3.connect('data/group.db')
    cursor = connection.cursor()
    cursor.execute('SELECT user FROM Users WHERE groupname = ?', (groupname,))
    names = cursor.fetchall()
    for i in range(len(names)):
        if names[i][0] not in name:
            name.append(names[i][0])
            outtextname += names[i][0] + '\n'
    await update.message.reply_text(rf'{outtextname}')
    connection.close()
    reply_keyboard = [['/deltestforgroup'], ['/deluserfromgroup']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    await update.message.reply_html(textout, reply_markup=markup)
    return ConversationHandler.END


async def deltestforgroup(update, context):
    reply_keyboard = []
    connection = sqlite3.connect('data/group.db')
    cursor = connection.cursor()
    cursor.execute('SELECT groupname FROM Users')
    groups = cursor.fetchall()
    for i in range(len(groups)):
        if [groups[i][0]] not in reply_keyboard:
            reply_keyboard.append([groups[i][0]])
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    await update.message.reply_html(rf"выбери группу для которой хотите удалить тест", reply_markup=markup)
    connection.close()
    return takenametest


async def takenametest(update, context):
    global groupnamedel
    groupnamedel = update.message.text
    reply_keyboard = []
    connection = sqlite3.connect('data/group.db')
    cursor = connection.cursor()
    cursor.execute('SELECT quizz FROM Users WHERE groupname = ?', (groupnamedel,))
    groups = cursor.fetchall()
    for i in range(len(groups)):
        if [groups[i][0]] not in reply_keyboard:
            reply_keyboard.append([groups[i][0]])
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    await update.message.reply_html(rf"выбери название теста, который хотите удалить для группы {groupnamedel}",
                                    reply_markup=markup)
    connection.close()
    return deletetestforgroup


async def deletetestforgroup(update, context):
    a = update.message.text
    connection = sqlite3.connect('data/group.db')
    cursor = connection.cursor()
    cursor.execute('DELETE FROM Users WHERE quizz = ? AND groupname = ?', (a, groupnamedel))
    connection.commit()
    connection.close()
    return ConversationHandler.END


async def deluserfromgroup(update, context):
    reply_keyboard = []
    connection = sqlite3.connect('data/group.db')
    cursor = connection.cursor()
    cursor.execute('SELECT groupname FROM Users')
    groups = cursor.fetchall()
    for i in range(len(groups)):
        if [groups[i][0]] not in reply_keyboard:
            reply_keyboard.append([groups[i][0]])
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    await update.message.reply_html(rf"выбери группу из которой хотите удалить пользователя", reply_markup=markup)
    connection.close()
    return choicegr


async def choicegr(update, context):
    global groupname
    groupname = update.message.text
    await update.message.reply_html(rf"Введите имя пользователя, котого хотите удалить из группы")
    return usernamedel


async def usernamedel(update, context):
    usname = update.message.text
    connection = sqlite3.connect('data/group.db')
    cursor = connection.cursor()
    cursor.execute('DELETE FROM Users WHERE user = ? AND groupname = ?', (usname, groupname))
    connection.commit()
    connection.close()
    await update.message.reply_text(rf"Введите пользователя группы, котого хотите удалить из группы."
                                    rf"Выйти из режима ввод вопроса нажмите /cancel.")
    return usernamedel


async def viewtests(update, context):
    reply_keyboard = []
    connection = sqlite3.connect('data/quiz.db')
    cursor = connection.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    table = cursor.fetchall()
    for i in range(len(table)):
        if [table[i][0]] not in reply_keyboard:
            reply_keyboard.append([table[i][0]])
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    await update.message.reply_html(rf"выбери название теста, который хотите посмотреть", reply_markup=markup)
    connection.close()
    return choiceview


async def choiceview(update, context):
    global testnamechoise
    testnamechoise = update.message.text
    outtext = ''
    connection = sqlite3.connect('data/quiz.db')
    cursor = connection.cursor()
    cursor.execute(f'SELECT * FROM {testnamechoise}')
    table = cursor.fetchall()
    for i in table:
        for j in i:
            outtext = outtext + str(j) + '\n'
    await update.message.reply_html(rf"{outtext}")
    reply_keyboard = [['/assignatest', '/removeatest']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    await update.message.reply_html(rf"Нажми /assignatest для назначения теста для группы./n"
                                    rf"Нажми /removeatest для отмены теста для группы",
                                    reply_markup=markup)
    connection.close()
    return ConversationHandler.END


async def assignatest(update, context):
    reply_keyboard = []
    connection = sqlite3.connect('data/group.db')
    cursor = connection.cursor()
    cursor.execute('SELECT groupname FROM Users')
    groups = cursor.fetchall()
    for i in range(len(groups)):
        if [groups[i][0]] not in reply_keyboard:
            reply_keyboard.append([groups[i][0]])
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    await update.message.reply_html(rf"выбери группу для которой хотите назначить тест", reply_markup=markup)
    connection.close()
    return assigntestforgroup


async def assigntestforgroup(update, context):
    a = update.message.text
    username = []
    connection = sqlite3.connect('data/group.db')
    cursor = connection.cursor()
    cursor.execute('SELECT user FROM Users WHERE groupname = ?', (a,))
    users = cursor.fetchall()
    for i in users:
        username.append(i[0])
    for i in username:
        cursor.execute('INSERT INTO Users (user, quizz, groupname) VALUES (?, ?, ?)', (i, testnamechoise, a))
    connection.commit()
    connection.close()
    return ConversationHandler.END


async def removeatest(update, context):
    reply_keyboard = []
    connection = sqlite3.connect('data/group.db')
    cursor = connection.cursor()
    cursor.execute('SELECT groupname FROM Users')
    groups = cursor.fetchall()
    for i in range(len(groups)):
        if [groups[i][0]] not in reply_keyboard:
            reply_keyboard.append([groups[i][0]])
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    await update.message.reply_html(rf"выбери группу для которой хотите убрать тест", reply_markup=markup)
    connection.close()
    return removetestforgroup


async def removetestforgroup(update, context):
    a = update.message.text
    username = []
    connection = sqlite3.connect('data/group.db')
    cursor = connection.cursor()
    cursor.execute('SELECT user FROM Users WHERE groupname = ?', (a,))
    users = cursor.fetchall()
    for i in users:
        username.append(i[0])
    for i in username:
        cursor.execute('DELETE FROM Users WHERE user = ? AND quizz = ? AND groupname = ?', (i, testnamechoise, a))
    connection.commit()
    connection.close()
    return ConversationHandler.END


async def create_a_test(update, context):
    textout = '''Нажми /Newquiz для создания квиза. \n Нажми /deletequize для удаления квиза.'''
    reply_keyboard = [['/Newquiz'], ['/deletequize']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    await update.message.reply_html(textout, reply_markup=markup)


async def Newquiz(update, context):
    await update.message.reply_text(rf"Введите название квиза.")
    return newnamequiz


async def newnamequiz(update, context):
    global namequiz
    namequiz = update.message.text
    await update.message.reply_text(rf"Введите впорос № 1")
    return newquestion


async def newquestion(update, context):
    global namequstion
    namequstion = update.message.text
    await update.message.reply_text(rf"Введите правильный ответ")
    return answer1


async def answer1(update, context):
    global a1
    a1 = update.message.text
    await update.message.reply_text(rf"Введите ответ 2")
    return answer2


async def answer2(update, context):
    global a2
    a2 = update.message.text
    await update.message.reply_text(rf"Введите ответ 3")
    return answer3


async def answer3(update, context):
    global a3
    a3 = update.message.text
    await update.message.reply_text(rf"Введите ответ 4")
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
    cursor.execute(f'''INSERT INTO {namequiz} (question, answer1, answer2, answer3, answer4) VALUES (?, ?, ?, ?, ?)''',
                   (namequstion, a1, a2, a3, a4))
    connection.commit()
    cursor.execute(f'''SELECT id FROM {namequiz}''')
    c = cursor.fetchall()
    countqwest = c[-1][0] + 1
    connection.close()
    if countqwest == 11:
        textb = '''
                Что хочешь сделать?\n
                Нажми /createtest для создания нового теста.\n
                Нажми /viewtests для просмотра существующих тестов.\n
                Нажми /creategroup для создания новой группы.\n
                Нажми /viewgroups для просмотра существующих групп.\n
                Нажми /results для просмотра результата.\n
            '''
        reply_keyboard = [['/createtest'], ['/viewtests'], ['/creategroup'], ['/viewgroups'], ['/results']]
        markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
        await update.message.reply_html(rf"{textb}", reply_markup=markup)
        return ConversationHandler.END
    else:
        await update.message.reply_text(rf"Введите вопрос № {countqwest}")
        return newquestion


async def cancel(update, context):
    textb = '''
            Что хочешь сделать?\n
            Нажми /createtest для создания нового теста.\n
            Нажми /viewtests для просмотра существующих тестов.\n
            Нажми /creategroup для создания новой группы.\n
            Нажми /viewgroups для просмотра существующих групп.\n
            Нажми /results для просмотра результата.\n
        '''
    reply_keyboard = [['/createtest'], ['/viewtests'], ['/creategroup'], ['/viewgroups'], ['/results']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
    await update.message.reply_html(rf"{textb}", reply_markup=markup)
    return ConversationHandler.END


async def create_a_group(update, context):
    await update.message.reply_text(rf"Введите название группы пользователей")
    return Newgroup


async def Newgroup(update, context):
    global grname
    grname = update.message.text
    await update.message.reply_text(rf"Введите название теста в котором должны учавствовать пользователи")
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
                    quizz TEXT NOT NULL,
                    groupname TEXT NOT NULL
                    )
    ''')
    cursor.execute('''INSERT INTO Users (user, quizz, groupname) VALUES (?, ?, ?)''', (username, qname, grname))
    connection.commit()
    connection.close()
    await update.message.reply_text(rf"Введите нового пользователя группы."
                                    rf"Выйти из режима ввод пользователя нажмите /cancel.")
    return adduser


async def deletequize(update, context):
    await update.message.reply_text(rf"Введите название теста, которой надо удалить.")
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


async def results(update, context):
    """Отправляет сообщение когда получена команда /help"""
    await update.message.reply_text("Я пока не умею помогать...")


def main():
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("teacher", teacher))
    application.add_handler(CommandHandler("student", student))

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('viewgroups', viewgroups)],

        states={
            viewgroup: [MessageHandler(filters.TEXT & ~filters.COMMAND, viewgroup)],
        },

        fallbacks=[CommandHandler("cancel", cancel)],
    )
    application.add_handler(conv_handler)

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('viewtests', viewtests)],

        states={
            choiceview: [MessageHandler(filters.TEXT & ~filters.COMMAND, choiceview)],
        },

        fallbacks=[CommandHandler("cancel", cancel)],
    )
    application.add_handler(conv_handler)

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('deltestforgroup', deltestforgroup)],

        states={
            takenametest: [MessageHandler(filters.TEXT & ~filters.COMMAND, takenametest)],
            deletetestforgroup: [MessageHandler(filters.TEXT & ~filters.COMMAND, deletetestforgroup)],
        },

        fallbacks=[CommandHandler("cancel", cancel)],
    )
    application.add_handler(conv_handler)

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('deluserfromgroup', deluserfromgroup)],

        states={
            choicegr: [MessageHandler(filters.TEXT & ~filters.COMMAND, choicegr)],
            usernamedel: [MessageHandler(filters.TEXT & ~filters.COMMAND, usernamedel)],
        },

        fallbacks=[CommandHandler("cancel", cancel)],
    )
    application.add_handler(conv_handler)

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('removeatest', removeatest)],

        states={
            removetestforgroup: [MessageHandler(filters.TEXT & ~filters.COMMAND, removetestforgroup)],
        },

        fallbacks=[CommandHandler("cancel", cancel)],
    )
    application.add_handler(conv_handler)

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('assignatest', assignatest)],

        states={
            assigntestforgroup: [MessageHandler(filters.TEXT & ~filters.COMMAND, assigntestforgroup)],
        },

        fallbacks=[CommandHandler("cancel", cancel)],
    )
    application.add_handler(conv_handler)

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('Viewresults', stedentresult)],

        states={
            result: [MessageHandler(filters.TEXT & ~filters.COMMAND, result)],
        },

        fallbacks=[CommandHandler("cancel", cancel)],
    )
    application.add_handler(conv_handler)

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('Taketest', studentсhoice)],

        states={
            quwest1: [MessageHandler(filters.TEXT & ~filters.COMMAND, quwest1)],
            quwest2: [MessageHandler(filters.TEXT & ~filters.COMMAND, quwest2)],
        },

        fallbacks=[CommandHandler("cancel", cancel)],
    )
    application.add_handler(conv_handler)

    application.add_handler(CommandHandler("createtest", create_a_test))

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
        entry_points=[CommandHandler('creategroup', create_a_group)],

        states={
            Newgroup: [MessageHandler(filters.TEXT & ~filters.COMMAND, Newgroup)],
            addq: [MessageHandler(filters.TEXT & ~filters.COMMAND, addq)],
            adduser: [MessageHandler(filters.TEXT & ~filters.COMMAND, adduser)],
        },

        fallbacks=[CommandHandler("cancel", cancel)],
    )
    application.add_handler(conv_handler)

    application.add_handler(conv_handler)

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('deletequize', deletequize)],

        states={
            deleteq: [MessageHandler(filters.TEXT & ~filters.COMMAND, deleteq)],
        },

        fallbacks=[CommandHandler("cancel", cancel)],
    )
    application.add_handler(conv_handler)

    application.run_polling()


if __name__ == '__main__':
    main()