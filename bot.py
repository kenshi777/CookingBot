from cgitb import text
from email import message
import re
import requests
from pprint import pprint
from config import TOKEN
from aiogram import Bot, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from random import randint

bot = Bot(token=TOKEN)
disp = Dispatcher(bot)


req_category = requests.get(
        f"https://www.themealdb.com/api/json/v1/1/categories.php"
    ).json()

list_of_lunch_category = []
for i in [1, 5, 8, 9, 13]:
    list_of_lunch_category.append(req_category['categories'][i]['strCategory'])
list_of_dinner_category = []
for i in [0, 3, 4, 6, 7]:
    list_of_dinner_category.append(req_category['categories'][i]['strCategory'])


def get_info(meal):
    r = requests.get(
            f"http://www.themealdb.com/api/json/v1/1/search.php?s={meal}"
        ).json()
    name = r['meals'][0]['strMeal']
    country = r['meals'][0]['strArea']
    category = r['meals'][0]['strCategory']
    ingredients_list = []
    for i in range(1, 20):
        if (r['meals'][0][f'strIngredient{i}'] != '') and (r['meals'][0][f'strIngredient{i}'] != None) and (r['meals'][0][f'strMeasure{i}'] != ' '):
            ingredients_list.append(r['meals'][0][f'strIngredient{i}'])
            
    instruction = r['meals'][0]['strInstructions']
    image = r['meals'][0]['strMealThumb']
    measures_list = []
    for m in range(1, 20):
        if (r['meals'][0][f'strMeasure{m}'] != '') and (r['meals'][0][f'strMeasure{m}'] != None) and (r['meals'][0][f'strMeasure{m}'] != ' '):
            measures_list.append(r['meals'][0][f'strMeasure{m}'])
    ingredients_result = []
    for l in range(len(ingredients_list)):
        ingredients_result.append(ingredients_list[l]+' '+measures_list[l])
    tags = r['meals'][0]['strTags']
    video = r['meals'][0]['strYoutube']
    text = f"Meal: {name}\nCountry: {country}\nCategory: {category}\nIngredients: {ingredients_result}\nInstruction: {instruction}\nTags: {tags}\nYoutube: {video}\nEnjoy your meal!"
    return text
def get_meal_from_category(category, n):
    req = requests.get(
            f"https://www.themealdb.com/api/json/v1/1/filter.php?c={category}"
        ).json()
    list_of_requests = []
    for i in range(len(req['meals'])):
        list_of_requests.append(req['meals'][i]['strMeal'])
        if len(list_of_requests[i]) > 50:
            list_of_requests[i] = list_of_requests[i][0:40]
    if n == 'all':
        final_list = list_of_requests
    if type(n) == int:
        if (len(list_of_requests) / 10) > n:
            final_list = list_of_requests[10*(n-1):10*n]
        if (len(list_of_requests)) < 10:
            final_list = list_of_requests[0:len(list_of_requests)]
        if ((len(list_of_requests) / 10) < n) and ((len(list_of_requests)) > 10): 
            final_list = list_of_requests[(len(list_of_requests)-10):len(list_of_requests)]
    return final_list

k = 1

button_1 = KeyboardButton('/Lets_go!')
button_2 = KeyboardButton('/help')
button_3 = KeyboardButton('/breakfast')
button_4 = KeyboardButton('/lunch')
button_5 = KeyboardButton('/dinner')
button_6 = KeyboardButton('/dessert')
button_7 = KeyboardButton('/back')

button_8 = KeyboardButton('/vegan')
button_9 = KeyboardButton('/vegetarian')


keyboard_1 = ReplyKeyboardMarkup(resize_keyboard=True)
keyboard_1.add(button_1).add(button_2)

keyboard_2 = ReplyKeyboardMarkup(resize_keyboard=True)
keyboard_2.row(button_3, button_4, button_5, button_6, button_7).row(button_8, button_9)


@disp.message_handler(commands=['start','help', 'back'])
async def start_command(message: types.Message):
    global k
    await message.reply("Hi! I'm a cooking bot! I'll help you choose a dish. Just follow the instructions I'm writing you. Bon Appetit!", reply_markup=keyboard_1)
    k = 1

