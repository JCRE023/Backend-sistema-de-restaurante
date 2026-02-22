class Mesa:
    def __init__(self, nombre, sillas, disponible):
        self.nombre = nombre
        self.sillas = sillas
        self.disponible = disponible


lista_de_mesas = []

mesa_1 = Mesa("Mesa 1", 4, True)
lista_de_mesas.append(mesa_1)

mesa_2 = Mesa("Mesa 2", 6, True)
lista_de_mesas.append(mesa_2)

mesa_3 = Mesa("Mesa 3", 4, True)
lista_de_mesas.append(mesa_3)

mesa_4 = Mesa("Mesa 4", 4, True)
lista_de_mesas.append(mesa_4)

mesa_5 = Mesa("Mesa 5", 2, True)
lista_de_mesas.append(mesa_5)

mesa_6 = Mesa("Mesa 6", 8, True)
lista_de_mesas.append(mesa_6)

mesa_7 = Mesa("Mesa 7", 8, True)
lista_de_mesas.append(mesa_7)

mesa_8 = Mesa("Mesa 8", 2, True)
lista_de_mesas.append(mesa_8)


def Mostrar_Mesas_Disponibles():

    print("Mesas totales:")
    for mesa in lista_de_mesas:
        if mesa.disponible is True:
            print(f"{mesa.nombre} | Sillas: {mesa.sillas} | Disponible: SI")
        else:
            print(f"{mesa.nombre} | Sillas: {mesa.sillas} | Disponible: NO")


def actualizar_disponibilidad():
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
