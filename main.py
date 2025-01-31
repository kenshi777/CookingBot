from email import message
from unicodedata import name
import requests
from pprint import pprint

def get_meal(meal):
    #try:
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
        print(
            f"Meal: {name}\nCountry: {country}\nCategory: {category}\nIngredients: {ingredients_result}\nInstruction: {instruction}\nTags: {tags}\nYoutube: {video}\nEnjoy your meal!"
        )
    #except:
        #print("Unknown meal!")

def main():
    meal = input("Enter meal: ")
    get_meal(meal)


if __name__ == '__main__':
    main()