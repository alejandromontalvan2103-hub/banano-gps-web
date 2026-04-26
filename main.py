from flask import Flask, jsonify, render_template, request
import pymysql
import os

app = Flask(__name__)

config_db = {
    "host": os.environ.get("DB_HOST"),
    "user": os.environ.get("DB_USER"),
    "password": os.environ.get("DB_PASSWORD"),
    "port": int(os.environ.get("DB_PORT")),
    "database": os.environ.get("DB_NAME")
}

# Ajusta según tu contorno
CONTORNO_MAX_ID = 84

def get_connection():
    return pymysql.connect(
        host=config_db["host"],
        user=config_db["user"],
        password=config_db["password"],
        port=config_db["port"],
        database=config_db["database"],
        cursorclass=pymysql.cursors.DictCursor
    )

@app.route("/")
def home():
    return render_template("index.html")

# 🔴 CONTORNO FIJO
@app.route("/api/contorno")
def contorno():
    conexion = get_connection()
    with conexion.cursor() as cursor:
        cursor.execute("""
            SELECT latitud, longitud 
            FROM historial_gps
            WHERE id <= %s
            ORDER BY id ASC
        """, (CONTORNO_MAX_ID,))
        datos = cursor.fetchall()
    conexion.close()
    return jsonify(datos)

# 📍 GPS ACTUAL
@app.route("/api/ubicacion")
def ubicacion():
    conexion = get_connection()
    with conexion.cursor() as cursor:
        cursor.execute("""
            SELECT latitud, longitud, fecha
            FROM historial_gps
            ORDER BY id DESC LIMIT 1
        """)
        dato = cursor.fetchone()
    conexion.close()

    if not dato:
        return jsonify({"latitud": -5.19, "longitud": -80.63, "hora": "sin datos"})

    return jsonify({
        "latitud": dato["latitud"],
        "longitud": dato["longitud"],
        "hora": str(dato["fecha"])
    })

# 📥 GUARDAR DATOS DE RASPBERRY
@app.route("/api/gps", methods=["POST"])
def gps():
    data = request.get_json()

    conexion = get_connection()
    with conexion.cursor() as cursor:
        cursor.execute("""
            INSERT INTO historial_gps (latitud, longitud, fecha)
            VALUES (%s, %s, NOW())
        """, (data["latitud"], data["longitud"]))
    conexion.commit()
    conexion.close()

    return jsonify({"ok": True})

if __name__ == "__main__":
    app.run()