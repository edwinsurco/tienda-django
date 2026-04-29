from django.shortcuts import render, redirect, get_object_or_404
from .forms import PedidoForm
from urllib.parse import quote
from .models import Pedido, DetallePedido
import urllib.parse
from .models import Pedido
from django.http import JsonResponse
from .models import Cliente

from .models import (
    Producto,
    Categoria,
    Pedido,
    DetallePedido
)
from .carrito import Carrito



def lista_productos(request):

    carrito = Carrito(request)

    categorias = Categoria.objects.all()

    productos = Producto.objects.all()

    # BUSCADOR

    buscar = request.GET.get("buscar")

    if buscar:

        productos = productos.filter(
            nombre__icontains=buscar
        )

    carrito_data = carrito.carrito

    # PRECIOS ESCALONADOS

    for producto in productos:

        producto_id = str(producto.id)

        cantidad = 0

        if producto_id in carrito_data:
            cantidad = carrito_data[producto_id]['cantidad']

        precio = float(producto.precio)

        escalas = producto.escalas.all().order_by(
            'cantidad_minima'
        )

        for escala in escalas:

            if cantidad >= escala.cantidad_minima:
                precio = float(escala.precio)

        producto.precio_actual = precio
        producto.cantidad_en_carrito = cantidad

        # NUEVO: detectar si hay descuento
        precio_original = float(producto.precio)
        if precio < precio_original:
           producto.tiene_descuento = True
        else:
           producto.tiene_descuento = False

    context = {

        'productos': productos,

        'categorias': categorias,

        'categoria_actual': None,  # IMPORTANTE

        'buscar': buscar

    }

    return render(
        request,
        'productos/lista_productos.html',
        context
    )


def agregar_producto(request, producto_id):

    carrito = Carrito(request)

    producto = get_object_or_404(
        Producto,
        id=producto_id
    )

    carrito.agregar(producto)

    return redirect(request.META.get('HTTP_REFERER', '/'))


def eliminar_producto(request, producto_id):

    carrito = Carrito(request)

    producto = get_object_or_404(
        Producto,
        id=producto_id
    )

    carrito.eliminar(producto)

    return redirect(request.META.get('HTTP_REFERER', '/'))


def sumar_producto(request, producto_id):

    carrito = Carrito(request)

    producto = get_object_or_404(
        Producto,
        id=producto_id
    )

    carrito.sumar(producto)

    return redirect(request.META.get('HTTP_REFERER', '/'))


def restar_producto(request, producto_id):

    carrito = Carrito(request)

    producto = get_object_or_404(
        Producto,
        id=producto_id
    )

    carrito.restar(producto)

    return redirect(request.META.get('HTTP_REFERER', '/'))

def ver_carrito(request):

    carrito = Carrito(request)

    context = {

        'carrito': carrito.carrito,

        'total': carrito.obtener_total(),

    }

    return render(
        request,
        'productos/carrito.html',
        context
    )
def productos_por_categoria(request, categoria_id):

    carrito = Carrito(request)

    categorias = Categoria.objects.all()

    categoria_actual = Categoria.objects.get(
        id=categoria_id
    )

    productos = Producto.objects.filter(
        categoria=categoria_actual
    )

    # BUSCADOR DENTRO DE CATEGORIA

    buscar = request.GET.get("buscar")

    if buscar:

        productos = productos.filter(
            nombre__icontains=buscar
        )

    carrito_data = carrito.carrito

    # PRECIOS ESCALONADOS

    for producto in productos:

        producto_id = str(producto.id)

        cantidad = 0

        if producto_id in carrito_data:
            cantidad = carrito_data[producto_id]['cantidad']

        precio = float(producto.precio)

        escalas = producto.escalas.all().order_by(
            'cantidad_minima'
        )

        for escala in escalas:

            if cantidad >= escala.cantidad_minima:
                precio = float(escala.precio)

        producto.precio_actual = precio
        producto.cantidad_en_carrito = cantidad

        # NUEVO: detectar si hay descuento
        precio_original = float(producto.precio)
        if precio < precio_original:
           producto.tiene_descuento = True
        else:
           producto.tiene_descuento = False

    context = {

        'productos': productos,

        'categorias': categorias,

        'categoria_actual': categoria_actual,

        'buscar': buscar

    }

    return render(
        request,
        'productos/lista_productos.html',
        context
    )


