import psycopg2
import telebot
from telebot import types

bot = telebot.TeleBot('')

# Соединение с базой данных
def getConnectionVariable():
    return psycopg2.connect(host = 'localhost',dbname = "itrun",user = "postgres",password = "12345" )

# функция для выборки данных в базу
def getData(query):
    try:
        connection = getConnectionVariable()
        cursor = connection.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()
        return rows    

    except Exception as e:
        print("Возникла ошибка")
        print(e)
    finally:
        cursor.close()
        connection.close()

# функция для вставки данных в базу
def setData(query):
    try:
        connection = getConnectionVariable()
        cursor = connection.cursor()
        cursor.execute(query)
        connection.commit()  

    except Exception as e:
        print("Возникла ошибка")
        print(e)
    finally:
        cursor.close()
        connection.close()


# функция обработки всех сообщений телеграма
@bot.message_handler(content_types=['text'])
def get_text_messages(message):

    # сохраняем сообщение пользователя
    setData( f"INSERT INTO messages(message, user_telegram_id) values('{message.text}', '{message.from_user.id}');")
        
    # берем все курсы как кнопки
    rows = getData(f'SELECT * FROM courses;')

    # отправляем пользователю созданные кнопки
    кнопки = types.InlineKeyboardMarkup()
    for row in rows:
        кнопка = types.InlineKeyboardButton(f"{row[1]}", callback_data=f'{row[0]}')
        кнопки.add(кнопка)
    bot.send_message(message.from_user.id, f"Здравствуйте, выберите действие", reply_markup=кнопки)


# функция обработки нажатых кнопок
@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    try:
        if call.message:
            
            # берем описание определенного курса и отправляем пользователю
            rows = getData(f"SELECT * FROM courses WHERE id = {call.data} LIMIT 1;")
            bot.send_message(call.message.chat.id, f'{rows[0][2]}')

            # отправляем пробные уроки определенного курса 
            lessons = getData(f"SELECT * FROM lessons WHERE course_id = {call.data} AND date>NOW() LIMIT 5;")
            for row in lessons:
                bot.send_message(call.message.chat.id, f'Урок на тему: {row[1]}, начало в {row[2]}')

    except:
        print('Ошибка')


# код запуска телеграмма
bot.polling(none_stop=True, interval=0)