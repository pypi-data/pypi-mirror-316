import requests
import pandas as pd

class BotConnector:
    def __init__(self, token):
        """
        Inicializa el cliente para interactuar con la API.
        :param token: Token único del bot asignado.
        """
        self.base_url = "https://concurso-trading.onrender.com"
        self.token = token

    def save_operation(self, activo, cantidad):
        """
        Guarda una operación en la base de datos y maneja errores reportados por el servidor.
        """
        try:
            response = requests.post(
                f"{self.base_url}/save-operation/",
                json={"activo": activo, "cantidad": cantidad},
                headers={"token": self.token}
            )
            print(cantidad)
            if response.status_code == 200:
                result = response.json()
                print(result.get("message", "Operación guardada exitosamente."))
            else:
                error_detail = response.json().get("detail", "Error desconocido.")
                print(f"Error al guardar operación: {error_detail}")
        except requests.RequestException as e:
            print(f"Error de conexión: {str(e)}")

    def get_operations(self):
        """
        Obtiene las operaciones realizadas por el bot.
        :return: DataFrame con las operaciones realizadas o un mensaje de error.
        """
        try:
            # Realiza la solicitud GET al servidor
            response = requests.get(
                f"{self.base_url}/get-operations/",
                headers={"token": self.token}
            )
            # Verificar si el servidor respondió
            if response.status_code == 200:
                try:
                    operations = response.json().get("operations", [])
                    print("Operaciones obtenidas exitosamente.")
                    return pd.DataFrame(operations)
                except ValueError:
                    print("Error: Respuesta del servidor no es JSON válida.")
                    print(f"Cuerpo de la respuesta: {response.text}")
                    return pd.DataFrame()  # Devuelve un DataFrame vacío en caso de error

            # Manejar errores devueltos por el servidor
            error_detail = response.json().get("detail", "Error desconocido.")
            print(f"Error al obtener operaciones: {error_detail}")
            return pd.DataFrame()  # Devuelve un DataFrame vacío en caso de error

        except requests.RequestException as e:
            # Manejar errores de conexión o solicitud
            print(f"Error de conexión: {str(e)}")
            return pd.DataFrame()  # Devuelve un DataFrame vacío en caso de error