@disp.message_handler(commands=['Lets_go!'])
async def first_step(message: types.Message):
    await message.reply("Good! What do you want to cook?", reply_markup=keyboard_2)

@disp.message_handler(commands=['breakfast'])
async def breakfast(message: types.Message):
    get_list = get_meal_from_category('Breakfast', k)
    buttons = [InlineKeyboardButton(get_list[i], callback_data=f"breakfast_{get_list[i]}") for i in range(len(get_list))]
    inline_keyboard = InlineKeyboardMarkup()
    for j in range(len(buttons)):
        inline_keyboard.add(buttons[j])
    inline_keyboard.add(InlineKeyboardButton('Random', callback_data='random_breakfast'))
    await message.reply("Choose a meal:", reply_markup=inline_keyboard)

@disp.message_handler(commands=['vegan'])
async def vegan(message: types.Message):
    get_list = get_meal_from_category('Vegan', k)
    buttons = [InlineKeyboardButton(get_list[i], callback_data=f"vegan_{get_list[i]}") for i in range(len(get_list))]
    inline_keyboard = InlineKeyboardMarkup()
    for j in range(len(buttons)):
        inline_keyboard.add(buttons[j])
    await message.reply("Choose a meal:", reply_markup=inline_keyboard)

@disp.message_handler(commands=['dessert'])
async def dessert(message: types.Message):
    global k
    get_list = get_meal_from_category('Dessert', k)
    buttons = [InlineKeyboardButton(get_list[i], callback_data=f"dessert_{get_list[i]}") for i in range(len(get_list))]
    inline_keyboard = InlineKeyboardMarkup()
    for j in range(len(buttons)):
        inline_keyboard.add(buttons[j])
    inline_keyboard.add(InlineKeyboardButton('More', callback_data=f'more_dessert_{k}_Dessert'))
    await message.reply("Choose a meal:", reply_markup=inline_keyboard)
    k=2

@disp.message_handler(commands=['vegetarian'])
async def vegetarian(message: types.Message):
    global k
    get_list = get_meal_from_category('Vegetarian', k)
    buttons = [InlineKeyboardButton(get_list[i], callback_data=f"vegetarian_{get_list[i]}") for i in range(len(get_list))]
    inline_keyboard = InlineKeyboardMarkup()
    for j in range(len(buttons)):
        inline_keyboard.add(buttons[j])
    inline_keyboard.add(InlineKeyboardButton('More', callback_data=f'more_vegetarian_{k}_Vegetarian'))
    await message.reply("Choose a meal:", reply_markup=inline_keyboard)
    k=2

@disp.message_handler(commands=['lunch'])
async def lunch(message: types.Message):
    global k
    k = 1
    buttons = [InlineKeyboardButton(list_of_lunch_category[i], callback_data=f"lunch_category_{list_of_lunch_category[i]}") for i in range(len(list_of_lunch_category))]
    inline_keyboard = InlineKeyboardMarkup()
    for j in range(len(buttons)):
        inline_keyboard.add(buttons[j])
    await message.reply("Choose a category:", reply_markup=inline_keyboard)

@disp.message_handler(commands=['dinner'])
async def dinner(message: types.Message):
    global k
    k = 1
    buttons = [InlineKeyboardButton(list_of_dinner_category[i], callback_data=f"dinner_category_{list_of_dinner_category[i]}") for i in range(len(list_of_dinner_category))]
    inline_keyboard = InlineKeyboardMarkup()
    for j in range(len(buttons)):
        inline_keyboard.add(buttons[j])
    await message.reply("Choose a category:", reply_markup=inline_keyboard)

@disp.callback_query_handler(lambda x : x.data and x.data.startswith('breakfast_'))
async def callback_breakfast(callback_query: types.CallbackQuery):
    try:
        await bot.send_message(callback_query.from_user.id, get_info(callback_query.data[10:]))
    except:
        await bot.send_message(callback_query.from_user.id, "Unknown meal!")
    await callback_query.answer(callback_query.data[10:])

@disp.callback_query_handler(lambda x : x.data and x.data.startswith('vegan_'))
async def callback_vegan(callback_query: types.CallbackQuery):
    try:
        await bot.send_message(callback_query.from_user.id, get_info(callback_query.data[6:]))
    except:
        await bot.send_message(callback_query.from_user.id, "Unknown meal!")
    await callback_query.answer(callback_query.data[6:])

