# -*- coding: utf-8 -*-

import telebot
import sqlite3 as sq
import config as cnf
import sql_db as s_go

bot = telebot.TeleBot(cnf.token)
print(cnf.token)

@bot.message_handler(commands=['start'])
def start_message(message):
    print("--->", message.chat.username, ": conecting")
    user_markup = telebot.types.ReplyKeyboardMarkup(True)
    user_markup.row('/help', '/stop', '/nt')
    user_markup.row('/tm', '/tz', '/ta','/bt')
    bot.send_message(message.chat.id, 'Добро пожаловать, выберите одну из команд на кнопках ниже поля для ввода...\nЧтобы узнать больше выберите команду /help.',
                     reply_markup=user_markup)

@bot.message_handler(commands=['help'])
def get_help(message):
    print("--->", message.chat.username, ": COMAND /help")
    bot.send_message(message.chat.id, cnf.description)

@bot.message_handler(commands=['tm'])
def get_tm(message):
    print("--->", message.chat.username, ": COMAND /tm:")
    conn = sq.connect('test.db')
    s = [x for x in s_go.sql_rq("SELECT * FROM teems", conn)]
    conn.close()
    srt = "Напишите номер темы: \n"
    for i in s:
        srt = srt + str(i[0]) + " - " + i[1] + "\n"
    bot.send_message(message.chat.id, srt)

@bot.message_handler(commands=['tz'])
def get_tz(message):
    print("--->", message.chat.username, ": COMAND /tz:")
    f2 = open('numer.txt', 'r')
    numer_tm = int(f2.read())
    f2.close()
    if numer_tm == 0:
        bot.send_message(message.chat.id, "Сначала выберите тему")
    elif numer_tm in [1,2,9,10,11]:
        cnf.index = 2
        conn = sq.connect('test.db')
        sql = "SELECT * FROM tz WHERE id_tm='" + str(numer_tm) + "'"
        srt = "Для того, чтобы просмотреть следующий тезис выберите команду /nt; предыдущий - /bt.\n\n"
        srt2 = ""
        ta = [x for x in s_go.sql_rq(sql, conn)]

        for i in ta:
            srt = srt + i[1]
            break
        cnf.ta2 = ta
        bot.send_message(message.chat.id, srt)

@bot.message_handler(commands=['ta'])
def get_ta(message):
    print("--->", message.chat.username, ": COMAND /ta:")
    f = open('numer.txt', 'r')
    numer_tm = int(f.read())
    f.close()
    if numer_tm == 0:
        bot.send_message(message.chat.id, "Сначала выберите тему")
    elif numer_tm in [1,2,9,10,11]:
        cnf.index = 1
        conn = sq.connect('test.db')
        sql = "SELECT * FROM facts WHERE id_tm='" + str(numer_tm) + "'"
        srt = "Для того, чтобы просмотреть следующий аргумент выберите команду /nt; предыдущий - /bt.\n\n"
        srt2 = ""
        ta = [x for x in s_go.sql_rq(sql, conn)]

        for i in ta:
            srt = srt + i[1] + "\n-----------\n" + i[2]
            break
        cnf.ta = ta
        bot.send_message(message.chat.id, srt)

