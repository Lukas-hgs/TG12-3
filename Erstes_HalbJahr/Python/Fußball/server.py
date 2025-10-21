from flask import Flask, request, jsonify
from pydantic import BaseModel, Field, field_validator, ValidationError
from model import Spieler 

spieler_Liste=[]

def attribute():
  return f"""
    Method: {request.method}
    Headers: {request.headers}
    Args: {request.args}
    Form: {request.form}
    Data: {request.data}
    Cookies: {request.cookies}
    Path: {request.path}
    URL: {request.url}
    Remote Address: {request.remote_addr}
    """
app = Flask(__name__)

# Route für die Hauptseite
@app.route('/')
def home():
   response_attribut = attribute()
   return jsonify({"attribut": response_attribut})


@app.route('/Profil')
def gym():
   return "<html><body><h1>Eray hat schwache Arme.</h1></body></html>"

# Route zum Empfangen von Nachrichten
@app.route('/message', methods=['POST'])
def handle_message():
    data = request.json
    message = data.get('message', '')
    print(f"Empfangen: {message}")
    print(attribute())
    response_message = f"Echo: {message}"
    return jsonify({"response": response_message})


  
@app.route("/Spieler", methods=["POST"])
def handle_Spieler():
    """Erstellt einen neuen Spieler aus JSON-Daten und prüft es mit Pydantic."""
    try:
        data = request.get_json()
        spieler = Spieler(**data)
        spieler_Liste.append(spieler.model_dump())
        return jsonify({
            "status": "ok👍",
            "message": "Spieler erfolgreich erstellt🤝",
            "Spieler": spieler.model_dump()
        }), 201
    except ValidationError as e:
        return jsonify({
            "status": "error",
            "message": "Validierung fehlgeschlagen",
            "details": e.errors()
        }), 400
    
@app.route('/Test')
def test():
    daten = ""
    for spieler in spieler_Liste:
        daten2 = (f"{daten2}<br> {spieler}")
    print(daten2)
    return(f"{daten2}")
 
    

    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=12345)  # Server starten
