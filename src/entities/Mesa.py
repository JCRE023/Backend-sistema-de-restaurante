class Mesa:
    """
    Crea un objeto mesa para el restaurante
    """

    def __init__(self, nombre: str, sillas: int, disponible: bool) -> None:
        self.nombre = nombre
        self.sillas = sillas
        self.disponible = disponible
        self.pedido = []

    def agregar_pedido(self, producto) -> None:
        """
        añade un platoprincipal, bebida o postre a la mesa
        """
        self.pedido.append(producto)
        print(f"{producto.nombre} agregado a la {self.nombre}")

    def limpiar_mesa(self) -> None:
        """
        se libera la mesa cuando el cliente paga
        """
        self.pedido = []
        self.disponible = True

    def mostrar_pedido(self):
        for n in self.pedido:
            print(f"Nombre: {n.nombre} ")

    def eliminar_pedido(self, elimina: str) -> None:

        almacenar = None

        for i in self.pedido:
            if i.nombre.lower() == elimina.lower():
                almacenar = i
                break

        if almacenar:
            self.pedido.remove(almacenar)


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


def mostrar_mesas_disponibles() -> None:
    """
    Imprime con un SI o NO si la mesa esta ocupada
    """
    print("Mesas totales:")
    for mesa in lista_de_mesas:
        if mesa.disponible is True:
            print(f"{mesa.nombre} | Sillas: {mesa.sillas} | Disponible: SI")
        else:
            print(f"{mesa.nombre} | Sillas: {mesa.sillas} | Disponible: NO")


def buscar_mesa_por_nombre(nombre_buscado: str) -> object:
    """
    Busca una mesa por su nombre y devuelve el objeto correspondiente.
    """
    for mesa in lista_de_mesas:
        if mesa.nombre.lower() == nombre_buscado.lower():
            return mesa
    return None


def actualizar_disponibilidad() -> str:
    """
    Actualiza las mesas, si estan disponibles o no.
    """
    nombre = input("Introduce el nombre de la mesa (Ej: Mesa 3): ")
    mesa = buscar_mesa_por_nombre(nombre)

    if mesa:
        respuesta = input(f"Esta la {mesa.nombre} disponible? (si/no): ")
        mesa.disponible = respuesta == "si"
        print(f"La disponibilidad ded la {mesa.nombre} ha sido actualizada")
    else:
        print("Error, la mesa no existe.")
