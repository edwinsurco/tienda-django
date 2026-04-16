from .models import Producto


class Carrito:

    def __init__(self, request):
        self.session = request.session
        carrito = self.session.get('carrito')

        if not carrito:
            carrito = self.session['carrito'] = {}

        self.carrito = carrito

    def agregar(self, producto):
        producto_id = str(producto.id)

        if producto_id not in self.carrito:
            self.carrito[producto_id] = {
                'nombre': producto.nombre,
                'precio': float(producto.precio),
                'cantidad': 1
            }
        else:
            self.carrito[producto_id]['cantidad'] += 1

        self.guardar()

    def eliminar(self, producto):
        producto_id = str(producto.id)

        if producto_id in self.carrito:
            del self.carrito[producto_id]

        self.guardar()

    def sumar(self, producto):
        producto_id = str(producto.id)

        if producto_id in self.carrito:
            self.carrito[producto_id]['cantidad'] += 1

        self.guardar()

    def restar(self, producto):
        producto_id = str(producto.id)

        if producto_id in self.carrito:
            self.carrito[producto_id]['cantidad'] -= 1

            if self.carrito[producto_id]['cantidad'] <= 0:
                self.eliminar(producto)

        self.guardar()

    def obtener_total(self):

        total = 0

        for key, item in self.carrito.items():

            producto = Producto.objects.get(id=key)

            cantidad = item['cantidad']

            precio = float(producto.precio)

            # ESCALAS POR PRODUCTO
            escalas = producto.escalas.all().order_by('cantidad_minima')

            for escala in escalas:
                if cantidad >= escala.cantidad_minima:
                    precio = float(escala.precio)

            subtotal = precio * cantidad

            # Guardar datos para mostrar
            item['precio_actual'] = precio
            item['subtotal'] = round(subtotal, 2)

            total += subtotal

        return round(total, 2)

    def obtener_cantidad_total(self):

        cantidad = 0

        for item in self.carrito.values():
            cantidad += item['cantidad']

        return cantidad

    def guardar(self):
        self.session['carrito'] = self.carrito
        self.session.modified = True


    def actualizar(self, producto, cantidad):

        producto_id = str(producto.id)

        if producto_id in self.carrito:

            self.carrito[producto_id]['cantidad'] = cantidad

        self.guardar()