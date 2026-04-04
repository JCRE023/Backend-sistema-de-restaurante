# 📑 Informe Técnico: Backend Sistema de Gestión de Restaurante

---

## 1. Introducción

El presente proyecto implementa una solución de software para la gestión operativa de un establecimiento gastronómico. Utiliza el lenguaje Python junto con el ORM SQLAlchemy y se fundamenta en el paradigma de Programación Orientada a Objetos (POO).

El sistema se conecta a una base de datos PostgreSQL alojada en la nube mediante el servicio Neon, empleando conexiones seguras con SSL. La interfaz de operación es un menú interactivo por consola que guía al usuario a través del ciclo completo de servicio de un restaurante: desde la autenticación hasta la generación de facturas.

---

## 2. Arquitectura de Software

### 2.1 Separación en Capas

El proyecto tiene una arquitectura en tres capas diferenciadas que permite la independencia entre la lógica de negocio, la persistencia y la presentación:

- Capa de Entidades: Define los modelos ORM que estableces directamente las tablas de la base de datos mediante SQLAlchemy. Cada clase hereda de `Base` y declara sus columnas, relaciones y restricciones.

- Capa CRUD : Contiene la lógica de acceso a datos y las validaciones de negocio (Create, Read, Update, Delete). Algunos módulos adoptan el patrón clase, mientras que otros requieren funciones independientes que realizan su propia sesión.

- Capa de Presentación: Implementa los menús interactivos de consola, lee la entrada del usuario y delega las operaciones a los módulos CRUD correspondientes.

### 2.2 Configuración de Base de Datos

El módulo `config.py` centraliza toda la configuración de conexión. Carga la variable `DATABASE_URL` desde el archivo `.env` mediante `python-dotenv` y crea el motor de SQLAlchemy.

### 2.3 Relaciones entre Entidades

- Asociación: `Orden` y `Mesa` están vinculadas, al abrir una orden la mesa cambia de estado, y al cerrarla la mesa queda disponible nuevamente.
- Composición `Detalle_orden` depende completamente de una `Orden` existente, no puede existir sin ella.
- Asociación `Factura` procesa la información de una `Orden` para registrar el cobro final.

---

## 3. Especificaciones de Clases

### 📦 Entidad: `Usuario`

Representa a los operadores del sistema. Implementa encapsulamiento al almacenar la contraseña únicamente en su forma hasheada, nunca en texto plano. El crud del usuario expone además una función `login()` que encapsula la verificación de credenciales.

### 🪑 Entidad: `Mesa`

Gestiona las mesas físicas del restaurante con control de disponibilidad. Implementa lógica de estado para controlar el flujo de ocupación e incluye auditoría de usuario tanto en la creación como en cada edición.

### 🍽️ Entidad: `Producto`

Catálogo de ítems disponibles en el menú del restaurante. Aplica auditoría completa registrando tanto al usuario que crea el producto como al que lo modifica.

### 📋 Entidad: `Orden`

Representa un servicio activo vinculado a una mesa y un mesero. Implementa un ciclo de vida controlado con dos estados posibles: `abierta` y `cerrada`.

### 🧾 Entidad: `Detalle_orden`

Representa cada ítem de una comanda: la cantidad de un producto dentro de una orden. Su existencia depende de que la orden asociada esté en estado `abierta`, lo que garantiza la integridad de los pedidos en curso.

### 💰 Entidad: `Factura`

Documento de cobro generado al concluir el servicio de una mesa. Asocia un monto total con la orden atendida y el usuario que realizó el cobro.

## 4. Lógica de Negocio

### 4.1 Algoritmo de Ciclo de Servicio

El flujo operativo del sistema sigue una secuencia estricta para garantizar la integridad de los datos en cada etapa del servicio:

1. Autenticación: El usuario inicia sesión con sus credenciales. El sistema verifica que el hash de la contraseña ingresada coincida con el guardado.

2. Apertura de Orden: Se valida que la mesa exista y tenga estado `DISPONIBLE`. Al confirmar, la mesa pasa automáticamente a `OCUPADA` y se registra la nueva orden en estado `abierta`.

3. Adición de Ítems: Se pueden agregar productos a la orden mientras este `abierta`. Cada ítem registra el producto y la cantidad solicitada, con validación de que la cantidad sea mayor a cero y que tanto la orden como el producto existan.

4. Cierre de Orden: La orden pasa a estado `cerrada`. Como efecto paso inmediato, la mesa asociada regresa automáticamente al estado `DISPONIBLE`, quedando lista para una nueva atención.

5. Generación de Factura: Se registra el cobro vinculado a la orden cerrada, almacenando el total y el usuario que realizó la operación.

### 4.2 Validaciones de Negocio

El sistema aplica las siguientes restricciones en la capa CRUD antes de persistir cualquier dato:

- Los nombres de usuario y nombres de mesa deben ser únicos, se lanza `ValueError` ante duplicados.
- Las contraseñas nunca se almacenan en texto plano, siempre se hashean antes de guardarlas.
- Los estados de mesa solo aceptan los valores `DISPONIBLE`, `OCUPADA` o `RESERVADA`.
- Solo se pueden crear, modificar o eliminar detalles de orden sobre órdenes en estado `abierta`.
- El precio de un producto y la cantidad de un ítem deben ser siempre valores positivos mayores a cero.
- Al crear un producto, se verifica que el usuario creador exista en la base de datos.

---

## 5. Dependencias del Proyecto

| Paquete | Versión mínima | Propósito |
| `sqlalchemy` | 2.0.0 | ORM y gestión de sesiones |
| `psycopg2-binary` | 2.9.0 | Driver de conexión a PostgreSQL |
| `python-dotenv` | 1.0.0 | Carga de variables de entorno |
| `pydantic` | 2.0.0 | Validación de datos |


Video Johan Steven Bermudez
www.youtube.com/watch?v=LOaMkQZE8tE&feature=youtu.be

Video Juan camilo rodriguez 
https://drive.google.com/file/d/1KJFgDxC0WnQFvh8zPeNKDkjJ75ivL-jm/view?usp=sharing

video Euner Murillo
https://youtu.be/9d27BIkQR4w

Video Santiago cano 

https://youtu.be/vycEs9QUosI
https://youtu.be/0Sc0kfJXHmY
