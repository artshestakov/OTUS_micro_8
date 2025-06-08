import requests
from enum import Enum
from flask import Flask, jsonify, request
# ----------------------------------------------------------------------------------------------------------------------
app = Flask(__name__)
# ----------------------------------------------------------------------------------------------------------------------
class SERVICE_PORT(Enum):
    PAYMENT = 5000,
    STOCK = 5001,
    DELIVERY = 5002
# ----------------------------------------------------------------------------------------------------------------------
@app.route('/orders', methods=['POST'])
def create_order():
    data = request.json
    order_id = data['order_id']

    # Сходим в сервис платежей и свалидируем платёж
    try:

        payment_resp = requests.post(
            f"http://127.0.0.1:{SERVICE_PORT.PAYMENT}/payments/validate",
            json={'order_id': order_id, 'amount': data['amount']},
            timeout=5)

        payment_resp.raise_for_status()
    except Exception as e:
        return jsonify({'error': f'Payment failed: {str(e)}'}), 400

    # Идём на "склад" и делаем резерв
    try:

        stock_resp = requests.post(
            f"http://127.0.0.1:{SERVICE_PORT.STOCK}/stock/reserve",
            json={'order_id': order_id, 'items': data['items']},
            timeout=5)

        stock_resp.raise_for_status()
    except Exception as e:

        # Компенсируем
        requests.post(f"http://127.0.0.1:{SERVICE_PORT.PAYMENT}/payments/cancel", json={'order_id': order_id})
        return jsonify({'error': f'Stock reservation failed: {str(e)}'}), 400

    # Резервируем доставку
    try:

        delivery_resp = requests.post(
            f"http://127.0.0.1:{SERVICE_PORT.DELIVERY}/delivery/reserve",
            json={'order_id': order_id, 'address': data['address'], 'timeslot': data['timeslot']},
            timeout=5)

        delivery_resp.raise_for_status()
    except Exception as e:

        # Компенсируем
        requests.post(f"http://127.0.0.1:{SERVICE_PORT.PAYMENT}/payments/cancel", json={'order_id': order_id})
        requests.post(f"http://127.0.0.1:{SERVICE_PORT.STOCK}/stock/release", json={'order_id': order_id})
        return jsonify({'error': f'Delivery reservation failed: {str(e)}'}), 400

    return jsonify({'status': 'Order created successfully'}), 201
# ----------------------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=50000)
# ----------------------------------------------------------------------------------------------------------------------
