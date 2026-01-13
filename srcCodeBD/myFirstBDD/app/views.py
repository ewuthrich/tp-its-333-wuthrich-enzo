

#conn = sqlite3.connect ( 'database.db' )

#print ("Base de données ouverte avec succès")
#conn.execute ( 'CREATE TABLE etudiants (nom TEXT, addr TEXT, pin TEXT)' )
#print ("Table créée avec succès")
#conn.close ()
import sqlite3
from flask import Flask, request, render_template
 
app = Flask(__name__)

conn = sqlite3.connect ( 'database.db' )
print ("Base de données ouverte avec succès")
conn.execute ( 'CREATE TABLE IF NOT EXISTS etudiants (nom TEXT, addr TEXT, pin TEXT)' )
print ("Table créée avec succès")
conn.close ()

@app.route("/new", methods=["POST"])
def add_student():
    nom = request.form['nom']
    addr = request.form['addr']
    pin = request.form['pin']

    with sqlite3.connect( "database.db") as con:
        cur = con.cursor()
        cur.execute(
        "INSERT INTO etudiants (nom,addr,pin) VALUES (?,?,?)", ("{nom}","{adrr}","{pin}"))
        con.commit()

    return f"Etudiant {nom} ajouté" 

if __name__ == "__main__":
    app.run(debug=True)
