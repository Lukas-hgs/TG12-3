import json
import requests


URL = "http://localhost:12345/Spieler"

spieler_liste = []
# Beispiel-Daten

spieler_daten = {
    "name": str (input("Name: ")),
    "jahrgang": int (input("Jahrgang: ")),
    "stearke": int (input("Stärke (1-10): ")),
    "torschuss": int (input("Torschuss (1-10): ")),
    "motivation": int (input("Motivation (1-10): "))
}




response = requests.post(URL, json=spieler_daten)
print("Statuscode:", response.status_code)

if response.status_code == 201:
    print("✅ Spieler erfolgreich erstellt:")
    print(json.dumps(response.json(), indent=4, ensure_ascii=False))
else:
    print("❌ Fehler bei der Erstellung:")
    print(json.dumps(response.json(), indent=4, ensure_ascii=False))
    

