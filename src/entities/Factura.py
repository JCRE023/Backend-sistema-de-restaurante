class Factura:
    def __init__(self, pedidos_mesa: list) -> None:
        """
        Recibe la lista de objetos (PlatoPrincipal, etc.) que tiene la mesa
        """
        self.productos = pedidos_mesa
        self.propina = 0
        self.subtotal = 0
        self.total_final = 0

    def calcular_cuenta(self) -> float:
        """
        Suma los precios de todos los objetos en la lista de pedidos
        """
        self.subtotal = sum(producto.precio for producto in self.productos)
        self.total_final = self.subtotal + self.propina
        return self.subtotal

    def aplicar_propina(self, porcentaje: float) -> None:
        """
        Calcula la propina basada en el subtotal
        """
        self.propina = self.subtotal * (porcentaje / 100)
        self.total_final = self.subtotal + self.propina

    def mostrar_detalle(self):
        """
        Imprime un resumen elegante de la cuenta
        """
        print("\n" + "=" * 25)
        print("      FACTURA       ")
        print("=" * 25)
        for p in self.productos:
            print(f"{p.nombre:15} ${p.precio:>8}")
        print("-" * 25)
        print(f"Subtotal:       ${self.subtotal:>8}")
        print(f"Propina:        ${self.propina:>8}")
        print(f"TOTAL:          ${self.total_final:>8}")
        print("=" * 25)

    def aplicar_propina_monto(self, monto: float) -> None:
        """
        Aplica un monto de propina ya calculado previamente
        """
        self.propina = monto
        self.total_final = self.subtotal + self.propina
