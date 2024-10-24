def convertir_unidad(costo, unidad_compra, unidad_destino):
    # Diccionario de conversiones entre unidades
    unit_conversions = {
        'Unidades': 1,
        'Mt2s': 1,

        'Litros': 1,
        'Mililitros': 1000,

        'Kilos': 1,
        'Gramos': 1000,

        'Onzas': 16,  # 1 libra = 16 onzas
        'Libras': 1,  # Las libras se usan como unidad de referencia

        'Mts': 1,
        'Cms': 100,  # 1 metro = 100 centímetros
    }
    
    if unidad_compra == unidad_destino:
        return costo
    else:
        if unidad_compra == 'Gramos' or unidad_compra == 'Mililitros' or unidad_compra == 'Onzas' or unidad_compra == 'Cms':
            return costo * unit_conversions[unidad_compra]
        else:
            return costo / unit_conversions[unidad_destino]
        
        


