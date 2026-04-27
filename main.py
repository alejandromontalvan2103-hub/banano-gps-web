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

CONTORNO_MAX_ID = 84

def get_connection():
    return pymysql.connect(
        host=config_db["host"],
        user=config_db["user"],
        password=config_db["password"],
        port=config_db["port"],
        database=config_db["database"],
        cursorclass=pymysql.cursors.DictCursor,
        connect_timeout=5,
        read_timeout=5,
        write_timeout=5
    )

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/api/testdb")
def testdb():
    conexion = None
    try:
        conexion = get_connection()
        return jsonify({"conexion": "OK"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        if conexion:
            conexion.close()

@app.route("/api/contorno")
def contorno():
    conexion = None
    try:
        conexion = get_connection()

        with conexion.cursor() as cursor:
            cursor.execute("""
                SELECT latitud, longitud
                FROM historial_gps
                WHERE id <= %s
                ORDER BY id ASC
            """, (CONTORNO_MAX_ID,))
            datos = cursor.fetchall()

        return jsonify(datos), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        if conexion:
            conexion.close()

@app.route("/api/ubicacion")
def ubicacion():
    conexion = None
    try:
        conexion = get_connection()

        with conexion.cursor() as cursor:
            cursor.execute("""
                SELECT latitud, longitud, fecha
                FROM historial_gps
                ORDER BY id DESC
                LIMIT 1
            """)
            dato = cursor.fetchone()

        if not dato:
            return jsonify({
                "vehiculo": "SIN-DATOS",
                "latitud": -5.19,
                "longitud": -80.63,
                "velocidad": 0,
                "hora": "sin datos"
            }), 200

        return jsonify({
            "vehiculo": "BAN-01",
            "latitud": dato["latitud"],
            "longitud": dato["longitud"],
            "velocidad": 0,
            "hora": str(dato["fecha"])
        }), 200

    except Exception as e:
        return jsonify({
            "error": str(e),
            "vehiculo": "ERROR",
            "latitud": -5.19,
            "longitud": -80.63,
            "velocidad": 0,
            "hora": "Error de conexión"
        }), 500

    finally:
        if conexion:
            conexion.close()

@app.route("/api/gps", methods=["POST"])
def gps():
    conexion = None
    try:
        data = request.get_json()

        if not data:
            return jsonify({"error": "No se recibió JSON"}), 400

        latitud = float(data["latitud"])
        longitud = float(data["longitud"])

        conexion = get_connection()

        with conexion.cursor() as cursor:
            cursor.execute("""
                INSERT INTO historial_gps (latitud, longitud, fecha)
                VALUES (%s, %s, NOW())
            """, (latitud, longitud))

        conexion.commit()

        return jsonify({
            "ok": True,
            "mensaje": "Punto GPS guardado correctamente"
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        if conexion:
            conexion.close()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)