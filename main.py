from src.entities.Bebida import Bebida
from src.entities.Factura import Factura
from src.entities.Plato_principal import PlatoPrincipal
from src.entities.Postre import Postre
from src.entities.Mesa import Mesa, mostrar_mesas_disponibles, buscar_mesa_por_nombre

print("¡¡¡Bienvenido al menu del restaurante!!!")


def menu_principal():
    print("-" * 30)
    opcion = input(
        "RESTAURANTE MENU\n"
        "1. Reservar mesa\n"
        "2. Ordenar plato\n"
        "3. Agregar / Eliminar producto\n"
        "4. Aplicar propina\n"
        "5. Calcular cuenta\n"
        "6. Pagar\n"
        "0. Salir\n"
        "Seleccione una opción: "
    )
    if opcion.isdigit() == False:
        print("¡Debes ingresar un numero!")

    while True:
        if opcion == "1":
            print("\n--- GESTIÓN DE DISPONIBILIDAD ---")
            mostrar_mesas_disponibles()

            nombre_m = input("\nIntroduce el nombre de la mesa (Ej: Mesa 1): ")
            mesa = buscar_mesa_por_nombre(nombre_m)

            if mesa:

                print(
                    f"La {mesa.nombre} actualmente está {'Disponible' if mesa.disponible else 'Ocupada'}."
                )
                respuesta = input("¿Desea cambiar su estado? (si/no): ").lower()

                if respuesta == "si":

                    mesa.disponible = not mesa.disponible
                    print(
                        f"Éxito: La {mesa.nombre} ahora está {'Disponible' if mesa.disponible else 'Ocupada'}."
                    )
            else:
                print("Error: Esa mesa no existe.")

        elif opcion == "2":
            print("\n--- NUEVA ORDEN ---")
            nombre_m = input("¿Para qué mesa es el pedido?: ")
            mesa = buscar_mesa_por_nombre(nombre_m)

            if mesa:

                PlatoPrincipal.mostrar_platos_principales()
                Postre.mostrar_postres()
                Bebida.mostrar_bebidas()

                prod_nombre = input("\nEscribe el nombre del producto: ")

                producto = buscar_producto(prod_nombre)

                if producto:

                    mesa.agregar_pedido(producto)

                    mesa.disponible = False
                else:
                    print("Error: El producto no existe en el menú.")
            else:
                print("Error: Mesa no encontrada.")
        elif opcion == "3":
            print("")
        elif opcion == "4":
            print("")
        elif opcion == "5":
            print("")
        elif opcion == "6":
            print("")
        elif opcion == "0":
            print("Saliendo del Sistema...")
            break
        else:
            print("Opcion ingresada no valida, vuelve a intentarlo")

        print("-" * 30)
        opcion = input(
            "RESTAURANTE MENU\n"
            "1. Reservar mesa\n"
            "2. Ordenar plato\n"
            "3. Agregar / Eliminar producto\n"
            "4. Aplicar propina\n"
            "5. Calcular cuenta\n"
            "6. Pagar\n"
            "0. Salir\n"
            "Seleccione una opción: "
        )
        if opcion.isdigit() == False:
            print("¡Debes ingresar un numero!")


menu_principal()


def buscar_producto(nombre: str):
    """
    Busca un producto por su nombre en las listas de platos, bebidas y postres.

    Args:
        nombre (str): El nombre del artículo a buscar.

    Returns:
        Union[PlatoPrincipal, Postre, None]: El objeto encontrado o None.
    """

    for plato in PlatoPrincipal.lista_de_platos_principales:
        if plato.nombre.lower() == nombre.lower():
            return plato

    for postre in Postre.lista_de_postres:
        if postre.nombre.lower() == nombre.lower():
            return postre

    for bebida in Bebida.lista_de_bebidas:
        if bebida.nombre.lower() == nombre.lower():
            return bebida

    return None
