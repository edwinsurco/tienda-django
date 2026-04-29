from django import forms

class PedidoForm(forms.Form):

    dni_ruc = forms.CharField(
        label="DNI o RUC",
        max_length=20
    )

    nombre_razon_social = forms.CharField(
        label="Nombre o Razón Social",
        max_length=200
    )

    celular = forms.CharField(
        label="Celular",
        max_length=20
    )

    direccion = forms.CharField(
        label="Dirección",
        widget=forms.Textarea
    )

    correo = forms.EmailField(
        label="Correo",
        required=False
    )