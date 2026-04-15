from django.contrib import admin

from .models import (
    Producto,
    Categoria,
    EscalaPrecio,
    Pedido,
    DetallePedido
)

# INLINE ESCALAS

class EscalaPrecioInline(admin.TabularInline):

    model = EscalaPrecio

    extra = 1


# ADMIN PRODUCTOS

class ProductoAdmin(admin.ModelAdmin):

    list_display = (
        'nombre',
        'precio',
        'categoria'
    )

    inlines = [
        EscalaPrecioInline
    ]


# INLINE DETALLES PEDIDO

class DetallePedidoInline(admin.TabularInline):

    model = DetallePedido

    extra = 0

    readonly_fields = (
        'producto',
        'cantidad',
        'precio',
        'subtotal'
    )


# ADMIN PEDIDOS (MUY IMPORTANTE)

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


# REGISTROS

admin.site.register(
    Producto,
    ProductoAdmin
)

admin.site.register(Categoria)

admin.site.register(
    Pedido,
    PedidoAdmin
)