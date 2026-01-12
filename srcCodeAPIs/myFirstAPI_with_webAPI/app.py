from flask import Flask, jsonify, request

app = Flask(__name__)

## EXO1: API GET: renvoyer un helloworld - API end point name: "api/salutation"
@app.route('/api/salutation', methods=['GET'])
def salutation():
    return jsonify(message = "Hello World")

## EXO2: API POST: renvoyer un nom fourni en parametre - API end point name: "api/utilisateurs"

@app.route('/api/utilisateurs', methods=['GET', 'POST'])
def utilisateurs():
    data = request.get_json()

    if not data or 'nom' not in data:
        return jsonify({"error": "Le champ 'nom' est requis"}), 400
        
    nom =data['nom']
    return jsonify(message=f"Utilisateur {nom} ajoute avec succes :)"), 201 #{"nom": data['nom']})
    



# to be tested with curl: 
# >> curl -i -X GET http://localhost:5000/api/salutation
# >> curl -i -X POST -H 'Content-Type: application/json' -d '{"nom": "Bob"}' http://localhost:5000/api/utilisateurs

if __name__ == '__main__':
    app.run(debug=True)