from dataclasses import dataclass


BASE_URL = 'https://www.mcdonalds.com/ua/uk-ua/eat/fullmenu.html'
SINGLE_PAGE_URL = 'https://www.mcdonalds.com/dnaapp/itemDetails?country=UA&language=uk&showLiveData=true&item='


class ProductSuit:
    CALORIES = 'calories'
    FATS = 'fats'
    CARBS = 'carbs'
    PROTEINS = 'proteins'
    UNSATURATED = 'unsaturated'
    SUGAR = 'sugar'
    SALT = 'salt'
    PORTION = 'portion'


@dataclass
class Product:
    name: str
    description: str
    product_suits: dict
