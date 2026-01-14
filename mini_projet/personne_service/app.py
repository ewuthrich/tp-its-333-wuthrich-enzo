from flask import Flask, request, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from functools import wraps
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
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# ---- modèle Person ----
class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)

# ---- création de la DB dans le contexte ----
with app.app_context():
    db.create_all()

# ---- routes ----
@app.route('/persons', methods=['POST'])
@token_required
def create_person():
    data = request.json
    if not data or 'name' not in data:
        return jsonify({'error': 'Name required'}), 400
    person = Person(name=data['name'])
    db.session.add(person)
    db.session.commit()
    return jsonify({'id': person.id, 'name': person.name}), 201

@app.route('/persons/<int:person_id>', methods=['GET'])
def get_person(person_id):
    person = Person.query.get(person_id)
    if not person:
        abort(404)
    return jsonify({'id': person.id, 'name': person.name})

@app.route('/persons/<int:person_id>', methods=['DELETE'])
@token_required
def delete_person(person_id):
    person = Person.query.get(person_id)
    if not person:
        abort(404)
    db.session.delete(person)
    db.session.commit()
    return '', 204

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug= True)
