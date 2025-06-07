import pickle

class Persistencia:
    @staticmethod
    def guardar(objeto, archivo):
        """
        Guarda un objeto en un archivo usando pickle.
        """
        try:
            with open(archivo, 'wb') as f:
                pickle.dump(objeto, f)
        except Exception as e:
            print(f"Error al guardar en {archivo}: {e}")

    @staticmethod
    def cargar(archivo):
        """
        Carga un objeto desde un archivo usando pickle.
        """
        try:
            with open(archivo, 'rb') as f:
                return pickle.load(f)
        except Exception as e:
            print(f"Error al cargar desde {archivo}: {e}")
            return None