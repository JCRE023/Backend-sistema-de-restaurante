class PlatoPrincipal:
    def __init__(self, nombre, ingredientes, precio):
        self.nombre = nombre
        self.ingredientes = ingredientes
        self.precio = precio

    def __str__(self):
        return f"[{self.id_plato}] {self.nombre.upper()}: ${self.precio}"
