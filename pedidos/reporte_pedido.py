import pandas as pd
from django.http import HttpResponse
from reportlab.lib.pagesizes import landscape, LEGAL
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from io import BytesIO
from collections import defaultdict
from reportlab.lib.pagesizes import landscape, A4
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from io import BytesIO
from django.http import HttpResponse
from collections import defaultdict


# Función para obtener los datos agrupados
def obtener_datos_reporte(queryset):

    datos_agrupados = defaultdict(lambda: {
        "cantidad_solicitada": 0,
        "stock_actual": 0,
        "unidad_medida": None,
        "costo_unitario": 0,
        "subtotal_costo": 0,
        "total_precio_unitario": 0,
        "total_precio_venta": 0,
        "rentabilidad": 0,
        "total_precio_venta": 0,
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
            precio_unit_venta = item.producto_precio.precio_unitario_madre()
            subtotal_costo = costo_unit * float(cantidad)


            datos_agrupados[key]["cantidad_solicitada"] += cantidad
            datos_agrupados[key]["stock_actual"] = float(max(0, producto.stock_actual))  # No contar stock negativo
            datos_agrupados[key]["costo_unitario"] = costo_unit
            datos_agrupados[key]["subtotal_costo"] = subtotal_costo
            datos_agrupados[key]["total_precio_unitario"] = precio_unit_venta
            datos_agrupados[key]["total_precio_venta"] += precio_unit_venta * cantidad
            datos_agrupados[key]["rentabilidad"] += round((precio_unit_venta* cantidad)- subtotal_costo,2)
            datos_agrupados[key]["unidad_medida"] = unidad_base
        

    # Calcular el precio de venta ponderado y organizar los datos
    datos = []
    for (proveedor, codigo, nombre, unidad_base), valores in datos_agrupados.items():
        diferencia = max(0, valores["cantidad_solicitada"] - valores["stock_actual"])
        estado_stock = f"Faltante {abs(round(diferencia, 2))}" if diferencia > 0 else "OK"
        precio_venta_unitario = valores["total_precio_unitario"]
        precio_venta_total = valores["total_precio_venta"]
        
        # Inversión faltante solo para la cantidad faltante
        inversion_faltante = diferencia * valores["costo_unitario"]

        datos.append({
            "Proveedor": proveedor,
            "Código": codigo,
            "Nombre": nombre,
            "Unidad de Medida": unidad_base,
            "Solicitado": round(valores["cantidad_solicitada"], 2),
            "Disponible": round(valores["stock_actual"], 2),
            "Diferencia": round(diferencia, 2),
            "Estado stock": estado_stock,
            "Último Costo": round(valores["costo_unitario"], 2),
            "Costo Total": round(valores["subtotal_costo"], 2),
            "Precio Venta Unitario": round(precio_venta_unitario, 2),
            "Total Pedido": round(precio_venta_total, 2),
          
            "Ganancias Estimadas": round(valores["rentabilidad"], 2),
            "Inversión Faltante": round(inversion_faltante, 2)
        })


    return datos



def exportar_a_excel(modeladmin, request, queryset):
    datos = obtener_datos_reporte(queryset)
    df = pd.DataFrame(datos)

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="reporte_pedidos.xlsx"'
    df.to_excel(response, index=False)
    return response

import zipfile
from io import BytesIO
# Acción para exportar a PDF
def exportar_a_pdf(modeladmin, request, queryset):
    datos = obtener_datos_reporte(queryset)

    # Configurar el ZIP
    zip_buffer = BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        
        # Agrupar datos por proveedor
        datos_por_proveedor = defaultdict(list)
        for item in datos:
            datos_por_proveedor[item["Proveedor"]].append(item)

        for proveedor, items in datos_por_proveedor.items():
            # Crear un buffer para el PDF de cada proveedor
            pdf_buffer = BytesIO()
            doc = SimpleDocTemplate(pdf_buffer, pagesize=landscape(LEGAL), leftMargin=30, rightMargin=30, topMargin=40, bottomMargin=40)
            elements = []
            styles = getSampleStyleSheet()

            title_style = ParagraphStyle(
                'TitleStyle',
                parent=styles['Heading2'],
                fontSize=16,
                spaceAfter=14,
                textColor=colors.HexColor("#1D3557")
            )

            elements.append(Paragraph(f"Productos a comprar al proveedor: {proveedor}", title_style))
            elements.append(Spacer(1, 10))

            # Encabezado de la tabla
            data = [
                ["Código", "Descripción", "Solicitado", "Disponible", "Diferencia", "Estado", "Costo Unitario", "Costo Total", "Precio Venta Unitario", "Total Pedido", "Ganancias Estimadas", "Inversión Faltante"]
            ]

            total_inversion = 0
            total_sin_stock = 0
            total_rentabilidad = 0

            # Datos de cada producto
            for item in items:
                data.append([
                    item["Código"],
                    item["Nombre"],
                    f"{item['Solicitado']} {item['Unidad de Medida']}",
                    item["Disponible"],
                    item["Diferencia"],
                    item["Estado stock"],
                    f"${item['Último Costo']:,.2f}",
                    f"${item['Costo Total']:,.2f}",
                    f"${item['Precio Venta Unitario']:,.2f}",
                    f"${item['Total Pedido']:,.2f}",
                    f"${item['Ganancias Estimadas']:,.2f}",
                    f"${item['Inversión Faltante']:,.2f}"
                ])
                # Acumulación de totales
                total_inversion += item["Costo Total"]
                total_sin_stock += item["Inversión Faltante"]
                total_rentabilidad += item["Ganancias Estimadas"]

            # Configuración de la tabla
            table = Table(data, colWidths=[0.7*inch, 1.5*inch, 0.9*inch, 0.9*inch, 0.9*inch, 1.0*inch, 1.0*inch, 1.1*inch, 1.2*inch, 1.2*inch, 1.5*inch, 1.2*inch])
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 8),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige)
            ]))

            # Añadir la tabla y totales
            elements.append(table)
            elements.append(Spacer(1, 12))
            
            # Agregar los totales como cuadros independientes
            total_texts = [
                f"Inversión total: ${total_inversion:,.2f}",
                f"Inversión extra: ${total_sin_stock:,.2f}",
                f"Ganancias esperadas: ${total_rentabilidad:,.2f}"
            ]
            
            for total in total_texts:
                elements.append(Paragraph(total, styles['Normal']))
            
            # Crear el PDF en el buffer
            doc.build(elements)
            pdf_buffer.seek(0)

            # Guardar el PDF en el archivo ZIP
            pdf_filename = f"{proveedor}.pdf"
            zip_file.writestr(pdf_filename, pdf_buffer.read())

    # Preparar la respuesta como archivo ZIP
    zip_buffer.seek(0)
    response = HttpResponse(zip_buffer, content_type='application/zip')
    response['Content-Disposition'] = 'attachment; filename="reportes_proveedores.zip"'
    
    return response