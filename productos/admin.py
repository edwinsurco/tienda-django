from django.contrib import admin

from .models import (
    Cliente,
    Producto,
    Categoria,
    EscalaPrecio,
    Pedido,
    DetallePedido
)

# =========================
# INLINE ESCALAS
# =========================

class EscalaPrecioInline(admin.TabularInline):

    model = EscalaPrecio
    extra = 1


# =========================
# ADMIN PRODUCTOS
# =========================

class ProductoAdmin(admin.ModelAdmin):

    list_display = (
        'nombre',
        'precio',
        'categoria'
    )

    search_fields = (
        'nombre',
    )

    list_filter = (
        'categoria',
    )

    inlines = [
        EscalaPrecioInline
    ]


# =========================
# INLINE DETALLE PEDIDO
# =========================

class DetallePedidoInline(admin.TabularInline):

    model = DetallePedido
    extra = 0

    readonly_fields = (
        'producto',
        'cantidad',
        'precio',
        'subtotal'
    )


# =========================
# ADMIN PEDIDOS
# =========================

class PedidoAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'nombre',
        'telefono',
        'total',
        'estado',
        'fecha'
    )

    list_filter = (
        'estado',
        'fecha'
    )

    search_fields = (
        'nombre',
        'telefono'
    )

    inlines = [
        DetallePedidoInline
    ]


# =========================
# ADMIN CLIENTES
# =========================

class ClienteAdmin(admin.ModelAdmin):

    list_display = (
        'dni_ruc',
        'nombre_razon_social',
        'celular',
        'correo',
        'fecha_registro'
    )

    search_fields = (
        'dni_ruc',
        'nombre_razon_social',
        'celular'
    )


# =========================
# REGISTROS
# =========================

admin.site.register(
    Cliente,
    ClienteAdmin
)

admin.site.register(
    Producto,
    ProductoAdmin
)

admin.site.register(Categoria)

admin.site.register(
    Pedido,
    PedidoAdmin
)