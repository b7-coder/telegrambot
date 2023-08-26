import psycopg2
import telebot

bot = telebot.TeleBot('ТОКЕН')


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.from_user.id, "Наш бот работает")

@bot.message_handler(commands=['getAll'])
def start(message):
    bot.send_message(message.from_user.id, "Другая команда")

@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    
    try:
        connection = psycopg2.connect(host = 'localhost',dbname = "payments",user = "postgres",password = "12345", )
        print("Успешно подключено")

        cursor = connection.cursor()
        # Базу chat
        # таблица messages(id, text(varchar), userId(varchar))
        query = f"Запрос на вставку данных {message.text}"
        cursor.execute(query)

    except Exception as e:
        print("Возникла ошибка")
        print(e)
    finally:
        if connection:
            connection.close()


bot.polling(none_stop=True, interval=0)