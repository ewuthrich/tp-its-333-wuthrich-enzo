from flask import Flask
from ClassEtudiant import db, Groupe, Etudiant  # ✅ ici seulement

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///alchimie.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()

    if Groupe.query.filter_by(group_nom="ITS2").first():
        e1 = Etudiant(nom="Jojo", groupe= group_nom, pin=3658)
        e2 = Etudiant(nom="Dodo", groupe=group_nom, pin=2589)
        e3 = Etudiant(nom="Bobo", groupe=group_nom, pin=5476)
        db.session.add_all([e1, e2, e3])
        db.session.commit()

@app.route("/test")
def test():
    groupe = Groupe.query.filter_by(group_nom="ITS2").first()
    return {
        "groupe": groupe.group_nom,
        "etudiant": [e.nom for e in groupe.etudiant]
    }

if __name__ == "__main__":
    app.run(debug=True)