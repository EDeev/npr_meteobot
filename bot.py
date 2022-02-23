import config, asyncio, info
import logging, pymorphy2, time

from aiogram import Bot, Dispatcher, executor, types
from sql import SQLighter
from datetime import datetime as dt

# задаем уровень логов
logging.basicConfig(level=logging.INFO)

# инициализируем бота
bot = Bot(token=config.API_TOKEN)
dp = Dispatcher(bot)
keyboard = types.InlineKeyboardMarkup()
morph = pymorphy2.MorphAnalyzer()

# инициализируем соединение с БД
db = SQLighter('sub.db')


# СТАРТОВЫЕ КОМАНДЫ
@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    if not db.user_exists(message.from_user.id):
        # если юзера нет в базе, добавляем его
        db.add_user(message.from_user.id)

    buttons = [types.InlineKeyboardButton(text="1-я смена", callback_data="prt1"),
               types.InlineKeyboardButton(text="2-я смена", callback_data="prt2")]

    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(*buttons)

    await message.answer(f"Привет, {message.from_user.first_name}!\nЯ - погодный бот, созданный для выдачи информации о"
                         f" вероятных актировках. Прошу вас выбрать вашу смену обучения!\n\n<i>Для последующей "
                         f"смены: города или смены обучения воспользуйтесь командой <b>/town</b></i>",
                         parse_mode=types.ParseMode.HTML, reply_markup=keyboard)


@dp.message_handler(content_types=['sticker'])
async def stick(message: types.Message):
    print(message.sticker.file_id)


@dp.message_handler(commands=['town'])
async def town(message: types.Message):

    buttons = [types.InlineKeyboardButton(text="1-я смена", callback_data="prt1"),
               types.InlineKeyboardButton(text="2-я смена", callback_data="prt2")]

    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(*buttons)

    await message.answer("<b>Прошу вас выбрать вашу смену обучения!</b>", parse_mode=types.ParseMode.HTML,
                         reply_markup=keyboard)


# ИЛАЙН КЛАВИАТУРА
@dp.callback_query_handler(text="prt1")
async def part_one(call: types.CallbackQuery):
    db.update_user(call.message.chat.id, 3, 1)

    buttons = [types.InlineKeyboardButton(text="Норильск", callback_data="nor"),
               types.InlineKeyboardButton(text="Талнах", callback_data="tal"),
               types.InlineKeyboardButton(text="Оганер", callback_data="oga"),
               types.InlineKeyboardButton(text="Каеркан", callback_data="kae")]

    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(*buttons)

    await call.message.answer(text="<b><i>Отлично!</i></b> Теперь вам надо выбрать район в котором вы проживаете "
                                   "на территории НПР!",
                              parse_mode=types.ParseMode.HTML, reply_markup=keyboard)


@dp.callback_query_handler(text="prt2")
async def part_two(call: types.CallbackQuery):
    db.update_user(call.message.chat.id, 3, 2)

    buttons = [types.InlineKeyboardButton(text="Норильск", callback_data="nor"),
               types.InlineKeyboardButton(text="Талнах", callback_data="tal"),
               types.InlineKeyboardButton(text="Оганер", callback_data="oga"),
               types.InlineKeyboardButton(text="Каеркан", callback_data="kae")]

    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(*buttons)

    await call.message.answer(text="<b><i>Конечно я вам не завидую, но куда деваться)</i></b> Теперь вам надо выбрать "
                                   "район в котором вы проживаете на территории НПР!",
                              parse_mode=types.ParseMode.HTML, reply_markup=keyboard)


@dp.callback_query_handler(text=["nor", "tal", "oga", "kae"])
async def function(call: types.CallbackQuery):
    txt = call.data
    if txt == "nor":
        db.update_user(call.message.chat.id, 4, 1)
    elif txt == "tal":
        db.update_user(call.message.chat.id, 4, 2)
    elif txt == "oga":
        db.update_user(call.message.chat.id, 4, 3)
    elif txt == "kae":
        db.update_user(call.message.chat.id, 4, 4)

    await call.message.answer(text='<b>Прекрасно!</b> Вы заполнили данные, теперь если вы хотите подписаться на '
                                   'утреннюю рассылку об актировках воспользуйтесь командой <b>/letter</b>.\n\n'
                                   '<i><b>Для полного ознакомления можете воспользоваться командой /help</b></i>',
                              parse_mode=types.ParseMode.HTML)


# КОМАНДЫ АКТИВАЦИИ ПОДПИСОК
@dp.message_handler(commands=['notice'])
async def notification(message: types.Message):
    if str(message.chat.id) not in db.get_send():
        db.update_user(message.chat.id, 2, 1)
        await message.answer("Увидомление приходит каждый день не зависимо от наличия актировки!")
    else:
        db.update_user(message.chat.id, 2, 0)
        await message.answer("Уведомление приходит, только если есть актировка!")


@dp.message_handler(commands=['letter'])
async def letter(message: types.Message):
    if str(message.chat.id) not in db.get_subs():
        db.update_user(message.chat.id, 1, 1)
        await message.answer("Вы подписались на рассылку!")
    else:
        db.update_user(message.chat.id, 1, 0)
        await message.answer("Вы отписались от расслыки!")


@dp.message_handler(commands=['storm'])
async def storm(message: types.Message):
    await message.answer(info.storm(), parse_mode=types.ParseMode.MARKDOWN)


