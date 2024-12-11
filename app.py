from flask import Flask, jsonify, request, send_from_directory
from core.utils import calcular_imc
from core.models import DietaGenerator
import json
import os

# Crear la aplicación Flask
app = Flask(__name__, static_folder="static", static_url_path="")

# Instancia del generador de dietas
dieta_generator = DietaGenerator()

@app.route("/")
def serve_static_index():
    """
    Servir el archivo estático index.html desde la carpeta 'static'
    cuando el usuario accede a la raíz.
    """
    return send_from_directory(app.static_folder, "index.html")

@app.route("/api/generar_dieta", methods=["POST"])
def generar_dieta():
    """
    Endpoint para generar una dieta basada en los parámetros enviados.
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No se proporcionaron datos"}), 400

        peso = data.get("peso")
        altura = data.get("altura")
        sexo = data.get("sexo")
        preferencias = data.get("preferencias")

        if not all([peso, altura, sexo, preferencias]):
            return jsonify({"error": "Faltan campos obligatorios"}), 400

        # Calcular el IMC
        imc = calcular_imc(peso, altura)

        # Generar dieta con base en el IMC
        dieta_raw = dieta_generator.generar_dieta(imc, sexo, preferencias)

        # Asegurar conversión segura desde JSON
        if isinstance(dieta_raw, str):
            dieta = json.loads(dieta_raw)
        else:
            dieta = dieta_raw

        return jsonify(dieta), 200
    except Exception as e:
        return jsonify({"error": f"Error al generar la dieta: {str(e)}"}), 500

if __name__ == "__main__":
    # Para desarrollo local, usa el servidor interno de Flask
    app.run(debug=True, host="0.0.0.0", port=8000)
