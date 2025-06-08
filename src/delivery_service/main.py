from flask import Flask, jsonify, request
# ----------------------------------------------------------------------------------------------------------------------
app = Flask(__name__)
timeslots = {}
deliveries = {}
# ----------------------------------------------------------------------------------------------------------------------
@app.route('/delivery/reserve', methods=['POST'])
def reserve_delivery():
    data = request.json
    order_id = data['order_id']
    timeslot = data['timeslot']

    # Если такой уже есть - отказываем
    if timeslot in timeslots:
        return jsonify({'error': 'Timeslot already taken'}), 400

    # Формируем
    timeslots[timeslot] = order_id
    deliveries[order_id] = {
        'address': data['address'], # В боевом примере можно сделать проверку адреса по ФИАС
        'timeslot': timeslot,
        'status': 'reserved'
    }

    return jsonify({'status': 'Delivery reserved'}), 200
# ----------------------------------------------------------------------------------------------------------------------
@app.route('/delivery/cancel', methods=['POST'])
def cancel_delivery():

    order_id = request.json['order_id']

    # Если такой есть - удаляем
    if order_id in deliveries:
        timeslot = deliveries[order_id]['timeslot']
        del timeslots[timeslot]
        del deliveries[order_id]

    # Но 200-ку отдаём в любом случае, чтобы не нагружать клиента лишней логикой
    return jsonify({'status': 'Delivery cancelled'}), 200
# ----------------------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)
# ----------------------------------------------------------------------------------------------------------------------
