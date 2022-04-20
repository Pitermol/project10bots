import json
import schedule
from threading import Thread
import telebot
import time
import hashlib

from yoomoney import Quickpay, Client

token_ym = "4100112274525531.8D2250A6A1ADE9E5E275DBC5DCEFEFA876D465E8B60188017176394978C1D6F3159F9BC5711ACC46029230" \
        "4016C9ABF9E05C9DC7AE1B168458AA61CABEB14C0156C68EF95FEF56BFD0D8C335AEBAE48D345A5EFC03FA980412CA4CECC346D" \
        "D8AF9CD3C2D0FE8044CD002ECDB2441F126CC4FABE410B8004DDBA7ECDD1794D767"

token = "5391977172:AAF_LOA1BCCFn5gMEmIm7reVFwzRE-O-mwo"
bot = telebot.TeleBot(token)
with open('cities.json', 'r', encoding="utf-8") as f:
    cities = json.load(f)['cities']
f.close()
with open('all_categories.json', 'r', encoding="utf-8") as f:
    all_categories = json.load(f)['categories']
f.close()
all_categories1 = list(map(lambda x: x + "1", all_categories))


# Эти списки должны обновляться в функциях

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
        users[str(message.chat.id)] = {"nickname": message.from_user.username, "creating": None, "watching": 0,
                                       "moderating": []}
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

        with open("users.json", "r", encoding="utf-8") as f:
            users = json.load(f)
        f.close()
        hash_object = hashlib.sha256(str(time.time()).encode("utf-8")).hexdigest()[-13:]
        users[str(message.chat.id)]["creating"] = {"offer_id": hash_object, "name": None, "category": None, "title": None,
                                                   "description": None, "city": None, "address": None,
                                                   "phone": None, "price": None, "photos": []}
        with open("users.json", "w") as f:
            json.dump(users, f)
        f.close()
        send = bot.send_message(message.chat.id, 'Введите ваше имя')
        bot.register_next_step_handler(send, category)
    else:
        send = bot.send_message(message.chat.id, 'Ошибка! Неверная команда')
        bot.register_next_step_handler(send, start_func)


def checking_adverts(message):
    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.add(telebot.types.InlineKeyboardButton(text="Личные вещи", callback_data='Личные вещи1'))
    keyboard.add(telebot.types.InlineKeyboardButton(text="Транспорт", callback_data="Транспорт1"))
    keyboard.add(telebot.types.InlineKeyboardButton(text="Работа", callback_data="Работа1"))
    keyboard.add(telebot.types.InlineKeyboardButton(text="Для дома и дачи", callback_data="Для дома и дачи1"))
    keyboard.add(telebot.types.InlineKeyboardButton(text="Недвижимость", callback_data="Недвижимость1"))
    keyboard.add(telebot.types.InlineKeyboardButton(text="Предложение услуг", callback_data="Предложение услуг1"))
    keyboard.add(telebot.types.InlineKeyboardButton(text="Электроника", callback_data="Электроника1"))
    keyboard.add(telebot.types.InlineKeyboardButton(text="Готовый бизнес", callback_data="Готовый бизнес1"))
    send = bot.send_message(message.chat.id, 'Выберите интересующую вас категорию', reply_markup=keyboard)


