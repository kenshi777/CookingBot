from cgitb import text
import requests
from pprint import pprint
from config import TOKEN
from aiogram import Bot, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

bot = Bot(token=TOKEN)
disp = Dispatcher(bot)

button_1 = KeyboardButton('/Lets_go!')
button_2 = KeyboardButton('/help')
button_3 = KeyboardButton('/breakfast')
button_4 = KeyboardButton('/lunch')
button_5 = KeyboardButton('/dinner')
button_6 = KeyboardButton('/dessert')
button_7 = KeyboardButton('/back')


keyboard_1 = ReplyKeyboardMarkup(resize_keyboard=True)
keyboard_1.add(button_1).add(button_2)

keyboard_2 = ReplyKeyboardMarkup(resize_keyboard=True)
keyboard_2.row(button_3, button_4, button_5, button_6, button_7)

@disp.message_handler(commands=['start','help'])
async def start_command(message: types.message):
    await message.reply("Hi! I'm a cooking bot! I'll help you choose a dish. Just follow the instructions I'm writing you. Bon Appetit!", reply_markup=keyboard_1)
@disp.message_handler(commands=['Lets_go!'])
async def first_step(message: types.message):
    await message.reply("Good! What do you want to cook?", reply_markup=keyboard_2)
@disp.message_handler(commands=['breakfast'])
async def breakfast(message: types.message):
    breakfast_requests = requests.get(
        f"https://www.themealdb.com/api/json/v1/1/filter.php?c=Breakfast"
    ).json()
    list_of_breakfast_meal = []
    for i in range(len(breakfast_requests['meals'])):
        list_of_breakfast_meal.append(breakfast_requests['meals'][i]['strMeal'])
    breakfast_buttons = [InlineKeyboardButton(list_of_breakfast_meal[i], callback_data=i) for i in range(len(list_of_breakfast_meal))]
    breakfast_inline_keyboard = InlineKeyboardMarkup()
    for j in range(len(breakfast_buttons)):
        breakfast_inline_keyboard.add(breakfast_buttons[j])
    print(breakfast_buttons)
    await message.reply("Choose a meal:", reply_markup=breakfast_inline_keyboard)
for i in range(len(requests.get("https://www.themealdb.com/api/json/v1/1/filter.php?c=Breakfast").json()['meals'])):  ##исправить ошибку
    @disp.callback_query_handler(text=i)
    async def callback(call: types.CallbackQuery):
        try:
            r = requests.get(
                f"http://www.themealdb.com/api/json/v1/1/search.php?s={i}"
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
            tags = r['meals'][0]['strTags']
            video = r['meals'][0]['strYoutube']
            await call.message.answer(
                f"Meal: {name}\nCountry: {country}\nCategory: {category}\nIngredients: {ingredients_list}\nMesaures: {measures_list}\nInstruction: {instruction}\nTags: {tags}\nYoutube: {video}\nEnjoy your meal!"
            )
            await call.answer()
        except:
            await call.message.answer(text="Unknown meal!")
            await call.answer()



@disp.message_handler()
async def get_meal(message: types.message):
    try:
        r = requests.get(
            f"http://www.themealdb.com/api/json/v1/1/search.php?s={message.text}"
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
        tags = r['meals'][0]['strTags']
        video = r['meals'][0]['strYoutube']
        await message.reply(
            f"Meal: {name}\nCountry: {country}\nCategory: {category}\nIngredients: {ingredients_list}\nMesaures: {measures_list}\nInstruction: {instruction}\nTags: {tags}\nYoutube: {video}\nEnjoy your meal!"
        )
    except:
        await message.reply("Unknown meal!")

if __name__ == "__main__":
    executor.start_polling(disp)