from django import forms
from .models import configuracion

class ConfiguracionForm(forms.ModelForm):
    class Meta:
        model = configuracion
        fields = [
            'emprendimiento', 'Moneda', 'Moneda_secundaria', 'tipo_cambio_1', 'calculo_rentabilidad',
            'gastos_fletes_compras', 'deposito_central', 'venta_stock_negativo', 'valuar_stock_negativo',
            'precio_venta_automatico', 'unidad_de_medida_precio_venta', 'confirmar_viaje_compra',
            'confirmar_descarga_compra', 'confirmar_pisar_costo', 'editar_fecha_compra', 
            'limite_pedidos_pendientes', 'mail_bienvenida_cliente', 'mail_bienvenida_proveedor',
            'gestionar_armar_pedido', 'gestionar_entrega'
        ]
