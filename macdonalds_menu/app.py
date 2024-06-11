from flask import Flask, jsonify, abort
import json

app = Flask(__name__)


def load_json_data(src_filepath: str):
    with open(src_filepath, 'r', encoding='utf-8') as file:
        return json.load(file)


# TODO: Input source json filepath
products = load_json_data('dst_filepath')


@app.route('/all_products/', methods=['GET'])
def get_all_products():
    return jsonify(products)


@app.route('/products/<string:product_name>', methods=['GET'])
def get_product(product_name: str):
    product = next((product for product in products if product['name'] == product_name), None)
    if product is None:
        abort(404, description="Product not found")
    return jsonify(product)


@app.route('/products/<string:product_name>/<string:product_field>', methods=['GET'])
def get_product_field(product_name: str, product_field: str):
    product = next((product for product in products if product['name'] == product_name), None)
    if product is None:
        abort(404, description="Product not found")

    if product_field in product:
        return jsonify({product_field: product[product_field]})
    elif product_field in product['product_suits']:
        return jsonify({product_field: product['product_suits'][product_field]})
    else:
        abort(404, description="Field not found")


def main():
    app.run(debug=True, host='0.0.0.0', port=8000)


if __name__ == '__main__':
    main()