@bot.message_handler(commands=['nt'])
def next_fact(message):
    print("--->", message.chat.username, ": COMAND /nt:")
    if cnf.index == 1:
        if cnf.ta != "":
            key = 0
            srt = "Для того, чтобы просмотреть следующий аргумент выберите команду /nt; предыдущий - /bt.\n\n"
            if cnf.key+1 > len(cnf.ta)-1:
                cnf.key = 0
            else:
                cnf.key += 1
            for i in cnf.ta:
                if key == cnf.key:
                    if i[1] == "" and i[2] == "":
                        if cnf.key+1 > len(cnf.ta)-1:
                            cnf.key = 0
                        else:
                            cnf.key += 1
                        continue
                    else:
                        srt = srt + i[1] + "\n-----------\n" + i[2]
                        break
                else:
                    key += 1
            bot.send_message(message.chat.id, srt)
        else:
            bot.send_message(message.chat.id, 'Вы ещё не выбрали не одну тему. Для того, чтобы выбрать тему выполните команду /ta, а затемы выберите номер темы.')
    elif cnf.index == 2:
        if cnf.ta2 != "":
            key = 0
            srt = "Для того, чтобы просмотреть следующий Тезис выберите команду /nt; предыдущий - /bt.\n\n"
            if cnf.key2+1 > len(cnf.ta2)-1:
                cnf.key2 = 0
            else:
                cnf.key2 += 1
            for i in cnf.ta2:
                if key == cnf.key2:
                    if i[1] == "" and i[2] == "":
                        if cnf.key2+1 > len(cnf.ta2)-1:
                            cnf.key2 = 0
                        else:
                            cnf.key2 += 1
                        continue
                    else:
                        srt = srt + "-----------\n" + i[1]
                        break
                else:
                    key += 1
            bot.send_message(message.chat.id, srt)
        else:
            bot.send_message(message.chat.id, 'Вы ещё не выбрали не одну тему. Для того, чтобы выбрать тему выполните команду /ta, а затемы выберите номер темы.')
    else:
        bot.send_message(message.chat.id, 'Сначала выберите тему - /tm.\n А потом выберите, что вам нужно показать:\n/tz - тезисы\n/ta - аргуметы')

@bot.message_handler(commands=['bt'])
def before_fact(message):
    print("--->", message.chat.username, ": COMAND /bt:")
    if cnf.index == 1:
        if cnf.ta != "":
            key = 0
            srt = "Для того, чтобы просмотреть следующий аргумент выберите команду /nt; предыдущий - /bt.\n\n"
            if (cnf.key-1) < 0:
                cnf.key = len(cnf.ta)-1
            else:
                cnf.key -= 1
            for i in cnf.ta:
                if key == cnf.key:
                    srt = srt + i[1] + "\n-----------\n" + i[2]
                    break
                else:
                    key += 1
            bot.send_message(message.chat.id, srt)
        else:
            bot.send_message(message.chat.id, 'Вы ещё не выбрали не одну тему. Для того, чтобы выбрать тему выполните команду /ta, а затемы выберите номер темы.')
    elif cnf.index == 2:
        if cnf.ta2 != "":
            key = 0
            srt = "Для того, чтобы просмотреть следующий Тезис выберите команду /nt; предыдущий - /bt.\n\n"
            if (cnf.key2-1) < 0:
                cnf.key2 = len(cnf.ta2)-1
            else:
                cnf.key2 -= 1
            for i in cnf.ta2:
                if key == cnf.key2:
                    srt = srt + "-----------\n" + i[1]
                    break
                else:
                    key += 1
            bot.send_message(message.chat.id, srt)
        else:
            bot.send_message(message.chat.id, 'Вы ещё не выбрали не одну тему. Для того, чтобы выбрать тему выполните команду /ta, а затемы выберите номер темы.')
    else:
        bot.send_message(message.chat.id, 'Сначала выберите тему - /tm.\n А потом выберите, что вам нужно показать:\n/tz - тезисы\n/ta - аргуметы')


@bot.message_handler(commands=['stop'])
def stop_message(message):
    print(message.chat.username, ": unconected")
    hide_markup = telebot.types.ReplyKeyboardHide()
    bot.send_message(message.chat.id, 'Досвидания...',
                     reply_markup=hide_markup)

@bot.message_handler(content_types=['text'])
def repeat_all_messages(message):
    num = message.text
    if num in ["1","2","9","10","11"]:
        try:
            x = int(num)
        except ValueError:
            bot.send_message(message.chat.id, "Напишите только номер темы, если вы хотели выбрать тему.\nЕсли вы не знаете номера тем, то выполните команду /tm")
        else:
            f = open('numer.txt', 'w')
            f.write(str(x))
            f.close()

            print("--->", message.chat.username, ": select the ", str(x), " teem")
            bot.send_message(message.chat.id, "Вы можете найти аргументы - команды /ta. \nИли найти тезисы /tz. \nДля выбора другой темы снова наберите /tm.")
    else:
        bot.send_message(message.chat.id, "Я не понимаю, что это за команда?")

bot.polling(none_stop=True, interval=1)
