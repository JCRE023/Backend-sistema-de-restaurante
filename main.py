from src.entities.Bebida import Bebida
from src.entities.Factura import Factura
from src.entities.Plato_principal import PlatoPrincipal
from src.entities.Postre import Postre
from src.entities.Mesa import Mesa, mostrar_mesas_disponibles, buscar_mesa_por_nombre

print("¡¡¡Bienvenido al menu del restaurante!!!")


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
        "7. añadir / eliminar producto del catalogo\n"
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
            print("\n--- AÑADIR / ELIMINAR PRODUCTO DE LA CUENTA ---")

            op = input(
                "Que opcion quiere hacer?\n"
                "1. Eliminar producto\n"
                "2. Añadir producto\n"
            )

            if op == "1":

                nombre_tres = input("\nIntroduce el nombre de la mesa (Ej: Mesa 1): ")

                mesa_tres = buscar_mesa_por_nombre(nombre_tres)

                mesa_tres.mostrar_pedido()

                elimina = input("Que producto desea eliminar?: ")

                mesa_tres.eliminar_pedido(elimina)

                print("Producto eliminado exitosamente, lista de productos:")

                mesa_tres.mostrar_pedido()

            elif op == "2":

                nombre_tres = input("\nIntroduce el nombre de la mesa (Ej: Mesa 1): ")

                mesa_tres = buscar_mesa_por_nombre(nombre_tres)

                PlatoPrincipal.mostrar_platos_principales()
                Postre.mostrar_postres()
                Bebida.mostrar_bebidas()

                prod_nombre = input("\nEscribe el nombre del producto: ")

                producto = buscar_producto(prod_nombre)

                if producto:

                    mesa_tres.agregar_pedido(producto)

                    mesa_tres.disponible = False
                else:
                    print("Error: El producto no existe en el menú.")

        elif opcion == "4":
            print("")
        elif opcion == "5":
            print("\n--- CALCULAR CUENTA ---")
            nombre_m = input("¿Para qué mesa deseas calcular la cuenta?: ")
            mesa = buscar_mesa_por_nombre(nombre_m)
            if mesa:
                if len(mesa.pedido) == 0:
                    print("Error: La mesa no tiene pedidos registrados.")
                else:
                    factura = Factura(mesa.pedido)
                    factura.calcular_cuenta()
                    factura.mostrar_detalle()
            else:
                print("Error: Mesa no encontrada.")
        elif opcion == "6":
            print("")
        elif opcion == "7":
            print("\n--- Agregar / eliminar producto ---")

            op = input(
                "Que opcion quiere hacer?\n"
                "1. Añadir producto\n"
                "2. Eliminar producto\n"
            )

            if op == "1":

                categoria = input(
                    "Seleccione la categoria del producto nuevo\n"
                    "1. Postre\n"
                    "2. Plato Principal\n"
                    "3. Bebida\n"
                )

                nombre = input("Nombre del producto: ")
                precio = int(input("Precio: "))

                if categoria == "1":

                    sabor = input("Sabor: ")
                    nuevo = Postre(nombre, precio, sabor)
                    Postre.lista_de_postres.append(nuevo)
                    print(
                        "Producto añadido exitosamente, se muestran los postres totales:"
                    )
                    Postre.mostrar_postres()

                elif categoria == "2":

                    tipo = input("Tipo? Vegano, Carne, etc: ")
                    nuevo = PlatoPrincipal(nombre, precio, tipo)
                    PlatoPrincipal.lista_de_platos_principales.append(nuevo)
                    print(
                        "Producto añadido exitosamente, se muestran los postres totales:"
                    )
                    PlatoPrincipal.mostrar_platos_principales()

                elif categoria == "3":

                    marca = input("Marca: ")
                    tamano = input("Tamaño (En Mll): ")
                    nuevo = Bebida(nombre, precio, marca, tamano)
                    Bebida.lista_de_bebidas.append(nuevo)
                    print("Producto añadido exitosamente")
                    Bebida.mostrar_bebidas()

            elif op == "2":
                eliminar = input(
                    "Seleccione la categoria del producto a eliminar: \n"
                    "1. Postre\n"
                    "2. Plato Principal\n"
                    "3. Bebida\n"
                )

                if eliminar == "1":

                    Postre.mostrar_postres()
                    nombre = input("Nombre del producto a eliminar: ").lower()

                    almacenar = None

                    for i in Postre.lista_de_postres:
                        if i.nombre.lower() == nombre:
                            almacenar = i
                            break

                    if almacenar:
                        Postre.lista_de_postres.remove(almacenar)
                        print("Eliminado correctamente")
                        Postre.mostrar_postres()

                elif eliminar == "2":

                    PlatoPrincipal.mostrar_platos_principales()
                    nombre = input("Nombre exacto del producto a eliminar: ")

                    almacenar = None

                    for i in PlatoPrincipal.lista_de_platos_principales:
                        if i.nombre == nombre:
                            almacenar = i
                            break

                    if almacenar:

                        PlatoPrincipal.lista_de_platos_principales.remove(almacenar)
                        print("Eliminado correctamente")
                        PlatoPrincipal.mostrar_platos_principales()

                elif eliminar == "3":
                    Bebida.mostrar_bebidas()
                    nombre = input("Nombre exacto del producto a eliminar: ")

                    almacenar = None

                    for i in Bebida.lista_de_bebidas:
                        if i.nombre == nombre:
                            almacenar = i
                            break

                    if almacenar:

                        Bebida.lista_de_bebidas.remove(almacenar)
                        print("Eliminado correctamente")
                        Bebida.mostrar_bebidas()

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
            "7. añadir / eliminar producto del catalogo\n"
            "0. Salir\n"
            "Seleccione una opción: "
        )
        if opcion.isdigit() == False:
            print("¡Debes ingresar un numero!")


menu_principal()
