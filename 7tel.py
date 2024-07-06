import telebot
from parser import parse_hh, parse_avito, parse_habr
from db import get_engine, create_tables, save_to_mysql_postgresql, save_to_mongodb

API_TOKEN = '7253308471:AAEHiIUUDl0VPRFAG6YTCvgh1UsH9_2rB-I'
bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(
        message,
        "Добро пожаловать! Я могу помочь вам найти вакансии на hh.ru, avito.ru и habr карьера. "
        "Введите /parse <database_type> <keyword> для получения последних вакансий и сохранения их в базу данных."
    )

@bot.message_handler(commands=['parse'])
def parse_and_save(message):
    try:
        _, db_type, keyword = message.text.split(' ', 2)
    except ValueError:
        bot.reply_to(message, "Неверный формат команды. Используйте: /parse <database_type> <keyword>")
        return

    bot.send_message(message.chat.id, f"Идет парсинг вакансий для ключевого слова '{keyword}'...")

    try:
        engine = get_engine(db_type)
    except ValueError as e:
        bot.reply_to(message, str(e))
        return

    # Выполням парсинг данных
    hh_vacancies = parse_hh(keyword)
    avito_vacancies = parse_avito(keyword)
    habr_vacancies = parse_habr(keyword)

    # Объединяем все ваканси в один список
    all_vacancies = hh_vacancies + avito_vacancies + habr_vacancies

    # Сохраняем ваканси в базу данных
    if db_type in ['mysql', 'postgresql']:
        create_tables(engine)
        save_to_mysql_postgresql(engine, all_vacancies)
    elif db_type == 'mongodb':
        save_to_mongodb(engine, 'vacancies_db', 'vacancies', all_vacancies)
    
    bot.send_message(message.chat.id, "Данные успешно сохранены в базу данных.")

bot.polling(none_stop=True)


    



