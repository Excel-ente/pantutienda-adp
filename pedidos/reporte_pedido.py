import pandas as pd
from django.http import HttpResponse
from reportlab.lib.pagesizes import landscape, A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from io import BytesIO
from collections import defaultdict

# Función para obtener los datos agrupados
def obtener_datos_reporte(queryset):
    datos_agrupados = defaultdict(lambda: {
        "cantidad_solicitada": 0,
        "stock_actual": 0,
        "unidad_medida": None,
        "ultimo_costo": 0,
        "subtotal": 0,
        "rentabilidad": 0 
    })

    for pedido in queryset:
        for item in pedido.items.all():
            producto = item.producto
            unidad_base = producto.unidad_de_medida
            unidad_venta = item.producto_precio.unidad_de_medida
            proveedor = producto.proveedor if producto.proveedor else "Proveedor desconocido"
            cantidad = item.cantidad

            # Conversiones de unidad
            if unidad_base != unidad_venta:
                if unidad_base in ['Kilos', 'Litros']:
                    cantidad = float(cantidad) * float(item.producto_precio.cantidad) / 1000
                elif unidad_base in ['Gramos', 'Mililitros']:
                    cantidad = float(cantidad) * float(item.producto_precio.cantidad) * 1000
                elif unidad_base == 'Mts':
                    cantidad = float(cantidad) * item.producto_precio.cantidad / 100
                elif unidad_base == 'Cms':
                    cantidad = float(cantidad) * float(item.producto_precio.cantidad) * 100
                elif unidad_base == 'Onzas':
                    cantidad = float(cantidad) * float(item.producto_precio.cantidad) / 60
                elif unidad_base == 'Libras':
                    cantidad = float(cantidad) * float(item.producto_precio.cantidad) * 16

            key = (proveedor, producto.codigo, producto.nombre, unidad_base)
            costo_unit = float(item.producto.costo_unitario)
            precio_unit_venta = item.producto_precio.precio_unitario_calculado()  # Precio de venta calculado
            subtotal = costo_unit * float(cantidad)
            rentabilidad_unitaria = precio_unit_venta - costo_unit

            # Actualizar datos agrupados
            datos_agrupados[key]["cantidad_solicitada"] += cantidad
            datos_agrupados[key]["stock_actual"] = producto.stock_actual
            datos_agrupados[key]["unidad_medida"] = unidad_base
            datos_agrupados[key]["ultimo_costo"] = costo_unit
            datos_agrupados[key]["subtotal"] += subtotal
            datos_agrupados[key]["rentabilidad"] += rentabilidad_unitaria * cantidad

    # Convertir a lista de diccionarios para el reporte
    datos = []
    for (proveedor, codigo, nombre, unidad_base), valores in datos_agrupados.items():
        diferencia = float(valores["stock_actual"]) - float(valores["cantidad_solicitada"])
        estado_stock = "OK" if diferencia >= 0 else f"Falta {abs(round(diferencia,2))}"

        datos.append({
            "Proveedor": proveedor,
            "Código": codigo,
            "Nombre": nombre,
            "Unidad de Medida": unidad_base,
            "Solicitado": round(valores["cantidad_solicitada"],2),
            "Disponible": round(valores["stock_actual"],2),
            "Diferencia": round(diferencia,2),
            "Estado stock": estado_stock,
            "Último Costo": round(valores["ultimo_costo"],2),
            "Subtotal": round(valores["subtotal"],2),
            "Ganancias Estimadas": round(valores["rentabilidad"], 2)  # Nueva columna de rentabilidad
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


def exportar_a_pdf(modeladmin, request, queryset):
    datos = obtener_datos_reporte(queryset)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="reporte_pedidos.pdf"'

    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=landscape(A4))
    elements = []
    styles = getSampleStyleSheet()

    # Agrupar datos por proveedor
    datos_por_proveedor = defaultdict(list)
    for item in datos:
        datos_por_proveedor[item["Proveedor"]].append(item)

    # Crear una tabla por cada proveedor
    for proveedor, items in datos_por_proveedor.items():
        elements.append(Paragraph(f"Productos a comprar al proveedor: {proveedor}", styles['Heading2']))
        
        # Encabezado de la tabla
        data = [
            ["Código", "Descripción", "Solicitado", "Disponible", "Diferencia", "Estado", "Último Costo", "Subtotal", "Ganancias Estimadas"]
        ]
        
        total_inversion = 0
        total_sin_stock = 0
        total_rentabilidad = 0

        for item in items:
            total_sin_stock += item["Último Costo"] * item["Diferencia"] if item["Diferencia"] < 0 else 0
            total_inversion += item["Subtotal"] + total_sin_stock
            total_rentabilidad += item["Ganancias Estimadas"]

            data.append([
                item["Código"],
                item["Nombre"],
                f"{item['Solicitado']} {item['Unidad de Medida']}",
                item["Disponible"],
                item["Diferencia"],
                item["Estado stock"],
                f"${item['Último Costo']:,.2f}",
                f"${item['Subtotal']:,.2f}",
                f"${item['Ganancias Estimadas']:,.2f}"
            ])

        # Totales
        data.append(["", "", "", "", "", "","", "", "",])
        data.append(["", "", "", "", "", "","", "Inversión total", f"${total_inversion:,.2f}"])
        data.append(["", "", "", "", "", "","", "Inversión extra", f"${total_sin_stock:,.2f}"])
        data.append(["", "", "", "", "", "","", "Ganancias esperadas", f"${total_rentabilidad:,.2f}"])
        

        # Crear y agregar la tabla al PDF
        table = Table(data, colWidths=[1*inch, 2*inch, 1.2*inch, 1*inch, 1*inch, 1*inch, 1*inch, 1.5*inch, 1.5*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
        ]))

        elements.append(table)
        elements.append(Paragraph("<br/>", styles['Normal']))

    # Construir el PDF
    doc.build(elements)
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response

