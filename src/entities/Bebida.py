from producto import Producto


class Bebida(Producto):
    """Clase que representa las bebidas del menú."""

    lista_de_bebidas = []

    def __init__(self, nombre: str, precio: int, marca: str, tamano: str) -> None:
        super().__init__(nombre, precio)
        self.marca = marca
        self.tamano = tamano

    @classmethod
    def mostrar_bebidas(cls) -> None:
        """Muestra las bebidas disponibles."""
        print("Bebidas del menú:")

        for bebida in cls.lista_de_bebidas:
            print(
                f"Bebida: {bebida.nombre} | "
                f"Marca: {bebida.marca} | "
                f"Tamaño: {bebida.tamano} | "
                f"Valor: {bebida.precio}"
            )


Bebida.lista_de_bebidas = [
    Bebida("Coca Cola", 4000, "Coca Cola", "350 ml"),
    Bebida("Pepsi", 4000, "Pepsi", "350 ml"),
    Bebida("Jugo Hit", 3000, "Hit", "500 ml"),
    Bebida("Agua", 2000, "Cristal", "600 ml"),
]
