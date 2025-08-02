from flask import Flask, render_template, request
import firebase_admin
from firebase_admin import credentials, db
import json

app = Flask(__name__)

# Leer las credenciales de Firebase desde el archivo JSON
with open("firebase_config.json", "r") as f:
    cred_dict = json.load(f)

# Inicializar Firebase solo una vez
if not firebase_admin._apps:
    cred = credentials.Certificate(cred_dict)
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://heart-trazabilidad-default-rtdb.firebaseio.com/'
    })

@app.route("/", methods=["GET", "POST"])
def index():
    resultado = None
    if request.method == "POST":
        consecutivo = request.form.get("consecutivo", "").strip()
        if consecutivo:
            ref = db.reference("documentos")
            data = ref.get()
            if data and consecutivo in data:
                registros = data[consecutivo]
                resultado = registros
            else:
                resultado = []
    return render_template("index.html", resultado=resultado)

@app.route("/novedades")
def novedades():
    ref = db.reference("novedades")
    data = ref.get()

    if isinstance(data, list):
        lista_novedades = [n for n in data if n]
    elif isinstance(data, dict):
        lista_novedades = list(data.values())
    else:
        lista_novedades = []

    return render_template("novedades.html", novedades=lista_novedades)

if __name__ == "__main__":
    app.run(debug=True)


