from django.db import models
from django.contrib.auth.models import User


class Categoria(models.Model):
    nombre = models.CharField(max_length=100)

    def save(self, *args, **kwargs):
        if self.nombre:
            self.nombre = self.nombre.strip().capitalize()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nombre


class Producto(models.Model):
    nombre = models.CharField(max_length=200)

    precio = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    descripcion = models.TextField(
        blank=True,
        null=True
    )

    imagen = models.ImageField(
        upload_to='productos/',
        null=True,
        blank=True
    )

    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.CASCADE
    )

    stock = models.PositiveIntegerField(
        default=0
    )

    def save(self, *args, **kwargs):
        if self.nombre:
            self.nombre = self.nombre.strip().capitalize()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nombre


class VarianteProducto(models.Model):
    producto = models.ForeignKey(
        Producto,
        on_delete=models.CASCADE,
        related_name='variantes'
    )

    nombre = models.CharField(max_length=100)

    def save(self, *args, **kwargs):
        if self.nombre:
            self.nombre = self.nombre.strip().capitalize()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.producto.nombre} - {self.nombre}"


class EscalaPrecio(models.Model):
    producto = models.ForeignKey(
        Producto,
        on_delete=models.CASCADE,
        related_name='escalas'
    )

    cantidad_minima = models.IntegerField()

    precio = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    def __str__(self):
        return f"{self.producto.nombre} - {self.cantidad_minima}+ unidades"


class Cliente(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    dni_ruc = models.CharField(
        max_length=20,
        unique=True
    )

    nombre_razon_social = models.CharField(
        max_length=200
    )

    celular = models.CharField(
        max_length=20
    )

    direccion = models.TextField()

    correo = models.EmailField(
        blank=True,
        null=True
    )

    fecha_registro = models.DateTimeField(
        auto_now_add=True
    )

    def save(self, *args, **kwargs):
        if self.nombre_razon_social:
            self.nombre_razon_social = self.nombre_razon_social.strip().title()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.nombre_razon_social} - {self.dni_ruc}"


class Pedido(models.Model):
    cliente = models.ForeignKey(
        Cliente,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='pedidos'
    )

    nombre = models.CharField(max_length=100)

    telefono = models.CharField(max_length=20)

    direccion = models.TextField()

    fecha = models.DateTimeField(auto_now_add=True)

    total = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    ESTADOS = [
        ('Pendiente', 'Pendiente'),
        ('Preparacion', 'En preparación'),
        ('Enviado', 'Enviado'),
        ('Entregado', 'Entregado'),
        ('Cancelado', 'Cancelado'),
    ]

    estado = models.CharField(
        max_length=20,
        choices=ESTADOS,
        default='Pendiente'
    )

    def __str__(self):
        return f"Pedido {self.id} - {self.nombre}"


class DetallePedido(models.Model):
    pedido = models.ForeignKey(
        Pedido,
        on_delete=models.CASCADE,
        related_name='detalles'
    )

    producto = models.ForeignKey(
        Producto,
        on_delete=models.CASCADE
    )

    variante = models.ForeignKey(
        VarianteProducto,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    cantidad = models.IntegerField()

    precio = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    subtotal = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    def __str__(self):
        if self.variante:
            return f"{self.producto.nombre} - {self.variante.nombre}"
        return self.producto.nombre


class CarritoCliente(models.Model):
    cliente = models.OneToOneField(
        Cliente,
        on_delete=models.CASCADE,
        related_name='carrito_guardado'
    )

    fecha_actualizacion = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return f"Carrito de {self.cliente.nombre_razon_social}"


class ItemCarritoCliente(models.Model):
    carrito = models.ForeignKey(
        CarritoCliente,
        on_delete=models.CASCADE,
        related_name='items'
    )

    producto = models.ForeignKey(
        Producto,
        on_delete=models.CASCADE
    )

    variante = models.ForeignKey(
        VarianteProducto,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    cantidad = models.PositiveIntegerField(
        default=1
    )

    def __str__(self):
        if self.variante:
            return f"{self.producto.nombre} - {self.variante.nombre} x {self.cantidad}"
        return f"{self.producto.nombre} x {self.cantidad}"