import psycopg2
import telebot
bot = telebot.TeleBot('6561176643:AAH3fXP9bTjBF_AZfGbDJgaIZceeXE0qRZI')
# /start

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.from_user.id, "Наш бот работает")

@bot.message_handler(commands=['getAll'])
def getAll(message):
    try:
        connection = psycopg2.connect(host = 'localhost',dbname = "payments",user = "postgres",password = "12345", )
        print("Успешно подключено")

        cursor = connection.cursor()
        query = f"SELECT * FROM messages;"
        cursor.execute(query)
        rows = cursor.fetchall()
        for row in rows:
            bot.send_message(message.from_user.id, f"{row}")

    except Exception as e:
        print("Возникла ошибка")
        print(e)
    finally:
        if connection:
            connection.close()

@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    
    try:
        connection = psycopg2.connect(host = 'localhost',dbname = "payments",user = "postgres",password = "12345", )
        print("Успешно подключено")

        cursor = connection.cursor()
        # Базу chat
        # таблица messages(id, text(varchar), userId(varchar))
        query = f"insert into messages(text, userid) values('{message.text}', '{message.from_user.id}');"
        cursor.execute(query)
        connection.commit()

        cursor.execute("SELECT * FROM moiu")
        rows = cursor.fetchall()

        for row in rows:
            bot.send_message(message.from_user.id, f"{row}")


    except Exception as e:
        print("Возникла ошибка")
        print(e)


bot.polling(none_stop=True, interval=0)