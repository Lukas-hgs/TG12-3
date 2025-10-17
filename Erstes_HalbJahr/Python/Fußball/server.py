from flask import Flask, request, jsonify

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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=12345)  # Server starten

  


 
    

    

