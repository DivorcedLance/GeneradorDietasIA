import google.generativeai as genai
import os
from dotenv import load_dotenv

class GeminiAPI:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.initialize()
        return cls._instance

    def initialize(self):
        if not hasattr(self, 'initialized'):
            load_dotenv()
            key = os.getenv('API_KEY')
            if not key:
                raise ValueError("API Key está faltando en la configuración.")
            genai.configure(api_key=key)
            self.initialized = True

    def generate_diet(self, prompt):
        model = genai.GenerativeModel('gemini-1.5-flash-latest')
        try:
            response = model.generate_content(prompt,
                                              generation_config=genai.types.GenerationConfig(
                                                  candidate_count=1,
                                                  temperature=0.7,
                                              ))
            return response.text if hasattr(response, 'text') else str(response)
        except Exception as e:
            return f"Error en la generación de la dieta: {str(e)}"