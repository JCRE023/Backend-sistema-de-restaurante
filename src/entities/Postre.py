from producto import Producto

lista_de_postres = [
    Producto("trufas", 3000),
    Producto("brownie", 5000),
    Producto("copa de fresa", 12000),
    Producto("helado 1 bola", 4000),
    Producto("helado 2 bolas", 6000),
]


def mostrar_postres() -> str:
    """
    Muestra el catalogo de postres
    """
    print("Postres del menu:")
    for postre in lista_de_postres:
        print(f"Postre: {postre.nombre} Valor: {postre.precio} ")


mostrar_postres()
