import sys
from typing import Optional
from uuid import UUID

sys.path.insert(0, ".")

from src.crud import factura_crud as crud_factura
from src.crud import usuario_crud as crud_usuario
from src.crud.Detalle_orden_crud import Detalle_orden_crud
from src.crud.Orden_crud import Orden_crud
from src.crud.Producto_crud import ProductoCRUD
from src.crud import Mesa_crud as crud_mesa

from src.entities.Usuario import Usuario


def leer_texto(mensaje: str, default: str = "") -> str:
    """
    Lee una cadena de texto desde la entrada.
    Si el usuario no ingresa ningún valor, retorna el valor por defecto.

    Parameters:
    mensaje : str
        Texto que se muestra al usuario como indicación de entrada.
    default : str, optional
        Valor retornado si el usuario no ingresa nada. Por defecto "".

    Returns:
    str
        Texto ingresado por el usuario, o el valor por defecto si la entrada está vacía.
    """
    s = input(mensaje).strip()
    return s if s else default


def leer_float(mensaje: str, default: float = 0.0) -> float:
    """
    Lee un número decimal desde la entrada.
    Si el usuario no ingresa ningún valor o ingresa un texto no convertible
    a float, retorna el valor por defecto sin interrumpir la ejecución.

    Parameters:
    mensaje : str
        Texto que se muestra al usuario como indicación de entrada.
    default : float, optional
        Valor retornado si la entrada está vacía o es inválida. Por defecto 0.0.

    Returns:
    float
        Número decimal ingresado por el usuario, o el valor por defecto
        si la entrada es vacía o no es convertible a float.
    """
    try:
        return float(input(mensaje).strip() or default)
    except ValueError:
        return default


def leer_int(mensaje: str, default: int = 0) -> int:
    """
    Lee un número entero desde la entrada.
    Si el usuario no ingresa ningún valor o ingresa un texto no convertible
    a int, retorna el valor por defecto sin interrumpir la ejecución.

    Parameters:
    mensaje : str
        Texto que se muestra al usuario como indicación de entrada.
    default : int
        Valor retornado si la entrada está vacía o es inválida. Por defecto 0.

    Returns:
    int
        Número entero ingresado por el usuario, o el valor por defecto
        si la entrada es vacía o no es convertible a int.
    """
    try:
        return int(input(mensaje).strip() or default)
    except ValueError:
        return default


def leer_uuid(mensaje: str) -> Optional[UUID]:
    """
    Lee un identificador UUID desde la entrada.
    Si el usuario no ingresa ningún valor retorna None. Si el texto ingresado
    no corresponde a un formato UUID, también retorna None sin
    interrumpir la ejecución.

    Parameters:
    mensaje : str
        Texto que se muestra al usuario como indicación de entrada.

    Returns:
    Optional[UUID]
        Objeto UUID construido a partir de la entrada del usuario,
        o None si la entrada está vacía o tiene un formato inválido.
    """
    s = input(mensaje).strip()
    if not s:
        return None
    try:
        return UUID(s)
    except ValueError:
        return None


def ingresar_o_crear_usuario() -> Optional[Usuario]:
    """
    Muestra un menú interactivo para autenticar o registrar un usuario.
    Presenta tres opciones al operador: iniciar sesión con credenciales
    existentes, registrar un nuevo usuario, o salir del sistema.

    Returns:
    Optional[Usuario]
        El objeto Usuario autenticado si las credenciales son correctas,
        o None si el usuario elige salir sin autenticarse.

    """

    while True:
        print("\n--- Inicio de Sesión / Registro ---")
        print("1. Login  2. Crear Usuario (Primer registro)  0. Salir")
        op = leer_texto("Opción: ")

        if op == "0":
            return None

        nombre = leer_texto("Usuario: ")
        contra = leer_texto("Contraseña: ")

        if op == "1":
            usuario = crud_usuario.login(nombre, contra)
            if usuario:
                print(f"\nBienvenido, {usuario.username}.\n")
                return usuario
            print("Credenciales incorrectas.")

        elif op == "2":
            rol = leer_texto("Rol (usuario/admin): ", "usuario")
            try:
                nuevo_usuario = crud_usuario.crear(nombre, contra, rol)
                print(f"Usuario {nuevo_usuario.username} creado exitosamente.")
            except Exception as e:
                print("Error al crear usuario:", e)


