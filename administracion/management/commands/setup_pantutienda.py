from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.contrib.auth import get_user_model
from configuracion.models import configuracion, Monedas, medioDeCompra, medioDeVenta
from contabilidad.models import Cuentas
from inventario.models import Deposito, ListaDePrecio

class Command(BaseCommand):
    help = 'Configura el proyecto inicializando la base de datos y creando un superusuario.'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Inicializando la base de datos...'))
        call_command('migrate')
        User = get_user_model()

        # Crear superusuario
        self.stdout.write(self.style.SUCCESS('Creando un superusuario...'))
        if not User.objects.filter(username='EXCEL-ENTE').exists():
            username = 'EXCEL-ENTE'
            email = 'admin@example.com'
            password = 'Pantutienda123.'
            User.objects.create_superuser(username=username, email=email, password=password)
            self.stdout.write(self.style.SUCCESS(f'Superusuario creado: {username} / {password}'))
        else:
            username = 'EXCEL-ENTE'
            self.stdout.write(self.style.WARNING(f'El superusuario ya existe. Usuario {username}'))

        # Crear moneda principal
        if not Monedas.objects.filter(id=1).exists():
            moneda_efectivo = Monedas.objects.create(
                nombre='Efectivo',
                abreviacion='ARS',
                signo='$',
                principal=True,
            )
        else:
            moneda_efectivo = Monedas.objects.get(id=1)

        # Crear deposito general
        if not Deposito.objects.filter(id=1).exists():
            deposito = Deposito.objects.create(
                nombre='Deposito Central',
                direccion='Sin Dirección asignada',
            )
        else:
            deposito = Deposito.objects.get(id=1)

        # Crear configuración inicial usando la instancia de Monedas
        self.stdout.write(self.style.SUCCESS('Verificando configuración inicial...'))
        if not configuracion.objects.filter(id=1).exists():
            configuracion.objects.create(
                emprendimiento='EXCEL-ENTE',
                Moneda=moneda_efectivo,  # Utiliza la instancia de Monedas
                Moneda_secundaria=moneda_efectivo,
                deposito_central=deposito,
            )
            self.stdout.write(self.style.SUCCESS('Configuración inicial creada.'))
        else:
            self.stdout.write(self.style.WARNING('La configuración inicial ya existe.'))

        # Crear cuenta con la moneda asignada
        if not Cuentas.objects.filter(id=1).exists():
            Cuentas.objects.create(
                numero='001',
                moneda=moneda_efectivo,  # Utiliza la instancia de Monedas
                descripcion='Caja Diaria',
                tipo_cuenta='Activo',
            )

        # Crear medios de compra y venta
        if not medioDeCompra.objects.filter(id=1).exists():
            medioDeCompra.objects.create(
                nombre='Efectivo',
                tipo='Efectivo',
            )

        if not medioDeVenta.objects.filter(id=1).exists():
            medioDeVenta.objects.create(
                nombre='Efectivo',
                tipo='Efectivo',
            )

        if not ListaDePrecio.objects.filter(id=1).exists():
            ListaDePrecio.objects.create(
                nombre='Lista General',
            )