@dp.message_handler(commands=['acta'])
async def act(message: types.Message):
    mail = f"<b>Актировка за {'.'.join(reversed(str(db.get_data()[0]).split('-')))}</b>\n"

    for part in [1, 2]:
        mail = mail + f"\n<b>Для {part}-ой смены:</b>\n"
        if db.check_acta(part):
            cities = config.NAMES
            city = db.get_acta(part)

            for i, town in enumerate(city):
                if str(town) != "нет":
                    mail = mail + f"<b>*</b> В {morph.parse(cities[i])[0].inflect({'loct'}).word.title()} актировка " \
                                  f"с 1 по {town} классы!\n"
                else:
                    mail = mail + f"<b>*</b> В {morph.parse(cities[i])[0].inflect({'loct'}).word.title()} актировки нет!\n"

        else:
            mail = mail + "На данный момент информации на сайте нету!\n\n"
    await message.answer(mail, parse_mode=types.ParseMode.HTML)


@dp.message_handler(commands=['weather'])
async def storm(message: types.Message):
    text = message.text.split()
    try:
        day = int(text[1])
        if 0 <= day <= 9:
            weather = db.get_weather(day)

            txt = "<b>Погода:</b>\n\n"
            for hour in weather:
                dat = weather[hour]
                if len(dat[1]) == 2:
                    par = f"{dat[1][0]}-{dat[1][1]}"
                else:
                    par = str(dat[1][0])
                txt = txt + f"<b>В {hour}:</b>\n  Температура: {dat[0]}\n  Скорость и порывы ветра: {par}\n  Направление ветра: {dat[2]}\n  Осадки: {dat[3]}\n\n"

            await message.answer(txt, parse_mode=types.ParseMode.HTML)
        else:
            raise NameError('Число не вподходящем диапозоне!')
    except Exception:
        await message.answer("Введи число дня по счёту от сегодня, погода которого тебе нужна!\n\nТо есть:\nСегодня - {/waether 0}\nЗавтра - {/weather 1}", 
                             parse_mode=types.ParseMode.MARKDOWN)


@dp.message_handler(commands=['help'])
async def main(message: types.Message):
    await message.answer('*Инструкция использования:*\n\n'
                         '*/town* - с помощью этой команды вы можете изменить данные о городе и смене обучения\n'
                         '*/acta* - команда, выдающая данные об актировке на все города на данный момент\n'
                         '*/storm* - команда, выдающая данные о штормовом предупреждении\n'
                         '*/letter* - команда, позваляющая подписаться на утреннюю рассылку о наличии актировки\n'
                         '*/notice* - команда, дающая выбор - получать уведомления в любом случае или только при '
                         'наличии актировки\n', types.ParseMode.MARKDOWN)


# УВЕДОМЛЕНИЕ
async def timer(wait_for):
    while True:
        await asyncio.sleep(wait_for)
        city, part = info.act()

        if city:
            date_old, part_old = db.get_data()
            date_now, part_num = str(dt.now().date()), int(part[0])

            if (part_num == 1 and date_old != date_now) or (part_num == 2 and date_old == date_now):
                if part_old != part_num:
                    db.update_data(dt.now().date(), part_num)
                    db.save_acta(city, part_num)
                    for twn in city:
                        town = morph.parse(twn[0][1])[0].inflect({'datv'}).word
                        if isinstance(twn[1], int):
                            for s in db.get_users(part_num, twn[0][0]):
                                try:
                                    await bot.send_sticker(chat_id=s, sticker=config.ID_STICKERS + config.STICKERS[1])
                                    await bot.send_message(chat_id=s, text=f"*Для {part} по {town.title()} объявлена актировка c 1 по {twn[1]} классы!*",
                                                           parse_mode=types.ParseMode.MARKDOWN)
                                except Exception as e:
                                    print(repr(e))
                                    db.update_status(s)
                        else:
                            for s in db.get_sends(part_num, twn[0][0]):
                                try:
                                    await bot.send_sticker(chat_id=s, sticker=config.ID_STICKERS + config.STICKERS[6])
                                    await bot.send_message(chat_id=s, text=f"*Для {part} по {town.title()} актировка отсутствует!",
                                                           parse_mode=types.ParseMode.MARKDOWN)
                                except Exception as e:
                                    print(repr(e))
                                    db.update_status(s)
                        print("---------------------------------")


# ОБНОВЛЕНИЕ ДАННЫХ О ПОГОДЫ 
async def wind(wait_for):
    while True:
        await asyncio.sleep(wait_for)
        for moment in db.get_moments():
            weather = info.weather(moment)

            if type(weather) == dict:
                for tm in weather:
                    db.update_weather(weather[tm], moment, tm)
            else:
                print(weather)
            time.sleep(10)


# ОЧИСТКА ДАННЫХ ОБ АКТИРОВКАХ
async def clear(wait_for):
    while True:
        await asyncio.sleep(wait_for)

        if (db.get_data()[0] != str(dt.now().date())) and (db.check_acta(1) or db.check_acta(2)):
            db.del_acta()


# ЗАПУСК ЛОНГ ПОЛЛИНГА
if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(timer(60))  # ПРОВЕРКА МЕТЕО НОРИЛЬСК КАЖДУЮ МИНУТУ
    loop.create_task(clear(300))  # ПРОВЕРКА НА НОВЫЙ ДЕНЬ КАЖДЫЕ 10 МИНУТ
    loop.create_task(wind(1200))  # ПРОВЕРКА НА ОБНОВЛЕНИЕ ПОГОДЫ КАЖДЫЕ 20 МИНУТ
    executor.start_polling(dp, skip_updates=True)