def category(message):
    with open("users.json", "r") as f:
        users = json.load(f)
    f.close()
    users[str(message.chat.id)]["creating"]["name"] = message.text
    with open("users.json", "w") as f:
        json.dump(users, f)
    f.close()
    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.add(telebot.types.InlineKeyboardButton(text="Личные вещи", callback_data='Личные вещи'))
    keyboard.add(telebot.types.InlineKeyboardButton(text="Транспорт", callback_data="Транспорт"))
    keyboard.add(telebot.types.InlineKeyboardButton(text="Работа", callback_data="Работа"))
    keyboard.add(telebot.types.InlineKeyboardButton(text="Для дома и дачи", callback_data="Для дома и дачи"))
    keyboard.add(telebot.types.InlineKeyboardButton(text="Недвижимость", callback_data="Недвижимость"))
    keyboard.add(telebot.types.InlineKeyboardButton(text="Предложение услуг", callback_data="Предложение услуг"))
    keyboard.add(telebot.types.InlineKeyboardButton(text="Электроника", callback_data="Электроника"))
    keyboard.add(telebot.types.InlineKeyboardButton(text="Готовый бизнес", callback_data="Готовый бизнес"))
    send = bot.send_message(message.chat.id, 'Выберите интересующую вас категорию', reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: call.data in all_categories1)
def watching_adverts(call):
    with open("categories.json", "r") as f:
        categories = json.load(f)
    f.close()
    with open("users.json", "r") as f:
        users = json.load(f)
    f.close()
    cat = call.data[:-1]
    if cat in categories:
        users[str(call.message.chat.id)]["watching"] = -1
        offers = categories[cat]
        creation = offers[users[str(call.message.chat.id)]["watching"]]
        confirm = f"\nг. {creation['city']}\n{creation['address']}\n\nЗаголовок:\n{creation['title']}\n\n" \
                  f"Описание:\n{creation['description']}\n\n📞 " \
                  f"{''.join(creation['phone'].split())}\n\n" \
                  f"Написать продавцу"
        with open("users.json", "w") as f:
            json.dump(users, f)
        f.close()

        keyboard = telebot.types.ReplyKeyboardMarkup(True)
        keyboard.row('Далее', 'Обновить объявления')
        print(offers)
        send = bot.send_message(call.message.chat.id, confirm, reply_markup=keyboard)
        bot.register_next_step_handler(send, checking_function, offers)

        # Добавить кнопки (Далее, Обновить)
        # Далее - в функцию next_offer
        # Обновить - Снова функцию watching_adverts
    else:
        bot.send_message(call.message.chat.id, 'Тут пока ничего нет. Загляните позже')
        try:
            keyboard = telebot.types.InlineKeyboardMarkup()
            keyboard.add(telebot.types.InlineKeyboardButton(text="Личные вещи", callback_data='Личные вещи1'))
            keyboard.add(telebot.types.InlineKeyboardButton(text="Транспорт", callback_data="Транспорт1"))
            keyboard.add(telebot.types.InlineKeyboardButton(text="Работа", callback_data="Работа1"))
            keyboard.add(telebot.types.InlineKeyboardButton(text="Для дома и дачи", callback_data="Для дома и дачи1"))
            keyboard.add(telebot.types.InlineKeyboardButton(text="Недвижимoсть", callback_data="Недвижимость1"))
            keyboard.add(
                telebot.types.InlineKeyboardButton(text="Предложение услуг", callback_data="Предложение услуг1"))
            keyboard.add(telebot.types.InlineKeyboardButton(text="Электроника", callback_data="Электроника1"))
            keyboard.add(telebot.types.InlineKeyboardButton(text="Готовый бизнес", callback_data="Готовый бизнес1"))
            bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, "Объявлений пока нет",
                                          reply_markup=keyboard)
        except:
            keyboard = telebot.types.InlineKeyboardMarkup()
            keyboard.add(telebot.types.InlineKeyboardButton(text="Личные вещи", callback_data='Личные вещи1'))
            keyboard.add(telebot.types.InlineKeyboardButton(text="Транспoрт", callback_data="Транспорт1"))
            keyboard.add(telebot.types.InlineKeyboardButton(text="Работа", callback_data="Работа1"))
            keyboard.add(telebot.types.InlineKeyboardButton(text="Для дома и дачи", callback_data="Для дома и дачи1"))
            keyboard.add(telebot.types.InlineKeyboardButton(text="Недвижимoсть", callback_data="Недвижимость1"))
            keyboard.add(
                telebot.types.InlineKeyboardButton(text="Предложение услуг", callback_data="Предложение услуг1"))
            keyboard.add(telebot.types.InlineKeyboardButton(text="Электроника", callback_data="Электроника1"))
            keyboard.add(telebot.types.InlineKeyboardButton(text="Готовый бизнес", callback_data="Готовый бизнес1"))
            bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, "Объявлений пока нет",
                                          reply_markup=keyboard)


