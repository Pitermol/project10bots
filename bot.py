import json

import telebot
import time
import hashlib

token = "5391977172:AAF_LOA1BCCFn5gMEmIm7reVFwzRE-O-mwo"
bot = telebot.TeleBot(token)


@bot.message_handler(commands=['start'])
def start_message(message):
    with open("users.json", "r", encoding="utf-8") as f:
        users = json.load(f)
    f.close()
    if str(message.chat.id) not in users:
        users[str(message.chat.id)] = {"nickname": message.from_user.username, "creating": None}
    with open("users.json", "w", encoding="utf-8") as f:
        json.dump(users, f, ensure_ascii=False)
    f.close()
    # bot.send_media_group(message.chat.id, [telebot.types.InputMediaPhoto(open('image0.jpg', 'rb'), caption="text"),
    #                                        telebot.types.InputMediaPhoto(open('image1.jpg', 'rb'))])
    keyboard = telebot.types.ReplyKeyboardMarkup(True)
    keyboard.row('Создать объявление')
    send = bot.send_message(message.chat.id, '''Добро пожаловать в чат Бот "Название".
                                Размещение рекламного объявления в данной системе платное, стоимость одного рекламного объявления составляет  10 рублей. Срок размещения объявления 5 дней.
                                «ВАЖНО» Надо как то сделать , по истечению 5 дней как то уведомлять клиента что срок его заканчив
                                ается если это возможно конечно.

                                Получить информацию вы можете отправив /help

                                Отправь /start что бы вернуться на главную.''', reply_markup=keyboard)
    bot.register_next_step_handler(send, start_func)


@bot.message_handler(content_type=['text'])
def start_func(message):
    with open("users.json", "r") as f:
        users = json.load(f)
    f.close()
    users[str(message.chat.id)]["creating"] = {"name": None, "category": None, "title": None,
                                               "description": None, "city": None, "address": None,
                                               "phone": None, "price": None, "photos": []}
    with open("users.json", "w") as f:
        json.dump(users, f)
    f.close()
    send = bot.send_message(message.chat.id, 'Введите ваше имя')
    bot.register_next_step_handler(send, category)


def category(message):
    with open("users.json", "r") as f:
        users = json.load(f)
    f.close()
    users[str(message.chat.id)]["creating"]["name"] = message.text
    with open("users.json", "w") as f:
        json.dump(users, f)
    f.close()
    keyboard = telebot.types.ReplyKeyboardMarkup(True)
    keyboard.row('Личные вещи', 'Транспорт', 'Работа')
    keyboard.row('Для дома и дачи', 'предложение услуг')
    keyboard.row('Недвижимость', 'Электроника', 'Готовый бизнес')
    send = bot.send_message(message.chat.id, 'Выберите интересующую вас категорию', reply_markup=keyboard)
    bot.register_next_step_handler(message, main_func)


def main_func(message):
    with open("users.json", "r") as f:
        users = json.load(f)
    f.close()
    users[str(message.chat.id)]["creating"]["category"] = message.text
    with open("users.json", "w") as f:
        json.dump(users, f)
    f.close()
    send = bot.send_message(message.chat.id, 'Введите заголовок')
    bot.register_next_step_handler(send, description)


def name(message):
    with open("users.json", "r") as f:
        users = json.load(f)
    f.close()
    users[str(message.chat.id)]["creating"]["title"] = message.text
    with open("users.json", "w") as f:
        json.dump(users, f)
    f.close()
    send = bot.send_message(message.chat.id, 'Введите описание объявления')
    bot.register_next_step_handler(send, description)


def description(message):
    with open("users.json", "r") as f:
        users = json.load(f)
    f.close()
    users[str(message.chat.id)]["creating"]["description"] = message.text
    with open("users.json", "w") as f:
        json.dump(users, f)
    f.close()
    send = bot.send_message(message.chat.id, 'Введите ваш город')
    bot.register_next_step_handler(send, city)


