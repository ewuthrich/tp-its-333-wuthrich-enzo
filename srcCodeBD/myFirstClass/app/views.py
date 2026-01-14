from flask import request, jsonify
import jwt
import datetime
from functools import wraps

from app import app, db, SECRET_KEY
from app.models import Groupe, Etudiant

# ---------------- CREATION BASE ----------------
with app.app_context():
    db.create_all()
    if not Groupe.query.filter_by(nom="ITS2").first():
        its2 = Groupe(nom="ITS2")
        e1 = Etudiant(nom="Zozo", groupe=its2)
        e2 = Etudiant(nom="Dodo", groupe=its2)
        e3 = Etudiant(nom="Coco", groupe=its2)
        db.session.add(its2)
        db.session.add_all([e1, e2, e3])
        db.session.commit()

# ---------------- JWT ----------------
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        if not token:
            return jsonify({'message': 'Token manquant !'}), 401
        try:
            jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        except:
            return jsonify({'message': 'Token invalide !'}), 401
        return f(*args, **kwargs)
    return decorated

@app.route('/login', methods=['POST'])
def login():
    auth = request.json
    if auth and auth.get('username') == "admin" and auth.get('password') == "1234":
        token = jwt.encode(
            {
                'user': auth['username'],
                'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
            },
            SECRET_KEY,
            algorithm="HS256"
        )
        return jsonify({'token': token})
    return jsonify({'message': 'Login échoué !'}), 401

# ---------------- ROUTES API ----------------
@app.route('/')
def index():
    groupe = Groupe.query.filter_by(nom="ITS2").first()
    return {
        "groupe": groupe.nom,
        "etudiants": [e.nom for e in groupe.etudiants]
    }

@app.route('/new', methods=['POST'])
@token_required
def add_etudiant():
    data = request.json
    nom = data.get('nom')
    if not nom:
        return jsonify({"message": "Nom manquant"}), 400
    its2 = Groupe.query.filter_by(nom="ITS2").first()
    e = Etudiant(nom=nom, groupe=its2)
    db.session.add(e)
    db.session.commit()
    return jsonify({"message": f"Étudiant {nom} ajouté ✅"})

@app.route('/etudiants')
def liste_etudiants():
    groupe = Groupe.query.filter_by(nom="ITS2").first()
    return {
        "groupe": groupe.nom,
        "etudiants": [e.nom for e in groupe.etudiants]
    }
