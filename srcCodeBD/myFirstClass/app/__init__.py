from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_swagger_ui import get_swaggerui_blueprint

app = Flask(__name__)

# ---------------- CONFIG ----------------
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ecole.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
SECRET_KEY = "ma_cle_secrete"

db = SQLAlchemy(app)

# ---------------- SWAGGER ----------------
SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'

swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={'app_name': "Gestion Étudiants API"}
)

app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

# ⚠ IMPORTANT : importer views et models À LA FIN
from app import views, models
