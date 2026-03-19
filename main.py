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
    s = input(mensaje).strip()
    return s if s else default


def leer_float(mensaje: str, default: float = 0.0) -> float:
    try:
        return float(input(mensaje).strip() or default)
    except ValueError:
        return default


def leer_int(mensaje: str, default: int = 0) -> int:
    try:
        return int(input(mensaje).strip() or default)
    except ValueError:
        return default


def leer_uuid(mensaje: str) -> Optional[UUID]:
    s = input(mensaje).strip()
    if not s:
        return None
    try:
        return UUID(s)
    except ValueError:
        return None


def ingresar_o_crear_usuario() -> Optional[Usuario]:

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


def menu_facturas(usuario_id: UUID) -> None:
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
