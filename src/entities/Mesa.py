class Mesa:
    """
    Crea un objeto mesa para el restaurante
    """

    def __init__(self, nombre: str, sillas: int, disponible: bool) -> None:
        self.nombre = nombre
        self.sillas = sillas
        self.disponible = disponible


lista_de_mesas = [
    Mesa("Mesa 1", 4, True),
    Mesa("Mesa 2", 6, True),
    Mesa("Mesa 3", 4, True),
    Mesa("Mesa 4", 4, True),
    Mesa("Mesa 5", 2, True),
    Mesa("Mesa 6", 8, True),
    Mesa("Mesa 7", 8, True),
    Mesa("Mesa 8", 2, True),
]


def Mostrar_Mesas_Disponibles() -> str:
    """
    Imprime con un SI o NO si la mesa esta ocupada
    """
    print("Mesas totales:")
    for mesa in lista_de_mesas:
        if mesa.disponible is True:
            print(f"{mesa.nombre} | Sillas: {mesa.sillas} | Disponible: SI")
        else:
            print(f"{mesa.nombre} | Sillas: {mesa.sillas} | Disponible: NO")


def actualizar_disponibilidad() -> str:
    """
    Actualiza a las mesas, si estan disponibles o ocupadas
    """
    buscar = input("Introduce el nombre de la mesa (Ej: Mesa 3): ")
    for mesa in lista_de_mesas:
        if mesa.nombre == buscar:
            respuesta = input(f"¿Está la {mesa.nombre} disponible? (si/no): ").lower()
            if respuesta == "si":
                mesa.disponible = True
            else:
                mesa.disponible = False
            print(f"La disponibilidad de la {mesa.nombre} ha sido actualizada.")
            break


actualizar_disponibilidad()
Mostrar_Mesas_Disponibles()
