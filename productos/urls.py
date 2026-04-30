from django.urls import path
from . import views

urlpatterns = [

    path(
        '',
        views.lista_productos,
        name='lista_productos'
    ),

    path(
        'agregar/<int:producto_id>/',
        views.agregar_producto,
        name='agregar_producto'
    ),

    path(
        'eliminar/<str:carrito_key>/',
        views.eliminar_producto,
        name='eliminar_producto'
    ),

    path(
        'sumar/<str:carrito_key>/',
        views.sumar_producto,
        name='sumar_producto'
    ),

    path(
        'restar/<str:carrito_key>/',
        views.restar_producto,
        name='restar_producto'
    ),

    path(
        'actualizar/<str:carrito_key>/',
        views.actualizar_cantidad,
        name='actualizar_cantidad'
    ),

    path(
        'carrito/',
        views.ver_carrito,
        name='ver_carrito'
    ),

    path(
        'categoria/<int:categoria_id>/',
        views.productos_por_categoria,
        name='productos_por_categoria'
    ),

    path(
        'crear-pedido/',
        views.crear_pedido,
        name='crear_pedido'
    ),

    path(
        'pedido-exitoso/<int:pedido_id>/',
        views.pedido_exitoso,
        name='pedido_exitoso'
    ),

    path(
        'consultar-pedido/',
        views.consultar_pedido,
        name='consultar_pedido'
    ),

    path(
        'buscar-cliente/',
        views.buscar_cliente,
        name='buscar_cliente'
    ),


    path(
        'registro/',
        views.registro_cliente,
        name='registro_cliente'
    ),

    path(
        'login/',
        views.login_cliente,
        name='login_cliente'
        ),

    path(
        'logout/',
        views.logout_cliente,
        name='logout_cliente'
        ),
]