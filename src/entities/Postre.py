from src.entities.producto import Producto


class Postre(Producto):

    lista_de_postres = []

    def __init__(self, nombre: str, precio: int, sabor: str):
        super().__init__(nombre, precio)
        self.sabor = sabor

    @classmethod
    def mostrar_postres(cls) -> str:
        """
        Muestra los postres disponibles
        """
        print("Postres del menu:")
        for postre in cls.lista_de_postres:
            print(
                f"Postre: {postre.nombre} | Sabor: {postre.sabor} | Valor: {postre.precio}"
            )


Postre.lista_de_postres = [
    Postre("trufas", 3000, "chocolate"),
    Postre("brownie", 5000, "chocolate"),
    Postre("copa de fresa", 12000, "fresa"),
    Postre("helado 1 bola", 4000, "vainilla"),
]
