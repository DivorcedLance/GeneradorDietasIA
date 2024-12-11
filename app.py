from flask import Flask, jsonify, request, send_from_directory
from core.utils import calcular_imc
from core.models import DietaGenerator
import json
import os

app = Flask(__name__, static_folder="static", static_url_path="")

dieta_generator = DietaGenerator()

@app.route("/")
def serve_static_index():
    return send_from_directory(app.static_folder, "index.html")

@app.route("/api/generar_dieta", methods=["POST"])
def generar_dieta():
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

        imc = calcular_imc(peso, altura)
        dieta_raw = dieta_generator.generar_dieta(imc, sexo, preferencias)

        if isinstance(dieta_raw, str):
            dieta = json.loads(dieta_raw)
        else:
            dieta = dieta_raw

        return jsonify(dieta), 200
    except Exception as e:
        return jsonify({"error": f"Error al generar la dieta: {str(e)}"}), 500