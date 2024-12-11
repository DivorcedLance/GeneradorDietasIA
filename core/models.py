from core.api import GeminiAPI
import json
import re

class DietaGenerator:
    def __init__(self):
        self.api = GeminiAPI()
        self.prompt_template = (
            """
            Crear una dieta personalizada para una persona con un IMC de {imc}, sexo {sexo}, 
            y preferencias alimenticias {preferencias}. 
            Indique los alimentos sugeridos para desayuno, almuerzo, cena y snacks. 
            Proporcione también un análisis nutricional detallado, 
            incluyendo "calorias", "proteinas", "carbohidratos" y "grasas" por comida.

            La respuesta debe estar en formato **JSON puro**. 
            No incluya texto adicional fuera del JSON. Solo devuelva:
            {{
                "desayuno": "Descripción del desayuno",
                "almuerzo": "Descripción del almuerzo",
                "cena": "Descripción de la cena",
                "snacks": "Descripción de los snacks",
                "analisis_nutricional": {{
                    "calorias": 2000,
                    "proteinas": 80,
                    "carbohidratos": 250,
                    "grasas": 60
                }}
            }}
            
            Asegúrese de que el JSON sea válido y bien estructurado.
            """
        )

    def limpiar_respuesta(self, raw_response):
        """
        Limpia la respuesta eliminando saltos de línea y caracteres no válidos.
        """
        # Quitar backticks si están presentes
        raw_response = re.sub(r"```json|```", "", raw_response)
        # Reemplazar saltos de línea y múltiples espacios
        cleaned_response = re.sub(r"\s+", " ", raw_response.strip())
        return cleaned_response

    def generar_dieta(self, imc, sexo, preferencias):
        prompt = self.prompt_template.format(imc=imc, sexo=sexo, preferencias=preferencias)
        raw_dieta = self.api.generate_diet(prompt)

        if not raw_dieta or not raw_dieta.strip():
            raise ValueError("Error al generar la dieta: La API devolvió una respuesta vacía o nula.")
        
        # Limpieza del JSON devuelto
        raw_dieta = self.limpiar_respuesta(raw_dieta)
        print("Respuesta de DietaGenerator (limpia):", raw_dieta)

        # Intentar convertir la respuesta en JSON
        try:
            dieta = json.loads(raw_dieta)
        except json.JSONDecodeError as e:
            raise ValueError(f"Error al procesar la dieta: Respuesta de API no es JSON válido: {str(e)}")

        # Verificar que el JSON contiene las claves requeridas
        required_keys = ["desayuno", "almuerzo", "cena", "snacks", "analisis_nutricional"]
        if not all(key in dieta for key in required_keys):
            raise ValueError("Error al generar la dieta: La respuesta no contiene todas las claves requeridas.")

        return dieta