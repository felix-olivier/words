from flask import Flask, jsonify

app = Flask(__name__)

stub = {
    "words": [{
        "word": "impeachment",
        "definitions": ["Amerikaans recht: <br />het in staat van beschuldiging stellen, niet het afzetten, van een overheidsfunctionaris."]
    }, {
        "word": "halal",
        "definitions": ["Halal (Arabisch: حَلاَلْ: rein, toegestaan) is een islamitische term waarmee wordt aangegeven wat voor moslims toegestaan is.", "Halal staat voor alles wat door de Koran als goed en rein kan worden gezien."]
    }]
}

@app.route('/', methods=['GET'])
def get_tasks():
    return stub # jsonify({'words': words})

if __name__ == '__main__':
    app.run(host='0.0.0.0')
