from .models import Producto


class Carrito:

    def __init__(self, request):
        self.session = request.session
        carrito = self.session.get('carrito')

        if not carrito:
            carrito = self.session['carrito'] = {}

        self.carrito = carrito

    def agregar(self, producto, variante=None):

    producto_id = str(producto.id)

    variante_id = ""

    variante_nombre = ""

    if variante:

        variante_id = str(variante.id)
        variante_nombre = variante.nombre

    carrito_key = producto_id

    if variante_id:

        carrito_key = f"{producto_id}_{variante_id}"

    if carrito_key not in self.carrito:

        nombre_producto = producto.nombre

        if variante_nombre:

            nombre_producto = f"{producto.nombre} - {variante_nombre}"

        self.carrito[carrito_key] = {
            'producto_id': producto_id,
            'variante_id': variante_id,
            'nombre': nombre_producto,
            'precio': float(producto.precio),
            'cantidad': 1
        }

    else:

        self.carrito[carrito_key]['cantidad'] += 1

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

        producto = Producto.objects.get(
            id=item.get('producto_id', key)
        )

        cantidad = item['cantidad']

        precio = float(producto.precio)

        escalas = producto.escalas.all().order_by(
            'cantidad_minima'
        )

        for escala in escalas:

            if cantidad >= escala.cantidad_minima:
                precio = float(escala.precio)

        subtotal = precio * cantidad

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