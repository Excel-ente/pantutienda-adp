import pandas as pd
from django.http import HttpResponse
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from io import BytesIO
from collections import defaultdict

def obtener_datos_reporte(queryset):
    datos_agrupados = defaultdict(lambda: {"cantidad_solicitada": 0, "stock_actual": 0, "unidad_medida": None})

    for pedido in queryset:

        for item in pedido.items.all():

            producto = item.producto
            unidad_base = producto.unidad_de_medida
            unidad_venta = item.producto_precio.unidad_de_medida
            proveedor = producto.proveedor.nombre if producto.proveedor else "Proveedor desconocido"
            cantidad = item.cantidad

            if unidad_base != unidad_venta:
                if unidad_base == 'Kilos' or unidad_base == 'Litros':
                    cantidad = float(cantidad) * float(item.producto_precio.cantidad) / 1000
                elif unidad_base == 'Gramos' or unidad_base == 'Mililitros':
                    cantidad = float(cantidad) * float(item.producto_precio.cantidad) * 1000

                elif unidad_base == 'Mts':
                    cantidad = float(cantidad) * item.producto_precio.cantidad / 100
                elif unidad_base == 'Cms':
                    cantidad = float(cantidad) * float(item.producto_precio.cantidad) * 100

                elif unidad_base == 'Onzas':
                    cantidad = float(cantidad) * float(item.producto_precio.cantidad) / 60

                elif unidad_base == 'Libras':
                    cantidad = float(cantidad) * float(item.producto_precio.cantidad) * 16


            # Clave única por proveedor, producto, y unidad base
            key = (proveedor, producto.codigo, producto.nombre, unidad_base)

            # Agregar la cantidad convertida a la unidad base
            datos_agrupados[key]["cantidad_solicitada"] += float(cantidad)
            datos_agrupados[key]["stock_actual"] = producto.stock_actual  # Stock actual también en la unidad base
            datos_agrupados[key]["unidad_medida"] = unidad_base

    # Convertir a lista de diccionarios para el reporte
    datos = []
    for (proveedor, codigo, nombre, unidad_base), valores in datos_agrupados.items():
        diferencia = float(valores["stock_actual"]) - float(valores["cantidad_solicitada"])
        estado_stock = "OK" if diferencia >= 0 else f"Falta {abs(diferencia)}"

        datos.append({
            "Proveedor": proveedor,
            "Código": codigo,
            "Nombre": nombre,
            "Unidad de Medida": unidad_base,
            "Stock solicitado": valores["cantidad_solicitada"],
            "Stock actual": valores["stock_actual"],
            "Diferencia": diferencia,
            "Estado stock": estado_stock,
        })

    return datos

# Acción para exportar a Excel
def exportar_a_excel(modeladmin, request, queryset):
    datos = obtener_datos_reporte(queryset)
    df = pd.DataFrame(datos)

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="reporte_pedidos.xlsx"'
    df.to_excel(response, index=False)
    return response

# Acción para exportar a PDF
def exportar_a_pdf(modeladmin, request, queryset):
    datos = obtener_datos_reporte(queryset)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="reporte_pedidos.pdf"'

    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=A4)
    pdf.setFont("Helvetica", 12)

    y = 800  # Altura inicial en el PDF
    for item in datos:
        texto = f"Código: {item['Código']} | Nombre: {item['Nombre']} | Solicitado: {item['Stock solicitado']} | " \
                f"Actual: {item['Stock actual']} | Diferencia: {item['Diferencia']} | Estado: {item['Estado stock']}"
        pdf.drawString(30, y, texto)
        y -= 20
        if y < 50:  # Si queda poco espacio en la página, agrega una nueva
            pdf.showPage()
            y = 800

    pdf.save()
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response