def menu_mesas(usuario_id: UUID) -> None:
    """
    Muestra el submenú interactivo para la gestión de mesas del restaurante.
    Permite al operador listar todas las mesas registradas, crear nuevas
    mesas, actualizar su estado y eliminarlas.

    Parameters:
    usuario_id : UUID
        Identificador del usuario autenticado, utilizado para registrar
        la auditoría de creación al añadir una nueva mesa.

    Returns:
    None

    """
    while True:
        print("\n--- Gestión de Mesas ---")
        print(
            "1. Lista de mesas  2. Crear mesas 3. Actualizar estado  4. Eliminar  0. Volver"
        )
        op = leer_texto("Opción: ")
        if op == "0":
            break

        if op == "1":
            for m in crud_mesa.obtener_todos():
                print(f"ID: {m.id_mesa} | Nº: {m.numero_mesa} | Estado: {m.estado}")
        elif op == "2":
            num = leer_texto("Número/Nombre de mesa: ")
            est = leer_texto("Estado (DISPONIBLE/OCUPADA): ", "DISPONIBLE")
            try:
                crud_mesa.crear_mesa(num, usuario_id, est)
                print("Mesa creada.")
            except Exception as e:
                print(f"Error: {e}")
        elif op == "3":
            id_m = leer_uuid("ID de la mesa: ")
            nuevo_est = leer_texto("Nuevo estado: ")
            if id_m:
                crud_mesa.actualizar_estado(id_m, nuevo_est)


def menu_productos(db_session, usuario_id: UUID) -> None:
    """
    Muestra el submenú interactivo para la gestión del catálogo de productos.
    Instancia la clase ProductoCRUD con la sesión de base de datos activa
    y permite al operador listar, crear, actualizar y eliminar productos
    del menú del restaurante.

    Parameters:
    db_session
        Sesión activa de SQLAlchemy utilizada por ProductoCRUD para
        realizar las operaciones de persistencia.
    usuario_id : UUID
        Identificador del usuario autenticado, utilizado para registrar
        la auditoría de creación al añadir un nuevo producto.

    Returns:
    None

    """
    crud = ProductoCRUD(db_session)
    while True:
        print("\n--- Gestión de Productos ---")
        print(
            "1. Lista de productos  2. Crear producto  3. Actualizar producto 4. Eliminar  0. Volver"
        )
        op = leer_texto("Opción: ")
        if op == "0":
            break

        if op == "1":
            for p in crud.obtener_productos():
                print(f"ID: {p.id_producto} | {p.nombre} | ${p.precio}")
        elif op == "2":
            nom = leer_texto("Nombre: ")
            pre = leer_float("Precio: ")
            cat = leer_texto("Categoría: ")
            desc = leer_texto("Descripción: ")
            try:
                crud.crear_producto(nom, pre, cat, usuario_id, desc)
                print("Producto creado.")
            except Exception as e:
                print(f"Error: {e}")


def menu_ordenes(db_session, usuario_id: UUID) -> None:
    """
    Muestra el submenú interactivo para la gestión del ciclo de vida de órdenes.
    Instancia la clase Orden_crud con la sesión de base de datos activa
    y permite al operador abrir nuevas órdenes en mesas disponibles,
    cerrarlas al finalizar el servicio y consultar sus detalles.

    Parameters:
    db_session
        Sesión activa de SQLAlchemy utilizada por Orden_crud para
        realizar las operaciones de persistencia.
    usuario_id : UUID
        Identificador del usuario autenticado, registrado como el mesero
        responsable al momento de abrir una nueva orden.

    Returns:
    None

    """
    crud = Orden_crud(db_session)
    while True:
        print("\n--- Gestión de Órdenes (Servicio) ---")
        print("1. Abrir Orden  2. Cerrar Orden  3. Ver Detalles de Orden  0. Volver")
        op = leer_texto("Opción: ")
        if op == "0":
            break

        if op == "1":
            id_m = leer_uuid("ID de Mesa: ")
            if id_m:
                try:
                    o = crud.crear_orden(id_m, usuario_id)
                    print(f"Orden {o.id_orden} abierta en mesa {id_m}.")
                except Exception as e:
                    print(f"Error: {e}")
        elif op == "2":
            id_o = leer_uuid("ID de Orden a cerrar: ")
            if id_o:
                crud.cerrar_orden(id_o)
                print("Orden cerrada y mesa liberada.")


