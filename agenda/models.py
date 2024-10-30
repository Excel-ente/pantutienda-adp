from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User


def validate_image_size(value):
    '''
        metodo para validar que el logo sea de 500x500
    '''
    width, height = value.width, value.height
    if width != 500 or height != 500:
        raise ValidationError('La imagen debe ser de 500x500 píxeles.')


# -----------------------------------------------------------------------------
# Metodos para acceder a los valores de forma dinamica
# vendedor.clientes_asociados()    ---> Devuelve la cantidad de clientes asociados al vendedor
# vendedor.pedidos_finalizados()    ---> Devuelve la cantidad de pedidos finalizados de clientes asociados al vendedor
# cliente.pedidos_encurso()    ---> Devuelve la cantidad de pedidos en curso de clientes asociados al vendedor
# vendedor.pedidos_pendientes()    ---> Devuelve la cantidad de pedidos pendientes de clientes asociados al vendedor

class Vendedor(models.Model):
    usuario = models.ForeignKey(User,on_delete=models.CASCADE,blank=False,null=False)
    nombre = models.CharField(max_length=120, null=False, blank=False)
    apellido = models.CharField(max_length=120, null=False, blank=False)
    habilitado = models.BooleanField(default=False)
    fecha_habilitacion = models.DateTimeField(blank=True, null=True)
    
    def __str__(self):
        return f'{self.usuario.username}'
    
    class Meta:
        verbose_name = 'vendedor'
        verbose_name_plural ='🪪 Vendedores' 

    def estado_cuenta(self):
        from contabilidad.models import CuentasComerciales
        cuenta = CuentasComerciales.objects.filter(vendedor=self).first()
        if cuenta:
            return f'{cuenta.saldo_actual:,.2f}'
        else:
            return f'Sin cuenta asignada'

    def clientes_asociados():
        # Falta armar funcion
        pass

    def pedidos_encurso():
        # Falta armar funcion
        pass

    def pedidos_finalizados():
        # Falta armar funcion
        pass

    def pedidos_pendientes():
        # Falta armar funcion
        pass


# -----------------------------------------------------------------------------
# Metodos para acceder a los valores de forma dinamica
# cliente.pedidos_encurso()    ---> Devuelve la cantidad de pedidos en curso
# cliente.pedidos_finalizados()    ---> Devuelve la cantidad de pedidos finalizados
# cliente.pedidos_pendientes()    ---> Devuelve la cantidad de pedidos pendientes
class Chofer(models.Model):
    usuario = models.ForeignKey(User,on_delete=models.CASCADE,blank=False,null=False,verbose_name='Chofer')
    habilitado = models.BooleanField(default=False)
    fecha_habilitacion = models.DateTimeField(blank=True, null=True)

    class Meta:
        verbose_name = 'chofer'  # Como se va a nombrar el objeto de la instancia
        verbose_name_plural ='🧑🏻‍🔧 Chofer' # Como se nombra el modelo

    def estado_cuenta(self):
        from contabilidad.models import CuentasComerciales
        cuenta = CuentasComerciales.objects.filter(chofer=self).first()
        if cuenta:
            return f'{cuenta.saldo_actual:,.2f}'
        else:
            return f'Sin cuenta asignada'

    def clean(self):
        super().clean()

    def __str__(self):
        return f'{self.usuario.username}'
    
