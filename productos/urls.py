from django.urls import path
from . import views

urlpatterns = [

    path('', views.lista_productos, name='lista_productos'),

    path('agregar/<int:producto_id>/',
         views.agregar_producto,
         name='agregar_producto'),

    path('eliminar/<int:producto_id>/',
         views.eliminar_producto,
         name='eliminar_producto'),

    path('sumar/<int:producto_id>/',
         views.sumar_producto,
         name='sumar_producto'),

    path('restar/<int:producto_id>/',
         views.restar_producto,
         name='restar_producto'),

    path('carrito/',
         views.ver_carrito,
         name='ver_carrito'),
    path('categoria/<int:categoria_id>/',
    views.productos_por_categoria,
    name='productos_por_categoria'),
    
    path(
    'crear-pedido/',
    views.crear_pedido,
    name='crear_pedido'),

    path(
    'pedido-exitoso/<int:pedido_id>/',
    views.pedido_exitoso,
    name='pedido_exitoso'),

    path(
    'actualizar/<int:producto_id>/',
    views.actualizar_cantidad,
    name='actualizar_cantidad'),

    path(
    'consultar-pedido/',
    views.consultar_pedido,
    name='consultar_pedido'),

]