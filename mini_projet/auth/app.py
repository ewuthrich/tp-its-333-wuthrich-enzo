from flask import Flask, request, jsonify
import jwt
import datetime

app = Flask(__name__)
SECRET_KEY = "supersecret"  # change en production
from functools import wraps
from flask import request, jsonify
import jwt

SECRET_KEY = "supersecret"  # doit être le même que dans auth-service

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            if auth_header.startswith("Bearer "):
                token = auth_header[7:]  # enlève "Bearer "
        if not token:
            return jsonify({'message': 'Token is missing'}), 401
        try:
            jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Invalid token'}), 401
        return f(*args, **kwargs)
    return decorated

# Login pour obtenir le token
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    if not data or data.get('username') != 'admin' or data.get('password') != 'password':
        return jsonify({'error': 'Invalid credentials'}), 401

    token = jwt.encode(
        {'user': 'admin', 'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)},
        SECRET_KEY,
        algorithm='HS256'
    )
    return jsonify({'token': token})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