# -----------------------------------------------------------------------------
# Metodos para acceder a los valores de forma dinamica
# cliente.pedidos_encurso()    ---> Devuelve la cantidad de pedidos en curso
# cliente.pedidos_finalizados()    ---> Devuelve la cantidad de pedidos finalizados
# cliente.pedidos_pendientes()    ---> Devuelve la cantidad de pedidos pendientes
class Cliente(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    codigo = models.CharField(verbose_name="documento",unique=True,max_length=200, null=True, blank=False)
    nombre_apellido = models.CharField(max_length=200, null=True, blank=False)
    telefono = models.CharField(max_length=20,default=1,blank=True,null=True)
    vendedor = models.ForeignKey(Vendedor,on_delete=models.CASCADE,blank=True,null=True,verbose_name="Vendedor asignado")
    tipo_cliente = models.ForeignKey('configuracion.TipoCliente',on_delete=models.SET_NULL,default=1,blank=True,null=True)
    cuit = models.CharField(max_length=255,blank=True,null=True)
    lista_de_precio = models.ForeignKey('configuracion.ListaDePrecio',on_delete=models.CASCADE,blank=True,null=True,verbose_name="Lista de Precio Asignada",help_text="Si no se asigna lista, el usuario no podrá ver ningun producto para solicitar.")
    
    habilitado = models.BooleanField(default=False)
    fecha_alta = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    fecha_habilitacion = models.DateTimeField(blank=True, null=True)

    habilitar_cc = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'cliente'
        verbose_name_plural ='🧑‍💼 Clientes'


    def clean(self):
        super().clean()

    def __str__(self):
        return f'{str(self.nombre_apellido).upper()}'
    
    def pedidos_encurso():
        # Falta armar funcion
        pass

    def pedidos_finalizados():
        # Falta armar funcion
        pass

    def pedidos_pendientes():
        # Falta armar funcion
        pass
    
# -----------------------------------------------------------------------------
# Metodos para acceder a los valores de forma dinamica
# proveedor.compras_encurso()    ---> Devuelve la cantidad de compras en curso
# proveedor.compras_finalizados()    ---> Devuelve la cantidad de compras finalizados
# proveedor.compras_pendientes()    ---> Devuelve la cantidad de compras pendientes

class Proveedor(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, null=False)
    fecha_alta = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    fecha_habilitacion = models.DateTimeField(blank=True, null=True)
    habilitado = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.usuario}'

    def clean(self):

        # Validar que no exista ya un proveedor para el mismo usuario
        if Proveedor.objects.filter(usuario=self.usuario).exclude(id=self.id).exists():
            raise ValidationError('Ya existe un proveedor asociado a este usuario')
        
        super().clean()

    def save(self, *args, **kwargs):
        # Llamar al método clean para validar antes de guardar
        self.clean()
        super(Proveedor, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'proveedor'
        verbose_name_plural = '🧑‍🔧 Proveedores'

    def empresa(self):
        empresa = OnboardingProveedor.objects.filter(proveedor=self).first()
        if empresa:
            return empresa.nombre_empresa
        else:
            return 'Sin Empresa Asociada'

    def compras_encurso(self):
        # Falta armar funcion
        pass

    def compras_finalizados(self):
        # Falta armar funcion
        pass

    def compras_pendientes(self):
        # Falta armar funcion
        pass

    def estado_cuenta(self):
        from contabilidad.models import CuentasComerciales
        cuenta = CuentasComerciales.objects.filter(proveedor=self).first()
        if cuenta:
            return f'{cuenta.saldo_actual:,.2f}'
        else:
            return f'Sin cuenta asignada'
        

# -----------------------------------------------------------------------------
# Metodos para acceder a los valores de forma dinamica
class DireccionEntregaCliente(models.Model):
    Cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, null=False, blank=False)
    direccion = models.CharField(max_length=150, null=False, blank=False)
    localidad = models.CharField(max_length=150, blank=False, null=True)
    barrio = models.CharField(max_length=150, null=True, blank=True)
    entre_calle_1 = models.CharField(max_length=150, null=False, blank=True)
    entre_calle_2 = models.CharField(max_length=150, null=False, blank=True)
    hora_desde = models.TimeField(default='09:00:00', null=False, blank=False)
    hora_hasta = models.TimeField(default='18:00:00', null=False, blank=False)
    comentarios = models.CharField(max_length=150, null=False, blank=True)
    pin_maps = models.URLField(max_length=255, null=True, blank=True)
    
    def __str__(self):
        return f'{self.direccion}'

    class Meta:
        verbose_name = 'direccion'
        verbose_name_plural = '🏠 Dirección de Entrega'

# -----------------------------------------------------------------------------
# Metodos para acceder a los valores de forma dinamica
class OnboardingProveedor(models.Model):
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE, related_name='onboardings',blank=False,null=False)  # Relación con Proveedor
    nombre_empresa = models.CharField(max_length=255,blank=False,null=False)
    cuit = models.CharField(max_length=11, verbose_name="CUIT", unique=True)
    direccion = models.CharField(max_length=255, verbose_name="Dirección",blank=False,null=True)
    telefono_contacto = models.CharField(max_length=20, verbose_name="Teléfono de Contacto",blank=False,null=True)
    correo = models.EmailField(blank=True,null=True)
    horario_atencion = models.CharField(max_length=255, verbose_name="Horarios de Atención",blank=True,null=True)
    fecha_solicitud = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Solicitud")
    aprobado = models.BooleanField(default=False, verbose_name="Aprobado")
    pin_maps = models.URLField(max_length=255, null=True, blank=True)

    def __str__(self):
        if self.horario_atencion:
            return f'Direccion: {self.direccion} | Contacto: {self.proveedor} | Empresa: {self.nombre_empresa}'
        else:
            return f'Dir: {self.direccion}'

    class Meta:
        verbose_name = 'empresa'
        verbose_name_plural = '🏭 Empresa'


# -----------------------------------------------------------------------------
# Metodos para acceder a los valores de forma dinamica
# cliente.pedidos_encurso()    ---> Devuelve la cantidad de pedidos en curso
# cliente.pedidos_finalizados()    ---> Devuelve la cantidad de pedidos finalizados
# cliente.pedidos_pendientes()    ---> Devuelve la cantidad de pedidos pendientes
class Flota(models.Model):
    patente = models.CharField(unique=True,max_length=200, null=True, blank=False)
    vehiculo = models.CharField(max_length=200, null=True, blank=False)
    habilitado = models.BooleanField(default=False)
    fecha_habilitacion = models.DateTimeField(blank=True, null=True)

    class Meta:
        verbose_name = 'vehiculo'
        verbose_name_plural ='🛻 Flota Vehiculos' 

    def clean(self):
        super().clean()

    def __str__(self):
        return f'{self.vehiculo} | PAT: {self.patente}'
    