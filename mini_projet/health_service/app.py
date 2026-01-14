from flask import Flask, request, jsonify, abort
import json
import requests
from functools import wraps
from flask import request, jsonify
import jwt
from functools import wraps
from flask import request, jsonify

SECRET_KEY = "supersecret"  # doit être le même que auth-service

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            if auth_header.startswith("Bearer "):
                token = auth_header[7:]
        if not token:
            return jsonify({'message': 'Token is missing'}), 401
        try:
            # PyJWT 2.x
            payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Invalid token'}), 401
        return f(*args, **kwargs)
    return decorated



app = Flask(__name__)
DATA_FILE = 'data.json'

#  Utiliser le nom du service Docker Personne
PERSON_SERVICE_URL = 'http://personne_service:5001/persons'

# Charger les données
try:
    with open(DATA_FILE) as f:
        health_data = json.load(f)
except:
    health_data = {}

def save_data():
    with open(DATA_FILE, 'w') as f:
        json.dump(health_data, f, indent=2)

def check_person_exists(person_id):
    try:
        r = requests.get(f"{PERSON_SERVICE_URL}/{person_id}")
        return r.status_code == 200
    except requests.exceptions.RequestException as e:
        print(f"Erreur lors de la vérification de la personne: {e}")
        return False

@app.route('/health/<int:person_id>', methods=['GET'])
def get_health(person_id):
    if not check_person_exists(person_id):
        abort(404)
    return jsonify(health_data.get(str(person_id), {}))

@app.route('/health/<int:person_id>', methods=['POST'])
@token_required
def add_health(person_id):
    if not check_person_exists(person_id):
        abort(404)
    data = request.json
    health_data[str(person_id)] = data
    save_data()
    return jsonify(data), 201

@app.route('/health/<int:person_id>', methods=['PUT'])
def update_health(person_id):
    if not check_person_exists(person_id):
        abort(404)
    if str(person_id) not in health_data:
        abort(404)
    data = request.json
    health_data[str(person_id)].update(data)
    save_data()
    return jsonify(health_data[str(person_id)])

@app.route('/health/<int:person_id>', methods=['DELETE'])
def delete_health(person_id):
    if not check_person_exists(person_id):
        abort(404)
    if str(person_id) in health_data:
        del health_data[str(person_id)]
        save_data()
    return '', 204

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)
