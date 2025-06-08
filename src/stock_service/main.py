from flask import Flask, jsonify, request
# ----------------------------------------------------------------------------------------------------------------------
app = Flask(__name__)
inventory = {'item1': 100, 'item2': 50}  # Просто как пример
reservations = {}
# ----------------------------------------------------------------------------------------------------------------------
@app.route('/stock/reserve', methods=['POST'])
def reserve_stock():
    data = request.json
    order_id = data['order_id']

    # Проверяем доступность товаров
    for item, quantity in data['items'].items():
        if inventory.get(item, 0) < quantity:
            return jsonify({'error': f'Not enough stock for {item}'}), 400

    # Резервируем товары
    for item, quantity in data['items'].items():
        inventory[item] -= quantity

    reservations[order_id] = data['items']
    return jsonify({'status': 'Stock reserved'}), 200
# ----------------------------------------------------------------------------------------------------------------------
@app.route('/stock/release', methods=['POST'])
def release_stock():

    order_id = request.json['order_id']

    # Если такой заказ есть в резерве - снимаем
    if order_id in reservations:
        for item, quantity in reservations[order_id].items():
            inventory[item] += quantity
        del reservations[order_id]

    return jsonify({'status': 'Stock released'}), 200
# ----------------------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
# ----------------------------------------------------------------------------------------------------------------------
