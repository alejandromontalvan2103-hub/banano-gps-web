from flask import Flask, jsonify, render_template
import pymysql
import os

app = Flask(__name__)

# Configuración de conexión a MySQL
config_db = {
    "host": os.environ.get("DB_HOST"),
    "user": os.environ.get("DB_USER"),
    "password": os.environ.get("DB_PASSWORD"),
    "port": int(os.environ.get("DB_PORT")),
    "database": os.environ.get("DB_NAME")
}

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

# Devuelve solo el último punto
@app.route("/api/ubicacion", methods=["GET"])
def obtener_ubicacion():
    try:
        conexion = get_connection()

        with conexion.cursor() as cursor:
            cursor.execute("""
                SELECT id, latitud, longitud, fecha
                FROM historial_gps
                ORDER BY id DESC
                LIMIT 1
            """)
            fila = cursor.fetchone()

        conexion.close()

        if not fila:
            return jsonify({
                "vehiculo": "SIN-DATOS",
                "latitud": -5.194,
                "longitud": -80.632,
                "velocidad": 0,
                "hora": "Sin datos"
            })

        return jsonify({
            "vehiculo": "BAN-01",
            "latitud": fila["latitud"],
            "longitud": fila["longitud"],
            "velocidad": 0,
            "hora": str(fila["fecha"])
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Devuelve todos los puntos para dibujar ruta/polígono
@app.route("/api/historial", methods=["GET"])
def obtener_historial():
    try:
        conexion = get_connection()

        with conexion.cursor() as cursor:
            cursor.execute("""
                SELECT id, latitud, longitud, fecha
                FROM historial_gps
                ORDER BY id ASC
            """)
            filas = cursor.fetchall()

        conexion.close()

        return jsonify(filas)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)