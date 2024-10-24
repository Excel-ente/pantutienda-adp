from django.db.models import Sum

def obtener_saldo_cuenta(id_cuenta):
    """
    Calcula el saldo de una cuenta específica.
    :param id_cuenta: ID de la cuenta para la cual calcular el saldo.
    :return: Saldo de la cuenta.
    """
    from .models import MovimientosCuentaContable

    movimientos = MovimientosCuentaContable.objects.filter(cuenta=id_cuenta)
    total_debe = movimientos.aggregate(Sum('debe'))['debe__sum'] or 0
    total_haber = movimientos.aggregate(Sum('haber'))['haber__sum'] or 0
    saldo = total_debe - total_haber
    
    return saldo


def obtener_saldo_cuenta_comercial(id_cuenta):
    """
    Calcula el saldo de una cuenta específica.
    :param id_cuenta: ID de la cuenta para la cual calcular el saldo.
    :return: Saldo de la cuenta.
    """
    from .models import MovimientosCuentaComercial

    movimientos = MovimientosCuentaComercial.objects.filter(cuenta=id_cuenta)
    total_debe = movimientos.aggregate(Sum('debe'))['debe__sum'] or 0
    total_haber = movimientos.aggregate(Sum('haber'))['haber__sum'] or 0
    saldo = total_debe - total_haber

    return saldo