def checking_function(message, offers):
    if message.text == 'В главное меню':
        start_message(message)
    elif message.text == 'Обновить объявления':
        checking_adverts(message)
    else:
        next_offer(message, offers)


def next_offer(message, offers):
    with open("users.json", "r") as f:
        users = json.load(f)
    f.close()
    # Переменную offers надо как то передавать в эту функцию, не читая файл снова, мб через бд
    # Проверка на количество оферов если abs(users[str(call.message.chat.id)]["watching"]) < кол-ва оферов, то дальше идем
    if abs(users[str(message.chat.id)]["watching"]) >= len(offers):
        keyboard = telebot.types.ReplyKeyboardMarkup(True)
        keyboard.row('В главное меню')
        send = bot.send_message(message.chat.id, 'Предложения закончились, попробуйте позже', reply_markup=keyboard)
        bot.register_next_step_handler(send, start_message)
    else:
        users[str(message.chat.id)]["watching"] -= 1
        creation = offers[users[str(message.chat.id)]["watching"]]
        confirm = f"\nг. {creation['city']}\n{creation['address']}\n\nЗаголовок:\n{creation['title']}\n\n" \
                  f"Описание:\n{creation['description']}\n\n📞 " \
                  f"{''.join(creation['phone'].split())}\n\n" \
                  f"Написать продавцу"
        keyboard = telebot.types.ReplyKeyboardMarkup(True)
        keyboard.row('Далее', 'Обновить объявления')
        keyboard.row('В главное меню')
        send = bot.send_message(message.chat.id, confirm, reply_markup=keyboard)
        with open("users.json", "w") as f:
            json.dump(users, f)
        f.close()
        bot.register_next_step_handler(send, checking_function, offers)

    # вывод оффера users[str(call.message.chat.id)]["watching"]
    # запись в users обновленного значения
    # кнопки далее и обновить


@bot.callback_query_handler(func=lambda call: call.data in all_categories)
def main_func(call):
    if call.data[-1] == '1':
        watching_adverts(call)
    elif call.data[-1] == '2':
        city(call)
    else:
        with open("users.json", "r") as f:
            users = json.load(f)
        f.close()
        users[str(call.message.chat.id)]["creating"]["category"] = call.data
        with open("users.json", "w") as f:
            json.dump(users, f)
        f.close()
        send = bot.send_message(call.message.chat.id, 'Введите заголовок')
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
    keyboard = telebot.types.InlineKeyboardMarkup()
    for i in cities:
        keyboard.add(telebot.types.InlineKeyboardButton(text=i, callback_data=i))
    send = bot.send_message(message.chat.id, 'Выберите ваш город', reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: call.data in cities)
