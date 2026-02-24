from producto import Producto


class Bebida(Producto):

    lista_de_bebidas = []

    def __init__(self, nombre: str, precio: int, marca: str, tamano: str):
        super().__init__(nombre, precio)
        self.marca = marca
        self.tamano = tamano

    @classmethod
    def mostrar_bebidas(cls):
        """
        Muestra las bebidas disponibles
        """
        print("Bebidas del menu:")
        for bebida in cls.lista_de_bebidas:
            print(
                f"Bebida: {bebida.nombre} | Marca: {bebida.marca} | Tamaño: {bebida.tamano} | Valor: {bebida.precio}"
            )


Bebida.lista_de_bebidas = [
    Bebida("Coca Cola", 4000, "Coca Cola", "350ml"),
    Bebida("Pepsi", 4000, "Pepsi", "350ml"),
    Bebida("Jugo Hit", 3000, "Hit", "500ml"),
    Bebida("Agua", 2000, "Cristal", "600ml"),
]