def menu_detalles_orden(db_session) -> None:
    """
    Muestra el submenú interactivo para la gestión de ítems de una comanda.
    Instancia la clase Detalle_orden_crud con la sesión de base de datos
    activa y permite al operador agregar productos a una orden abierta,
    modificar cantidades de ítems existentes y eliminar ítems de la
    comanda.

    Parameters:
    db_session
        Sesión activa de SQLAlchemy utilizada por Detalle_orden_crud
        para realizar las operaciones de persistencia.

    Returns:
    None
    """
    crud = Detalle_orden_crud(db_session)
    while True:
        print("\n--- Detalles de Comanda (Items) ---")
        print(
            "1. Agregar Producto a Orden  2. Modificar Cantidad  3. Quitar Item  0. Volver"
        )
        op = leer_texto("Opción: ")
        if op == "0":
            break

        if op == "1":
            id_o = leer_uuid("ID Orden: ")
            id_p = leer_uuid("ID Producto: ")
            cant = leer_int("Cantidad: ")
            if id_o and id_p:
                try:
                    crud.crear_detalle(id_o, id_p, cant)
                    print("Producto añadido.")
                except Exception as e:
                    print(f"Error: {e}")
        elif op == "2":
            id_d = leer_uuid("ID Detalle: ")
            cant = leer_int("Nueva cantidad: ")
            if id_d:
                try:
                    detalle = crud.actualizar_detalle(id_d, cant)
                    if detalle:
                        print(f"Cantidad actualizada a {detalle.cantidad}.")
                    else:
                        print("Detalle no encontrado.")
                except Exception as e:
                    print(f"Error: {e}")
        elif op == "3":
            id_d = leer_uuid("ID Detalle a eliminar: ")
            if id_d:
                try:
                    eliminado = crud.eliminar_detalle(id_d)
                    if eliminado:
                        print("Ítem eliminado de la comanda.")
                    else:
                        print("Detalle no encontrado.")
                except Exception as e:
                    print(f"Error: {e}")


def menu_facturas(usuario_id: UUID) -> None:
    """
    Muestra el submenú interactivo para la gestión de facturación.
    Permite al operador listar todas las facturas registradas en el sistema,
    generar una nueva factura asociada a una orden cerrada y consultar las
    facturas emitidas por un usuario específico.

    Parameters:
    usuario_id : UUID
        Identificador del usuario autenticado, registrado como el emisor
        de la factura al momento de generarla.

    Returns:
    None
    """
    while True:
        print("\n--- Facturación ---")
        print("1. Listar Todas  2. Generar Factura  3. Buscar por Usuario  0. Volver")
        op = leer_texto("Opción: ")
        if op == "0":
            break

        if op == "1":
            for f in crud_factura.obtener_todos():
                print(f"ID: {f.id_factura} | Total: {f.total} | Orden: {f.id_orden}")
        elif op == "2":
            id_o = leer_uuid("ID Orden: ")
            total = leer_float("Total Factura: ")
            if id_o:
                crud_factura.crear(total, id_o, usuario_id)
                print("Factura generada.")


def main() -> None:
    """
    Punto de entrada principal del Sistema de Gestión de Restaurante.
    Inicializa la sesión de base de datos, gestiona la autenticación del
    operador y presenta el menú principal desde el cual se accede a todos
    los submódulos del sistema. El bucle se mantiene activo hasta que el
    usuario elija salir.

    Returns:
    None
    """
    from src.database.config import SessionLocal

    db = SessionLocal()

    usuario = ingresar_o_crear_usuario()
    if not usuario:
        print("Saliendo del sistema.")
        return

    while True:
        print("\n========== SISTEMA DE RESTAURANTE ==========")
        print(f"Usuario: {usuario.username} | Rol: {usuario.rol}")
        print("1. Mesas")
        print("2. Productos")
        print("3. Órdenes (Apertura/Cierre)")
        print("4. Comandas (Agregar Items)")
        print("5. Facturación")
        print("0. Salir")

        op = leer_texto("Opción: ")

        if op == "0":
            print(f"Hasta luego, {usuario.username}.")
            break
        elif op == "1":
            menu_mesas(usuario.id_usuario)
        elif op == "2":
            menu_productos(db, usuario.id_usuario)
        elif op == "3":
            menu_ordenes(db, usuario.id_usuario)
        elif op == "4":
            menu_detalles_orden(db)
        elif op == "5":
            menu_facturas(usuario.id_usuario)
        else:
            print("Opción no válida.")


if __name__ == "__main__":
    main()
