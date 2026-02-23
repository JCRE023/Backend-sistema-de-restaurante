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
            print("")
        elif opcion == "2":
            print("")
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
