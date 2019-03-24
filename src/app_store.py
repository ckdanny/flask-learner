from flask import Flask, jsonify, request

app = Flask(__name__)
app.config['DEBUG'] = True

stores = [
    {
        'name': "My wonderful store",
        'items': [
            {
                'name': 'iPhone 7',
                'price': 15.99
            }

        ]
    }
]


@app.route('/store', methods=['POST'])  # default method is GET
def create_store():
    # to access the data in the request, `from flask import request`
    request_data = request.get_json()
    new_store = {
        'name': request_data['name'],
        'items': []
    }
    stores.append(new_store)
    # with app.app_context():
    return get_stores()


@app.route('/store/<string:name>')  # 'http://localhost:5000/store/some_name'
def get_store(name):
    for store in stores:
        if store['name'] == name:
            return jsonify(store)
    return jsonify({"status": 'Fail', "message": 'No store found'})


@app.route('/store')
def get_stores():
    return jsonify({'stores': tuple(map(lambda store: store['name'], stores))})


@app.route('/store/<string:name>/item', methods=['POST'])
def create_item_in_store(name):
    for store in stores:
        if store['name'] == name:
            store['items'].append(request.get_json())
            return jsonify({'status': True})
    return jsonify({'status': False, 'message': "no store found."})


@app.route('/store/<string:name>/item')
def get_items_in_store(name):
    store_details = get_store(name)
    return jsonify({'items': store_details.get_json()['items']})

if __name__ == "__main__":
    app.run(port=5000)


