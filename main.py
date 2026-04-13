from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

# Aquí se guarda la última ubicación recibida
ubicacion_actual = {
    "vehiculo": "BAN-01",
    "latitud": -5.194,
    "longitud": -80.632,
    "velocidad": 0,
    "hora": "Sin datos"
}

@app.route("/")
def home():
    return render_template("index.html")

# Ruta para que la Raspberry mande datos
@app.route("/api/gps", methods=["POST"])
def recibir_gps():
    global ubicacion_actual

    data = request.get_json()

    if not data:
        return jsonify({"error": "No se recibió JSON"}), 400

    try:
        ubicacion_actual["vehiculo"] = data.get("vehiculo", "BAN-01")
        ubicacion_actual["latitud"] = float(data.get("latitud"))
        ubicacion_actual["longitud"] = float(data.get("longitud"))
        ubicacion_actual["velocidad"] = float(data.get("velocidad", 0))
        ubicacion_actual["hora"] = data.get("hora", "Sin hora")

        return jsonify({
            "mensaje": "Ubicación recibida correctamente",
            "data": ubicacion_actual
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Ruta para que la web lea la última ubicación
@app.route("/api/ubicacion", methods=["GET"])
def obtener_ubicacion():
    return jsonify(ubicacion_actual)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)