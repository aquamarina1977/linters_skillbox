from flask import Flask, request, jsonify
from task_2_db_initialization import db
from task_2_models import Client, Parking, ClientParking
import os
from datetime import datetime


def create_app(test_config=None):
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY='dev',
        SQLALCHEMY_DATABASE_URI=os.getenv('DATABASE_URL', 'sqlite:///parking.db'),
        SQLALCHEMY_TRACK_MODIFICATIONS=False
    )

    if test_config:
        app.config.update(test_config)

    db.init_app(app)

    with app.app_context():
        db.create_all()


    @app.route('/clients', methods=['GET'])
    def get_clients():
        clients = Client.query.all()
        return jsonify([{'id': c.id, 'name': c.name, 'surname': c.surname, 'credit_card': c.credit_card,
                         'car_number': c.car_number} for c in clients])

    @app.route('/clients/<int:client_id>', methods=['GET'])
    def get_client(client_id):
        client = Client.query.get_or_404(client_id)
        return jsonify(
            {'id': client.id, 'name': client.name, 'surname': client.surname, 'credit_card': client.credit_card,
             'car_number': client.car_number})


    @app.route('/clients', methods=['POST'])
    def create_client():
        data = request.json
        client = Client(name=data['name'], surname=data['surname'], credit_card=data.get('credit_card'),
                        car_number=data.get('car_number'))
        db.session.add(client)
        db.session.commit()
        return jsonify({'message': 'Client created', 'id': client.id}), 201

    @app.route('/parkings', methods=['POST'])
    def create_parking():
        data = request.json
        parking = Parking(address=data['address'], opened=data.get('opened', True), count_places=data['count_places'],
                          count_available_places=data['count_places'])
        db.session.add(parking)
        db.session.commit()
        return jsonify({'message': 'Parking created', 'id': parking.id}), 201


    @app.route('/client_parkings', methods=['POST'])
    def park_car():
        data = request.json
        client = Client.query.get(data['client_id'])
        parking = Parking.query.get(data['parking_id'])
        if not client or not parking:
            return jsonify({'error': 'Invalid client or parking ID'}), 400
        if not parking.opened or parking.count_available_places <= 0:
            return jsonify({'error': 'Parking is closed or full'}), 400
        log = ClientParking(client_id=client.id, parking_id=parking.id, time_in=datetime.utcnow())
        parking.count_available_places -= 1
        db.session.add(log)
        db.session.commit()
        return jsonify({'message': 'Car parked'}), 201


    @app.route('/client_parkings', methods=['DELETE'])
    def leave_parking():
        data = request.json
        client = Client.query.get(data['client_id'])
        parking = Parking.query.get(data['parking_id'])
        if not client or not parking:
            return jsonify({'error': 'Invalid client or parking ID'}), 400
        log = ClientParking.query.filter_by(client_id=client.id, parking_id=parking.id, time_out=None).first()
        if not log:
            return jsonify({'error': 'No active parking session'}), 400
        if not client.credit_card:
            return jsonify({'error': 'Client has no credit card attached'}), 400
        log.time_out = datetime.utcnow()
        parking.count_available_places += 1
        db.session.commit()
        return jsonify({'message': 'Car left parking'}), 200


    return app