def city(message):
    with open("users.json", "r") as f:
        users = json.load(f)
    f.close()
    users[str(message.chat.id)]["creating"]["city"] = message.text
    with open("users.json", "w") as f:
        json.dump(users, f)
    f.close()
    send = bot.send_message(message.chat.id,
                            "Введите ваш адрес для быстро поиска. Если не хотите указывать адрес, напишите '-'")
    bot.register_next_step_handler(send, address)


def address(message):
    with open("users.json", "r") as f:
        users = json.load(f)
    f.close()
    users[str(message.chat.id)]["creating"]["address"] = message.text
    with open("users.json", "w") as f:
        json.dump(users, f)
    f.close()
    send = bot.send_message(message.chat.id, "Введите ваш номер телефона")
    bot.register_next_step_handler(send, price)


def phone(message):
    with open("users.json", "r") as f:
        users = json.load(f)
    f.close()
    users[str(message.chat.id)]["creating"]["phone"] = message.text
    with open("users.json", "w") as f:
        json.dump(users, f)
    f.close()
    send = bot.send_message(message.chat.id, "Введите цену")
    bot.register_next_step_handler(send, price)


def price(message):
    with open("users.json", "r") as f:
        users = json.load(f)
    f.close()
    users[str(message.chat.id)]["creating"]["price"] = message.text
    with open("users.json", "w") as f:
        json.dump(users, f)
    f.close()
    keyboard = telebot.types.ReplyKeyboardMarkup(True)
    keyboard.row('Готово')
    bot.send_message(message.chat.id, "Пришлите до 4-ех фотографий вашего продукта", reply_markup=keyboard)


@bot.message_handler(func=lambda x: x.text == "Готово")
def ready(message):
    print("ready pressed")
    with open("users.json", "r") as f:
        users = json.load(f)
    f.close()
    if users[str(message.chat.id)]['creating'] is not None:
        check(message)


def check(message):
    with open("users.json", "r") as f:
        users = json.load(f)
    f.close()
    with open("categories.json", "r") as f:
        categories = json.load(f)
    f.close()
    creation = users[str(message.chat.id)]['creating']
    cat = creation["category"]
    del creation["category"]
    if cat in categories:
        categories[cat].append(creation)
    else:
        categories[cat] = [creation]
    users[str(message.chat.id)]['creating'] = None
    with open("users.json", "w") as f:
        json.dump(users, f)
    f.close()
    with open("categories.json", "w") as f:
        json.dump(categories, f)
    f.close()

    keyboard = telebot.types.ReplyKeyboardMarkup(True)
    keyboard.row('Назад')
    bot.send_message(message.chat.id, "Все готово! Данные записаны", reply_markup=keyboard)


@bot.message_handler(content_types='photo')
def photo(message):
    print("starting")
    with open("users.json", "r") as f:
        users = json.load(f)
    f.close()
    fileID = message.photo[-1].file_id
    file_info = bot.get_file(fileID)
    downloaded_file = bot.download_file(file_info.file_path)
    name = str(time.time())[-5:] + str(message.chat.id) + str(len(users[str(message.chat.id)]['creating']['photos'])) + ".jpg"
    hash_object = hashlib.sha256(name.encode("utf-8"))
    name = hash_object.hexdigest()[-10:]
    with open(f"images/{name}", 'wb') as new_file:
        new_file.write(downloaded_file)
    users[str(message.chat.id)]['creating']['photos'].append(name)
    print(len(users[str(message.chat.id)]['creating']['photos']), name)
    if len(users[str(message.chat.id)]['creating']['photos']) == 4:
        bot.send_message(message.chat.id, "Фотография загружена успешно")
        with open("users.json", "w") as f:
            json.dump(users, f)
        f.close()
        check(message=message)
    else:
        with open("users.json", "w") as f:
            json.dump(users, f)
        f.close()
        keyboard = telebot.types.ReplyKeyboardMarkup(True)
        keyboard.row('Готово')
        send = bot.send_message(message.chat.id, "Фотография загружена успешно", reply_markup=keyboard)


bot.polling(none_stop=False, interval=1)
