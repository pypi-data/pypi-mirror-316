import requests
import pandas as pd

class CerebroClient:
    def __init__(self, token):
        """
        Inicializa el cliente para interactuar con la API.
        :param token: Token único del bot asignado.
        """
        self.base_url = "https://concurso-trading.onrender.com"  # URL base oculta al usuario
        self.token = token

    def save_operation(self, activo, cantidad):
        """
        Guarda una operación en la base de datos.
        :param activo: Símbolo del activo (por ejemplo, 'AAPL', 'PEP').
        :param cantidad: Cantidad de la operación.
        """
        response = requests.post(
            f"{self.base_url}/save-operation/",
            json={"token": self.token, "activo": activo, "cantidad": cantidad}
        )
        if response.status_code == 200:
            print("Operación guardada exitosamente.")
        else:
            print(f"Error al guardar la operación: {response.json()}")

    def get_operations(self):
        """
        Obtiene las operaciones realizadas por el bot.
        :return: DataFrame con las operaciones realizadas.
        """
        response = requests.get(f"{self.base_url}/get-operations/", params={"token": self.token})
        if response.status_code == 200:
            operations = response.json()
            return pd.DataFrame(operations)
        else:
            print(f"Error al obtener operaciones: {response.json()}")
            return pd.DataFrame()
