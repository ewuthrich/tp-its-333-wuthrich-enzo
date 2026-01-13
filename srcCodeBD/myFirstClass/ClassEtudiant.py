from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Etudiant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(80), unique=True, nullable=False)
    group_id = db.Column(db.Integer, db.ForeignKey('groupe.group_id'))
    pin = db.Column(db.String(20), unique=True, nullable=False)
    def __repr__(self):
        return f"<Etudiant {self.nom}>"

class Groupe(db.Model):
    group_id = db.Column(db.Integer, primary_key=True)
    group_nom = db.Column(db.String(80), unique=True, nullable=False)
    etudiant = db.relationship('Etudiant', backref= 'groupe', lazy=True)
    def __repr__(self):
            return f"<Groupe {self.nom}>"




