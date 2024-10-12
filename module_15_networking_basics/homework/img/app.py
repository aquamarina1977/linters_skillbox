from flask import Flask, jsonify, request

app = Flask(__name__)

rooms = []
bookings = []


@app.route('/room', methods=['GET'])
def get_rooms():
    available_rooms = [room for room in rooms if room['roomId'] not in [b['roomId'] for b in bookings]]
    return jsonify({"rooms": available_rooms})


@app.route('/add-room', methods=['POST'])
def add_room():
    new_room = request.get_json()
    new_room['roomId'] = len(rooms) + 1
    rooms.append(new_room)
    return jsonify({"rooms": rooms})


@app.route('/booking', methods=['POST'])
def book_room():
    booking_request = request.get_json()
    room_id = booking_request['roomId']

    if any(b['roomId'] == room_id for b in bookings):
        return 'Conflict', 409

    bookings.append(booking_request)
    return 'Success', 200


if __name__ == '__main__':
    app.run(debug=True)