def city(call):
    with open("users.json", "r") as f:
        users = json.load(f)
    f.close()
    users[str(call.message.chat.id)]["creating"]["city"] = call.data
    with open("users.json", "w") as f:
        json.dump(users, f)
    f.close()
    send = bot.send_message(call.message.chat.id,
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
    # -------------------
    # cat = creation["category"]
    # del creation["category"]
    # if cat in categories:
    #     categories[cat].append(creation)
    # else:
    #     categories[cat] = [creation]
    # users[str(message.chat.id)]['creating'] = None
    # with open("users.json", "w") as f:
    #     json.dump(users, f)
    # f.close()
    # with open("categories.json", "w") as f:
    #     json.dump(categories, f)
    # f.close()
    # ------------------
    keyboard = telebot.types.ReplyKeyboardMarkup(True)
    keyboard.row('Подтвердить', 'Заполнить заново')
    confirm = f"\nг. {creation['city']}\n{creation['address']}\n\nЗаголовок:\n{creation['title']}\n\n" \
              f"Описание:\n{creation['description']}\n\n📞 " \
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
    bot.register_next_step_handler(send, payment, creation)


@bot.message_handler(func=lambda x: x.text == "Подтвердить")
def payment(message, creation):
    with open("users.json", "r") as f:
        users = json.load(f)
    f.close()
    users[str(message.chat.id)]['creating'] = None
    with open("users.json", "w") as f:
        json.dump(users, f)
    f.close()

    message_id = message.message_id

    quickpay = Quickpay(
        receiver="4100117780986446",
        quickpay_form="shop",
        targets="Новое объявление",
        paymentType="SB",
        sum=2,
        label=creation["offer_id"]
    )
    keyboard = telebot.types.ReplyKeyboardMarkup(True)
    keyboard.row('Оплатил')
    send = bot.send_message(message.chat.id, f"Ссылка для оплаты: {quickpay.base_url}", reply_markup=keyboard)
    bot.register_next_step_handler(send, payment_confirm, creation["offer_id"], message_id, creation)


@bot.message_handler(func=lambda x: x.text == "Оплатил")
def payment_confirm(message, offer_id, message_id, creation):
    client = Client(token_ym)
    history = client.operation_history(label=str(offer_id))
    operation = history.operations
    ind = 0
    while len(operation) == 0:
        if ind == 3:
            break
        ind += 1
        time.sleep(2)
        history = client.operation_history(label=str(offer_id))
        operation = history.operations
    if len(operation) > 0:
        with open("moderating.json", "r") as f:
            moderating = json.load(f)
        f.close()
        senf = bot.send_message(message.chat.id, "Заявка отправлена на модерацию")
        message_id = senf.message_id
        moderating[offer_id] = [creation, message_id, message.chat.id]
        with open("moderating.json", "w") as f:
            json.dump(moderating, f)
        f.close()

        operation = operation[0]
        confirm = f"Operation_id: {operation.operation_id}\nDate: {operation.datetime}\nTitle:{operation.title}\n" \
                  f"Amount: {operation.amount}\nOffer_id: {operation.label}"
        keyboard = telebot.types.InlineKeyboardMarkup()
        keyboard.add(telebot.types.InlineKeyboardButton(text="Подтвердить", callback_data='confirm_adding'))
        bot.send_message("1156324879", confirm, reply_markup=keyboard)
    else:
        send = bot.send_message(message.chat.id, "Вы не совершили оплату")
        bot.register_next_step_handler(send, payment_confirm, offer_id, message_id, creation)


@bot.callback_query_handler(func=lambda call: call.data == "confirm_adding")
def confirm_adding(call):
    if call.message.chat.username == "justPeter3":
        with open("users.json", "r") as f:
            users = json.load(f)
        f.close()
        with open("categories.json", "r") as f:
            categories = json.load(f)
        f.close()
        with open("moderating.json", "r") as f:
            moderating = json.load(f)
        f.close()

        offer_id = call.message.text.split()[-1]
        creation, message_id, chat_id = moderating[offer_id]
        del moderating[offer_id]

        cat = creation["category"]
        del creation["category"]
        if cat in categories:
            categories[cat].append(creation)
        else:
            categories[cat] = [creation]
        with open("users.json", "w") as f:
            json.dump(users, f)
        f.close()
        with open("categories.json", "w") as f:
            json.dump(categories, f)
        f.close()
        with open("moderating.json", "w") as f:
            json.dump(moderating, f)
        f.close()
        with open("categories.json", "w") as f:
            json.dump(categories, f)
        f.close()

        bot.send_message(chat_id=chat_id, text="Заявка одобрена", reply_to_message_id=int(message_id))


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
