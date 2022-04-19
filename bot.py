import json
import schedule
from threading import Thread
import telebot
import time
import hashlib

token = "5391977172:AAF_LOA1BCCFn5gMEmIm7reVFwzRE-O-mwo"
bot = telebot.TeleBot(token)


def schedule_checker():
    while True:
        schedule.run_pending()
        time.sleep(1)


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
    keyboard.row('Создать объявление', 'Посмотреть объявления')
    send = bot.send_message(message.chat.id, '''Добро пожаловать в чат Бот "Название".
                                Размещение рекламного объявления в данной системе платное, стоимость одного рекламного объявления составляет  10 рублей. Срок размещения объявления 5 дней.
                                «ВАЖНО» Надо как то сделать , по истечению 5 дней как то уведомлять клиента что срок его заканчив
                                ается если это возможно конечно.

                                Получить информацию вы можете отправив /help

                                Отправь /start что бы вернуться на главную.''', reply_markup=keyboard)
    bot.register_next_step_handler(send, start_func)


@bot.message_handler(content_type=['text'])
def start_func(message):
    if message.text == 'Посмотреть объявления':
        checking_adverts(message)
    elif message.text == 'Создать объявление' or message.text == 'Заполнить заново':

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
    elif message.text == "Подтвердить":
        keyboard = telebot.types.ReplyKeyboardMarkup(True)
        keyboard.row('Создать объявление', 'Посмотреть объявления')
        send = bot.send_message(message.chat.id, "Успешно сохранено. Выберите раздел", reply_markup=keyboard)
        bot.register_next_step_handler(send, start_func)
    else:
        send = bot.send_message(message.chat.id, 'Ошибка! Неверная команда')
        bot.register_next_step_handler(send, start_func)


def checking_adverts(message):
    send = bot.send_message(message.chat.id, 'Выберите категорию, в которой хотите просмотреть объявления')


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
    if message.text not in ['Личные вещи', 'Транспорт', 'Работа', 'Для дома и дачи', 'предложение услуг',
                            'Недвижимость', 'Электроника', 'Готовый бизнес']:
        send = bot.send_message(message.chat.id, "Такой категории нет, попробуйте снова")
        bot.register_next_step_handler(send, main_func)
    else:
        with open("users.json", "r") as f:
            users = json.load(f)
        f.close()
        users[str(message.chat.id)]["creating"]["category"] = message.text
        with open("users.json", "w") as f:
            json.dump(users, f)
        f.close()
        send = bot.send_message(message.chat.id, 'Введите заголовок')
        bot.register_next_step_handler(send, name)


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
    bot.register_next_step_handler(send, phone)


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
    keyboard.row('Подтвердить', 'Заполнить заново')
    confirm = f"\nг. {creation['city']}\n{creation['address']}\n\nЗаголовок:\n{creation['title']}\n\n" \
              f"Описание:\n{creation['description']}\n\n#{cat}\n#{''.join(creation['city'].split())}\n\n📞 " \
              f"{''.join(creation['phone'].split())}\n\n" \
              f"Написать продавцу"
    if len(creation['photos']) == 0:
        bot.send_message(message.chat.id, confirm, reply_markup=keyboard)
    else:
        photos = []
        for i, name in enumerate(creation['photos']):
            if i == 0:
                photos.append(telebot.types.InputMediaPhoto(open('images/' + name, 'rb'), caption=confirm))
            else:
                photos.append(telebot.types.InputMediaPhoto(open('images/' + name, 'rb')))
        bot.send_media_group(message.chat.id, photos)
    send = bot.send_message(message.chat.id, "Сохранить?", reply_markup=keyboard)
    bot.register_next_step_handler(send, start_func)


@bot.message_handler(content_types='photo')
def photo(message):
    for i in range(4):
        print(message.photo[-1].file_id, 'AAAAAAAAAAAAA')
        if len(schedule.get_jobs(str(i))) > 0:
            continue
        else:
            print(message.photo[-1].file_id)
            schedule.every(2).seconds.do(go, message, str(i)).tag(str(i))
            break


def go(message, tag=''):
    print("starting")
    with open("users.json", "r") as f:
        users = json.load(f)
    f.close()
    fileID = message.photo[-1].file_id
    file_info = bot.get_file(fileID)
    downloaded_file = bot.download_file(file_info.file_path)
    name = str(time.time())[-5:] + str(message.chat.id) + str(len(users[str(message.chat.id)]['creating']['photos']))
    hash_object = hashlib.sha256(name.encode("utf-8"))
    name = hash_object.hexdigest()[-10:] + ".jpg"
    with open(f"images/{name}", 'wb') as new_file:
        new_file.write(downloaded_file)
    users[str(message.chat.id)]['creating']['photos'].append(name)
    print(len(users[str(message.chat.id)]['creating']['photos']), name)
    schedule.clear(tag)
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


if __name__ == "__main__":
    scheduleThread = Thread(target=schedule_checker)
    scheduleThread.daemon = True
    scheduleThread.start()
    bot.polling(none_stop=False, interval=1)
