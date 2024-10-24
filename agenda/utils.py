from contabilidad.models import CuentasComerciales
from configuracion.models import Monedas

def crear_cuenta_comercial_proveedor(proveedor):

    moneda_utilizada = Monedas.objects.filter(principal=True).first()

    cuenta_ext = CuentasComerciales.objects.filter(proveedor=proveedor).first()
    if not cuenta_ext:
        cuenta = CuentasComerciales.objects.create(
                descripcion=f'Cuenta comercial para emprendimiento: {proveedor.empresa()}',
                moneda=moneda_utilizada,
                proveedor=proveedor
                )

def crear_cuenta_comercial_cliente(cliente):

    moneda_utilizada = Monedas.objects.filter(principal=True).first()

    cuenta_ext = CuentasComerciales.objects.filter(cliente=cliente).first()
    if not cuenta_ext:
        cuenta = CuentasComerciales.objects.create(
                descripcion=f'Cuenta comercial para cliente: #{cliente.id} | {cliente.nombre_apellido}',
                moneda=moneda_utilizada,
                cliente=cliente
                )

def crear_cuenta_comercial_vendedor(vendedor):

    moneda_utilizada = Monedas.objects.filter(principal=True).first()

    cuenta_ext = CuentasComerciales.objects.filter(vendedor=vendedor).first()
    if not cuenta_ext:
        cuenta = CuentasComerciales.objects.create(
                descripcion=f'Cuenta comercial para vendedor: #{vendedor.id} | {vendedor.nombre}',
                moneda=moneda_utilizada,
                vendedor=vendedor
                )
        
def crear_cuenta_comercial_chofer(chofer):

    moneda_utilizada = Monedas.objects.filter(principal=True).first()

    cuenta_ext = CuentasComerciales.objects.filter(chofer=chofer).first()
    if not cuenta_ext:
        cuenta = CuentasComerciales.objects.create(
                descripcion=f'Cuenta comercial para chofer: #{chofer.id} | {chofer.usuario.username}',
                moneda=moneda_utilizada,
                chofer=chofer
                )



