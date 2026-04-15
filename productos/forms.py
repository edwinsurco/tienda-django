from django import forms

class PedidoForm(forms.Form):

    nombre = forms.CharField(
        label="Nombre",
        max_length=100
    )

    telefono = forms.CharField(
        label="Teléfono",
        max_length=20
    )

    direccion = forms.CharField(
        label="Dirección",
        widget=forms.Textarea
    )