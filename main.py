from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.types import InputFile

from config import TOKEN
from keyboard import Help, Choice
from dialog import Dialog
from database import Database

# INITIALIZATION
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start', 'stop'])
async def start_command(message: types.Message):
    bot_status.status = '/rest'
    await bot.send_message(message.from_user.id, "Привет")


@dp.message_handler(commands=['help'])
async def help_command(message: types.Message):
    text = '''Привет-привет!
     Многофункциональный бот тебя приветствует!
     Внизу ты увидишь пулл команд, которые ты волен нажимать.
     Название пишутся только на английском, так как сайт на аннглийском.
     Вот объяснение
     /find - найти аниме на myanimelist
     /trailer - посмотреть трейлер аниме
     /poster - посмотреть постер аниме
     /stop - чтобы выйти из режима
     Надеюсь тебе понравиться :)'''
    kb = Help()
    kb.add('/find', '/trailer', '/poster')
    await bot.send_message(message.from_user.id, text, reply_markup=kb.keyboard)


@dp.message_handler(commands=['find', 'trailer', 'poster'])
async def find_command(message: types.Message):
    kb.page = 1
    bot_status.change(message.text)
    print(bot_status.status)
    await bot.send_message(message.from_user.id, "Напишите, пожалуйста, название:")


@dp.callback_query_handler(lambda c: c.data and c.data in ['next', 'back'])
async def callback_extension_moment(callback_query: types.CallbackQuery):
    if (callback_query.data == 'back' and kb.page == 1) or \
            (callback_query.data == 'next' and kb.page == len(kb.buttons) / 5):
        pass
    elif callback_query.data == 'next':
        kb.page += 1
    else:
        kb.page -= 1
    kb1 = Choice(kb.page, kb.buttons)
    kb1.print_btns(5)
    if kb.page == 1:
        kb1.next()
    elif kb.page == len(kb.buttons) / 5:
        kb1.back()
    else:
        kb1.both()
    await callback_query.message.edit_reply_markup(reply_markup=kb1.keyboard)


@dp.callback_query_handler(lambda c: c.data)
async def callback_moment(callback_query: types.CallbackQuery):
    text = db[int(callback_query.data)]
    if bot_status.status == '/find':
        await bot.send_message(callback_query.from_user.id, "Ссылка загружается. Пожалуйста подождите...")
        await bot.send_message(callback_query.from_user.id, text)
    elif bot_status.status == '/poster':
        await bot.send_message(callback_query.from_user.id, "Картинка загружается. Пожалуйста подождите...")
        url = await bot_status.handle_poster(text)
        if url:
            file = InputFile(url, filename='poster')
            await bot.send_photo(callback_query.from_user.id, photo=file)
        else:
            await bot.send_message(callback_query.from_user.id, "Постера на сайте нет.")
    elif bot_status.status == '/trailer':
        await bot.send_message(callback_query.from_user.id, "Трейлер загружается. Пожалуйста подождите...")
        url = await bot_status.handle_trailer(text)
        if url:
            file = InputFile(url, filename='trailer')
            await bot.send_video(callback_query.from_user.id, video=file)
        else:
            await bot.send_message(callback_query.from_user.id, "Трейлера на сайте нет.")


@dp.message_handler()
async def message_moment(message: types.Message):
    global kb
    print(bot_status.status)
    if bot_status.status != "/rest":
        await bot.send_message(message.from_user.id, "Ваш запрос обрабатывается, подождите..")
        answer, res = bot_status.handle_call(message.text)
        if res:
            kb = Choice(kb.page, res)
            kb.print_btns(5)
            kb.next()
            await message.reply(answer, reply_markup=kb.keyboard)
        else:
            await message.reply("Ничего не найдено!")
    else:
        await bot.send_message(message.from_user.id, "Выберите, пожалуйста, любую команду...")


if __name__ == '__main__':
    bot_status = Dialog()
    db = Database()
    kb = Choice()
    executor.start_polling(dp)
    db.close()
