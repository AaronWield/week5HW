from operator import methodcaller
from flask import Blueprint, json, request, jsonify
from car_collection.helpers import token_required
from car_collection.models import Car, db, car_schema, cars_schema

api = Blueprint('api', __name__, url_prefix='/api')

@api.route('/getdata')
def getdata():
    return {'some_value': 52, 'another_value': 'Coding Temple'}
    
@api.route('/cars', methods=['POST'])
@token_required
def create_car(current_user_token):
    name = request.json['name']
    description = request.json['description']
    type = request.json['type']
    color = request.json['color']
    year = request.json['year']
    make = request.json['make']
    model = request.json['model']
    token = current_user_token.token

    print(f'TEST: {current_user_token.token}')
    car = Car(name, description, type, color, year, make, model, user_token = token)

    db.session.add(car)
    db.session.commit()

    response = car_schema.dump(car)
    return jsonify(response)

@api.route('/dcars', methods = ['GET'])
@token_required
def get_cars(current_user_token):
    owner = current_user_token.token
    cars = Car.query.filter_by(user_token = owner).all()
    response = cars_schema.dump(cars)
    return jsonify(response)

@api.route('/cars/<id>', methods = ['GET'])
@token_required
def get_car(current_user_token, id):
    car = Car.query.get(id)
    response = car_schema.dump(car)
    return jsonify(response)

@api.route('/cars/<id>', methods = ['POST', 'PUT'])
@token_required
def update_car(current_user_token, id):
    car = Car.query.get(id)
    print(car)
    if car:
        car.name = request.json['name']
        car.description = request.json['description']
        car.type = request.json['type']
        car.color = request.json['color']
        car.year = request.json['year']
        car.make = request.json['make']
        car.model = request.json['model']
        car.token = current_user_token.token
        db.session.commit()

        response = car_schema.dump(car)
        return jsonify(response)
    else:
        return jsonify({'Error': 'That car does not exist.'})

@api.route('/cars/<id>', methods = ['DELETE'])
@token_required
def delete_car(current_user_token, id):
    car = Car.query.get(id)
    if car:
        db.session.delete(car)
        db.session.commit()
        return jsonify({'Success': f'Car ID #{car.id} has been deleted'})
    else: 
        return jsonify({'Error': 'That car does not exist.'})
