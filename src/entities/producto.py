class Producto:
    def __init__(self, nombre: str, precio: float):
        self.__nombre = nombre
        self.__precio = precio

    @property
    def nombre(self):
        return self.__nombre

    @nombre.setter
    def nombre(self, nombre: str):
        self.__nombre = nombre.rstrip()

    @property
    def precio(self):
        return self.__precio

    @precio.setter
    def precio(self, precio: float):
        if precio < 0:
            return "¡El precio debe ser mayor a cero!"
        self.__precio = precio
