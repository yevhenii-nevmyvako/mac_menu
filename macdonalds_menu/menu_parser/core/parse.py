import logging

import requests
from bs4 import BeautifulSoup
from requests import HTTPError

from macdonalds_menu.menu_parser.core.const import ProductSuit, Product, BASE_URL, SINGLE_PAGE_URL
from macdonalds_menu.menu_parser.core.save_to_json import save_data_to_json


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("parser.log"),
        logging.StreamHandler()
    ]
)


def set_product_suits(nutrient_facts: dict) -> dict:
    """Sets product suits with params.

    Args:
        nutrient_facts: Dict of source suit.

    Returns:
        Dict of product suits after filtering.

    """

    nutrient_data = {}
    for nutrient in nutrient_facts:
        if nutrient['name'] != 'Ен. Цінність, кДж':
            category = nutrient['name']
            if category == 'Жири':
                category = ProductSuit.FATS
            if category == 'Калорійність':
                category = ProductSuit.CALORIES
            if category == 'НЖК':
                category = ProductSuit.UNSATURATED
            if category == 'Вуглеводи':
                category = ProductSuit.CARBS
            if category == 'Цукор':
                category = ProductSuit.SUGAR
            if category == 'Білки':
                category = ProductSuit.PROTEINS
            if category == 'Вага порції':
                category = ProductSuit.PORTION
            if category == 'Сіль':
                category = ProductSuit.SALT

            nutrient_data[category] = {
                'value': nutrient['value'],
                'uom': nutrient['uom']
            }

    return nutrient_data


def get_product_ids() -> list:
    """Gest product ids.

    Returns:
        List product ids.

    """
    response = requests.get(BASE_URL).content
    soup = BeautifulSoup(response, 'html.parser')
    page_soup = soup.find_all('li', {'data-product-id': True})
    product_ids = [element['data-product-id'] for element in page_soup]
    logging.info(f"Fetched product ids: {product_ids}")
    return product_ids


def get_product_data() -> list:
    """Gest list of product data from Api.

    Returns:
        List of filtered products.

    """
    product_page_ids = get_product_ids()
    products = []
    for page in product_page_ids:
        try:
            response = requests.get(f'{SINGLE_PAGE_URL}{page}')
            response.raise_for_status()
            product_param = response.json()['item']
            nutrient_facts = product_param.get('nutrient_facts', {}).get('nutrient', [])

            if not nutrient_facts:
                if not nutrient_facts:
                    logging.warning(f"No nutrient facts found for product ID {page}")
                    continue
                continue

            name, description = product_param['item_name'], product_param['description']
            suits = set_product_suits(nutrient_facts)
            products.append(Product(name=name, description=description, product_suits=suits))
            logging.info(f"Processed product: {name}")

        except (HTTPError, KeyError) as e:
            print(f"Error when processing goods with ID {page}: {e}")
            continue
    return products


def product_to_dict(product: Product) -> dict:
    """Gets dicts of product

    Args:
        product: Product from menu.

    Returns:
        Dict of product.

    """
    return {
        'name': product.name,
        'description': product.description,
        'product_suits': product.product_suits,
    }


def save_product_to_json(dst_filepath: str) -> None:
    products = get_product_data()
    save_data_to_json([product_to_dict(product) for product in products], dst_filepath)
    logging.info(f"Saved products data to {dst_filepath}")
