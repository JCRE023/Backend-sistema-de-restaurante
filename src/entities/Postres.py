class Postres:
    def __init__(self, nombre: str, precio: int):
        self.nombre = nombre
        self.precio = precio

    def mostrar(self):
        print(f"El nombre del postre es{self.nombre} y el precio es: {self.precio}")
