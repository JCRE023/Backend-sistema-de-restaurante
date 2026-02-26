📑 Informe Técnico: Backend Sistema de Restaurante
1. Introducción

El presente proyecto implementa una solución de software para la gestión operativa de un establecimiento gastronómico. Utiliza el lenguaje Python y se fundamenta en el paradigma de Programación Orientada a Objetos (POO) para garantizar un código modular, mantenible y escalable.
2. Arquitectura de Software
2.1 Modelo de Datos y Herencia

El sistema utiliza una jerarquía de clases para la gestión de productos. La clase abstracta Producto sirve como base, permitiendo que las subclases compartan lógica de validación de precios mientras mantienen atributos específicos.
2.2 Relación entre Entidades

    Agregación: Una Mesa contiene una lista de objetos tipo Producto.

    Asociación: La clase Factura procesa la información contenida en una Mesa para realizar los cálculos financieros.

3. Especificaciones de Clases
📦 Clase Base: Producto

    Encapsulamiento: Implementación de @property para proteger el acceso a atributos sensibles.

    Polimorfismo: Preparada para que cada subclase pueda redefinir su método de visualización.

🍱 Subclases: Plato_principal, Postre, Bebida

    Cada subclase gestiona su propio catálogo mediante atributos de clase (lista_de_...), permitiendo que el menú sea compartido por todas las mesas.

🪑 Gestión de Estado: Mesa

    Implementa lógica de negocio para el control de inventario local (pedido) y estados de ocupación.

4. Lógica de Negocio (Algoritmo de Pago)

El flujo de cierre de cuenta sigue un proceso secuencial para garantizar la integridad de los datos:

   1. Cálculo de Subtotal: Suma de los precios de los objetos dentro del atributo pedido.

   2. Cálculo de Propina: Aplicación del porcentaje seleccionado sobre el subtotal.

   3. Instanciación de Factura: Generación del objeto Factura para reporte.

   4. Reseteo de Estado: Limpieza de la lista de pedidos y cambio del booleano disponible a True.

5. Manual de Operación para el Usuario

Para operar el sistema, el usuario debe seguir el menú interactivo:

    1. Gestión de Inventario: Use la Opción 7 para poblar el menú antes de comenzar las ventas.

    2. Ciclo de Venta: Reservar (Opción 1) -> Ordenar (Opción 2) -> Pagar (Opción 6).

    3. Modificaciones: Use la Opción 3 para correcciones en pedidos activos si un cliente desiste de un producto.
