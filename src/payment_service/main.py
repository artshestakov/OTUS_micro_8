from flask import Flask, jsonify, request
# ----------------------------------------------------------------------------------------------------------------------
app = Flask(__name__)
payments = {}
# ----------------------------------------------------------------------------------------------------------------------
@app.route('/payments/validate', methods=['POST'])
def validate_payment():
    data = request.json

    # Фиктивно что-то делаем, но в реальном проекте, конечно же была бы проверка платежных данных
    payments[data['order_id']] = {'amount': data['amount'], 'status': 'reserved'}

    # Поэтому отдаём клиенту 200-ку
    return jsonify({'status': 'Payment reserved'}), 200
# ----------------------------------------------------------------------------------------------------------------------
@app.route('/payments/cancel', methods=['POST'])
def cancel_payment():
    data = request.json

    # Если нашли такой заказ - удаляем его из памяти
    if data['order_id'] in payments:
        payments[data['order_id']]['status'] = 'cancelled'

    return jsonify({'status': 'Payment cancelled'}), 200
# ----------------------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
# ----------------------------------------------------------------------------------------------------------------------