def crear_pedido(request):

    carrito = Carrito(request)

    if request.method == "POST":

        form = PedidoForm(request.POST)

        if form.is_valid():

            dni_ruc = form.cleaned_data['dni_ruc']
            nombre = form.cleaned_data['nombre_razon_social']
            telefono = form.cleaned_data['celular']
            direccion = form.cleaned_data['direccion']
            correo = form.cleaned_data['correo']

            cliente, creado = Cliente.objects.update_or_create(
                dni_ruc=dni_ruc,
                defaults={
                    'nombre_razon_social': nombre,
                    'celular': telefono,
                    'direccion': direccion,
                    'correo': correo
                }
            )

            pedido = Pedido.objects.create(
                cliente=cliente,
                nombre=nombre,
                telefono=telefono,
                direccion=direccion,
                total=carrito.obtener_total()
            )

            mensaje = f"Pedido nuevo:%0A%0A"
            mensaje += f"{nombre}%0A"
            mensaje += f"{telefono}%0A"
            mensaje += f"{direccion}%0A%0A"
            mensaje += "Productos:%0A"

            for key, item in carrito.carrito.items():

                DetallePedido.objects.create(
                    pedido=pedido,
                    producto_id=key,
                    cantidad=item['cantidad'],
                    precio=item['precio_actual'],
                    subtotal=item['subtotal']
                )

                mensaje += f"{item['nombre']} x {item['cantidad']}%0A"

            mensaje += f"%0ATotal: S/ {carrito.obtener_total()}"

            numero = "51918600550"

            url = f"https://wa.me/{numero}?text={mensaje}"

            request.session['mensaje_whatsapp'] = url
            request.session['carrito'] = {}

            return redirect(
                'pedido_exitoso',
                pedido_id=pedido.id
            )

    else:

        form = PedidoForm()

    return render(
        request,
        'productos/crear_pedido.html',
        {
            'form': form,
            'total': carrito.obtener_total()
        }
    )

def pedido_exitoso(request, pedido_id):

    pedido = Pedido.objects.get(id=pedido_id)

    return render(
        request,
        'productos/pedido_exitoso.html',
        {
            'pedido': pedido
        }
    )

def actualizar_cantidad(request, producto_id):

    if request.method == "POST":

        carrito = Carrito(request)

        cantidad = int(request.POST.get("cantidad"))

        producto = get_object_or_404(
            Producto,
            id=producto_id
        )

        carrito.actualizar(producto, cantidad)

    return redirect('ver_carrito')

def consultar_pedido(request):

    pedido = None
    detalles = None
    error = None

    if request.method == "POST":

        numero = request.POST.get("numero")

        try:

            pedido = Pedido.objects.get(id=numero)

            detalles = DetallePedido.objects.filter(
                pedido=pedido
            )

        except Pedido.DoesNotExist:

            error = "Pedido no encontrado"

    return render(
        request,
        'productos/consultar_pedido.html',
        {
            'pedido': pedido,
            'detalles': detalles,
            'error': error
        }
    )

def buscar_cliente(request):

    dni_ruc = request.GET.get('dni_ruc')

    try:
        cliente = Cliente.objects.get(dni_ruc=dni_ruc)

        data = {
            'existe': True,
            'nombre_razon_social': cliente.nombre_razon_social,
            'celular': cliente.celular,
            'direccion': cliente.direccion,
            'correo': cliente.correo or ''
        }

    except Cliente.DoesNotExist:

        data = {
            'existe': False
        }

    return JsonResponse(data)