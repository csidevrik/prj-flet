import os
import json

def gradient(name):
    # Obtener la ruta al archivo gradients.json
    json_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'gradients.json')

    with open(json_path, 'r') as file:
        data = json.load(file)
        for paleta in data:
            if paleta['name'] == name:
                return paleta['colors']
        # Si el nombre de la paleta no se encuentra, puedes manejar el caso de error como desees
        return None

# Ejemplo de uso:
# colors = getpaleta("Farhan")
# print(colors)  # Output: ['#9400D3', '#4B0082']
