class Bebidas:
    def __init__(self, marca: str, tamaño: str):
        self.precio = 1000
        self.marca = marca
        self.tamaño = tamaño

    def imprimir(self):
        print(f"La marca de la bebida es {self.marca} y el tamaño es: {self.tamaño}")