@disp.callback_query_handler(lambda x : x.data and x.data.startswith('dessert_'))
async def callback_dessert(callback_query: types.CallbackQuery):
    try:
        await bot.send_message(callback_query.from_user.id, get_info(callback_query.data[8:]))
    except:
        await bot.send_message(callback_query.from_user.id, "Unknown meal!")
    await callback_query.answer(callback_query.data[8:])

@disp.callback_query_handler(lambda x : x.data and x.data.startswith('vegetarian_'))
async def callback_vegetarian(callback_query: types.CallbackQuery):
    try:
        await bot.send_message(callback_query.from_user.id, get_info(callback_query.data[11:]))
    except:
        await bot.send_message(callback_query.from_user.id, "Unknown meal!")
    await callback_query.answer(callback_query.data[11:])

@disp.callback_query_handler(lambda x : x.data and x.data.startswith('lunch_category_'))
async def callback_lunch(callback_query: types.CallbackQuery):
    global k
    try:
        get_list = get_meal_from_category(callback_query.data[15:], k)
        buttons = [InlineKeyboardButton(get_list[i], callback_data=f"lunch_meal_{get_list[i]}") for i in range(len(get_list))]
        inline_keyboard = InlineKeyboardMarkup()
        for j in range(len(buttons)):
            inline_keyboard.add(buttons[j])
        inline_keyboard.add(InlineKeyboardButton('More', callback_data=f'more_lunch_{k}_{callback_query.data[15:]}'))
        inline_keyboard.add(InlineKeyboardButton('Random', callback_data=f'random_lunch_{callback_query.data[15:]}'))
        await bot.send_message(callback_query.from_user.id, "Choose a meal:", reply_markup=inline_keyboard)
        k=2
    except:
        await bot.send_message(callback_query.from_user.id, "Unknown meal!")
    await callback_query.answer(callback_query.data[15:])

@disp.callback_query_handler(lambda x : x.data and x.data.startswith('lunch_meal_'))
async def callback_lunch_meal(callback_query: types.CallbackQuery):
    try:
        await bot.send_message(callback_query.from_user.id, get_info(callback_query.data[11:]))
    except:
        await bot.send_message(callback_query.from_user.id, "Unknown meal!")
    await callback_query.answer(callback_query.data[11:])

@disp.callback_query_handler(lambda x : x.data and x.data.startswith('dinner_category_'))
async def callback_dinner(callback_query: types.CallbackQuery):
    global k
    try:
        get_list = get_meal_from_category(callback_query.data[16:], k)
        buttons = [InlineKeyboardButton(get_list[i], callback_data=f"dinner_meal_{get_list[i]}") for i in range(len(get_list))]
        inline_keyboard = InlineKeyboardMarkup()
        for j in range(len(buttons)):
            inline_keyboard.add(buttons[j])
        inline_keyboard.add(InlineKeyboardButton('More', callback_data=f'more_dinner_{k}_{callback_query.data[16:]}'))
        inline_keyboard.add(InlineKeyboardButton('Random', callback_data=f'random_dinner_{callback_query.data[16:]}'))
        await bot.send_message(callback_query.from_user.id, "Choose a meal:", reply_markup=inline_keyboard)
        k=2
    except:
        await bot.send_message(callback_query.from_user.id, "Unknown meal!")
    await callback_query.answer(callback_query.data[16:])

@disp.callback_query_handler(lambda x : x.data and x.data.startswith('dinner_meal_'))
async def callback_dinner_meal(callback_query: types.CallbackQuery):
    try:
        await bot.send_message(callback_query.from_user.id, get_info(callback_query.data[12:]))
    except:
        await bot.send_message(callback_query.from_user.id, "Unknown meal!")
    await callback_query.answer(callback_query.data[12:])

@disp.callback_query_handler(lambda x : x.data and x.data.startswith('more_lunch_'))
async def more_lunch(callback_query: types.CallbackQuery):
    global k
    get_list = get_meal_from_category(callback_query.data[13:], k)
    buttons = [InlineKeyboardButton(get_list[i], callback_data=f"lunch_meal_{get_list[i]}") for i in range(len(get_list))]
    inline_keyboard = InlineKeyboardMarkup()
    for j in range(len(buttons)):
        inline_keyboard.add(buttons[j])
    inline_keyboard.add(InlineKeyboardButton('More', callback_data=f'more_lunch_{k}_{callback_query.data[13:]}'))
    await bot.send_message(callback_query.from_user.id, "Choose a meal:", reply_markup=inline_keyboard)
    await callback_query.answer(callback_query.data[13:])
    k+=1

