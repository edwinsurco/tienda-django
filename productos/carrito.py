from .models import Producto, Cliente, CarritoCliente, ItemCarritoCliente, VarianteProducto


class Carrito:

    def __init__(self, request):
        self.request = request
        self.session = request.session
        carrito = self.session.get('carrito')

        if not carrito:
            carrito = self.session['carrito'] = {}

        self.carrito = carrito
        self.limpiar_invalidos()

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

        nombre_producto = producto.nombre

        if variante_nombre:
            nombre_producto = f"{producto.nombre} - {variante_nombre}"

        if carrito_key not in self.carrito:
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

    def eliminar(self, carrito_key):

        carrito_key = str(carrito_key)

        if carrito_key in self.carrito:
            del self.carrito[carrito_key]

        self.guardar()

    def sumar(self, carrito_key):

        carrito_key = str(carrito_key)

        if carrito_key in self.carrito:
            self.carrito[carrito_key]['cantidad'] += 1

        self.guardar()

    def restar(self, carrito_key):

        carrito_key = str(carrito_key)

        if carrito_key in self.carrito:
            self.carrito[carrito_key]['cantidad'] -= 1

            if self.carrito[carrito_key]['cantidad'] <= 0:
                del self.carrito[carrito_key]

        self.guardar()

    def actualizar(self, carrito_key, cantidad):

        carrito_key = str(carrito_key)

        if carrito_key in self.carrito:
            if cantidad <= 0:
                del self.carrito[carrito_key]
            else:
                self.carrito[carrito_key]['cantidad'] = cantidad

        self.guardar()

    def obtener_cantidad_producto(self, producto_id):

        producto_id = str(producto_id)

        total = 0

        for item in self.carrito.values():
            if str(item.get('producto_id')) == producto_id:
                total += item['cantidad']

        return total

    def obtener_total(self):

        total = 0

        self.limpiar_invalidos()

        for key, item in self.carrito.items():

            producto_id = item.get('producto_id', key)

            producto = Producto.objects.get(id=producto_id)

            cantidad_total_producto = self.obtener_cantidad_producto(producto.id)

            precio = float(producto.precio)

            escalas = producto.escalas.all().order_by(
                'cantidad_minima'
            )

            for escala in escalas:
                if cantidad_total_producto >= escala.cantidad_minima:
                    precio = float(escala.precio)

            subtotal = precio * item['cantidad']

            item['precio_actual'] = precio
            item['subtotal'] = round(subtotal, 2)

            total += subtotal

        return round(total, 2)

    def obtener_cantidad_total(self):

        cantidad = 0

        for item in self.carrito.values():
            cantidad += item['cantidad']

        return cantidad

    def limpiar_invalidos(self):

        cambios = False

        for key in list(self.carrito.keys()):

            producto_id = self.carrito[key].get('producto_id')

            if not producto_id:
                del self.carrito[key]
                cambios = True
                continue

            if not Producto.objects.filter(id=producto_id).exists():
                del self.carrito[key]
                cambios = True

        if cambios:
            self.guardar()

    def guardar(self):
        self.session['carrito'] = self.carrito
        self.session.modified = True
        self.guardar_en_bd_si_logueado()

    def guardar_en_bd_si_logueado(self):

        if not self.request.user.is_authenticated:
            return

        cliente = Cliente.objects.filter(
            user=self.request.user
        ).first()

        if not cliente:
            return

        carrito_bd, creado = CarritoCliente.objects.get_or_create(
            cliente=cliente
        )

        carrito_bd.items.all().delete()

        for key, item in self.carrito.items():

            producto_id = item.get('producto_id')
            variante_id = item.get('variante_id')

            producto = Producto.objects.filter(
                id=producto_id
            ).first()

            if not producto:
                continue

            variante = None

            if variante_id:
                variante = VarianteProducto.objects.filter(
                    id=variante_id
                ).first()

            ItemCarritoCliente.objects.create(
                carrito=carrito_bd,
                producto=producto,
                variante=variante,
                cantidad=item['cantidad']
            )