from producto import Producto


class PlatoPrincipal(Producto):

    lista_de_platos_principales = []

    def __init__(self, nombre: str, precio: int, tipo: str):
        super().__init__(nombre, precio)
        self.tipo = tipo

    def mostrar_platos_principales() -> None:
        print("Platos principales del menu:")
        for plato in PlatoPrincipal.lista_de_platos_principales:
            print(
                f"Plato principal: {plato.nombre} | Tipo: {plato.tipo} | Valor: {plato.precio}"
            )


PlatoPrincipal.lista_de_platos_principales = [
    PlatoPrincipal("Lasaña", 45000, "carne"),
    PlatoPrincipal("Lasaña vegetariana", 55000, "vegetariano"),
    PlatoPrincipal("Pollo al horno", 42000, "pollo"),
]
