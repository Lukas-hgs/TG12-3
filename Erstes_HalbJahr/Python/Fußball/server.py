from flask import Flask, request, jsonify
from flask_cors import CORS
from pydantic import ValidationError
from model import Spieler
import json
import os

app = Flask(__name__)
CORS(app)

dateiname = "spieler.json"
if os.path.exists(dateiname):
    try:
        with open(dateiname, "r", encoding="utf-8") as f:
            daten = json.load(f)
        spieler_liste = [Spieler(**s) for s in daten]
        print("📂 Geladene Spieler:")
        for s in spieler_liste:
            print(s)
    except Exception as e:
        print("Fehler beim Laden der Datei:", e)
        spieler_liste = []
else:
    print(f"⚠️ Datei '{dateiname}' wurde nicht gefunden. Leere Spielerliste wird erstellt.")
    spieler_liste = []

def save_spieler_liste():
    try:
        with open(dateiname, "w", encoding="utf-8") as f:
            json.dump([s.model_dump() for s in spieler_liste], f, ensure_ascii=False, indent=4)
        print("✅ Spieler wurden in '{}' gespeichert.".format(dateiname))
    except Exception as e:
        print("Fehler beim Speichern der Spielerliste:", e)
def attribute():
    return f"""
    Method: {request.method}
    Headers: {dict(request.headers)}
    Args: {request.args}
    Form: {request.form}
    Data: {request.data}
    Cookies: {request.cookies}
    Path: {request.path}
    URL: {request.url}
    Remote Address: {request.remote_addr}
    """

@app.route('/')
def home():
    response_attribut = attribute()
    return jsonify({"attribut": response_attribut})

@app.route('/Profil')
def gym():
    return "<html><body><h1>Eray hat schwache Arme.</h1></body></html>"

@app.route('/message', methods=['POST'])
def handle_message():
    data = request.json or {}
    message = data.get('message', '')
    print(f"Empfangen: {message}")
    print(attribute())
    response_message = f"Echo: {message}"
    return jsonify({"response": response_message})

# Datei, in der die Spieler gespeichert werden
dateiname = "spieler.json"

# Beim Start vorhandene Spieler laden


@app.route("/Spieler", methods=["POST"])
def handle_Spieler():
    """Erstellt einen neuen Spieler aus JSON-Daten und prüft es mit Pydantic."""
    try:
        data = request.get_json() or {}
        spieler = Spieler(**data)
        spieler_liste.append(spieler)
        with open("spieler.json", "w", encoding="utf-8") as f:
            json.dump([s.model_dump() for s in spieler_liste], f, ensure_ascii=False, indent=4)
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
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": "Interner Serverfehler",
            "details": str(e)
        }), 500
    
@app.route('/sp')
def Test_Ausgabe():
    daten = ""
    for s in spieler_liste:
        daten = (f"{daten} <br> {s}")
    print (daten)
    return (f"{daten}")


 

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
