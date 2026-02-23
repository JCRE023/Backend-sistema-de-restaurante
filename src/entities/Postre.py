from producto import Producto

Lista_De_Postres = [
    Producto("Trufas", 3000),
    Producto("Brownie", 5000),
    Producto("Copa de fresa", 12000),
    Producto("Helado 1 bola", 4000),
    Producto("Helado 2 bolas", 6000),
]


def Mostrar_Postres() -> str:
    """
    Muestra el catalogo de postres
    """
    print("Postres del menu:")
    for Postre in Lista_De_Postres:
        print(f"Postre: {Postre.nombre} Valor: {Postre.precio} ")


Mostrar_Postres()
