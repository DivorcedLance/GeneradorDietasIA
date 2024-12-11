def calcular_imc(peso, altura):
    """Calcula el Índice de Masa Corporal (IMC)."""
    return round(peso / (altura ** 2), 2)

def guardar_dieta(file_path, dieta):
    with open(file_path, 'w') as file:
        file.write(dieta)

def cargar_dieta(file_path):
    with open(file_path, 'r') as file:
        return file.read()