@disp.callback_query_handler(lambda x : x.data and x.data.startswith('more_dinner_'))
async def more_dinner(callback_query: types.CallbackQuery):
    global k
    get_list = get_meal_from_category(callback_query.data[14:], k)
    buttons = [InlineKeyboardButton(get_list[i], callback_data=f"lunch_meal_{get_list[i]}") for i in range(len(get_list))]
    inline_keyboard = InlineKeyboardMarkup()
    for j in range(len(buttons)):
        inline_keyboard.add(buttons[j])
    inline_keyboard.add(InlineKeyboardButton('More', callback_data=f'more_lunch_{k}_{callback_query.data[14:]}'))
    await bot.send_message(callback_query.from_user.id, "Choose a meal:", reply_markup=inline_keyboard)
    await callback_query.answer(callback_query.data[14:])
    k+=1

@disp.callback_query_handler(lambda x : x.data and x.data.startswith('more_dessert_'))
async def more_dessert(callback_query: types.CallbackQuery):
    global k
    get_list = get_meal_from_category(callback_query.data[15:], k)
    buttons = [InlineKeyboardButton(get_list[i], callback_data=f"lunch_meal_{get_list[i]}") for i in range(len(get_list))]
    inline_keyboard = InlineKeyboardMarkup()
    for j in range(len(buttons)):
        inline_keyboard.add(buttons[j])
    inline_keyboard.add(InlineKeyboardButton('More', callback_data=f'more_dessert_{k}_{callback_query.data[15:]}'))
    await bot.send_message(callback_query.from_user.id, "Choose a meal:", reply_markup=inline_keyboard)
    await callback_query.answer(callback_query.data[15:])
    k+=1

@disp.callback_query_handler(lambda x : x.data and x.data.startswith('more_vegetarian_'))
async def more_vegetarian(callback_query: types.CallbackQuery):
    global k
    get_list = get_meal_from_category(callback_query.data[18:], k)
    buttons = [InlineKeyboardButton(get_list[i], callback_data=f"lunch_meal_{get_list[i]}") for i in range(len(get_list))]
    inline_keyboard = InlineKeyboardMarkup()
    for j in range(len(buttons)):
        inline_keyboard.add(buttons[j])
    inline_keyboard.add(InlineKeyboardButton('More', callback_data=f'more_vegetarian_{k}_{callback_query.data[18:]}'))
    await bot.send_message(callback_query.from_user.id, "Choose a meal:", reply_markup=inline_keyboard)
    await callback_query.answer(callback_query.data[18:])
    k+=1

@disp.callback_query_handler(lambda x : x.data and x.data.startswith('random_breakfast'))
async def random_breakfast(callback_query: types.CallbackQuery):
    get_list = get_meal_from_category('Breakfast', 1)
    await bot.send_message(callback_query.from_user.id, get_info(get_list[randint(0, len(get_list))]))
    await callback_query.answer('Random')

@disp.callback_query_handler(lambda x : x.data and x.data.startswith('random_lunch_'))
async def random_breakfast(callback_query: types.CallbackQuery):
    get_list = get_meal_from_category(callback_query.data[13:], 'all')
    await bot.send_message(callback_query.from_user.id, get_info(get_list[randint(0, len(get_list))]))
    await callback_query.answer('Random')

@disp.callback_query_handler(lambda x : x.data and x.data.startswith('random_dinner_'))
async def random_breakfast(callback_query: types.CallbackQuery):
    get_list = get_meal_from_category(callback_query.data[14:], 'all')
    await bot.send_message(callback_query.from_user.id, get_info(get_list[randint(0, len(get_list))]))
    await callback_query.answer('Random')


@disp.message_handler()
async def get_meal(message: types.message):
    try:
        await message.reply(get_info(message.text))
    except:
        await message.reply("Unknown meal!")


if __name__ == "__main__":
    executor.start_polling(disp)