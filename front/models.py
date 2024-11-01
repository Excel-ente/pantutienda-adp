from django.db import models
from django.core.exceptions import ValidationError

from inventario.models import Categoria

class Landing(models.Model):

    nombre = models.CharField(max_length=255, blank=False, null=False, default='pagina_inicio', unique=True)
    sections = models.ManyToManyField('front.Section', related_name="landings")

    section_hero = models.BooleanField(default=False)
    hero_background_image = models.ImageField(
            upload_to='img/landing/',
            blank=True,
            null=True,
        )
    
    hero_title = models.CharField(max_length=200, null=True, blank=False)
    hero_description = models.CharField(max_length=200, null=True, blank=False)

    section_category = models.BooleanField(default=False)
    category_1 = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True, blank=True, related_name="landing_category_1")
    category_2 = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True, blank=True, related_name="landing_category_2")
    category_3 = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True, blank=True, related_name="landing_category_3")
    category_4 = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True, blank=True, related_name="landing_category_4")


    section_gallery = models.BooleanField(default=False)
    gallery_1_image = models.ImageField(upload_to='img/landing/',blank=True,null=True)
    gallery_titulo_1 = models.CharField(max_length=200, null=True, blank=False)
    gallery_descripcion_1 = models.CharField(max_length=200, null=True, blank=False)
    gallery_2_image = models.ImageField(upload_to='img/landing/',blank=True,null=True)
    gallery_titulo_2 = models.CharField(max_length=200, null=True, blank=False)
    gallery_descripcion_2 = models.CharField(max_length=200, null=True, blank=False)
    gallery_3_image = models.ImageField(upload_to='img/landing/',blank=True,null=True)
    gallery_titulo_3 = models.CharField(max_length=200, null=True, blank=False)
    gallery_descripcion_3 = models.CharField(max_length=200, null=True, blank=False)
    gallery_4_image = models.ImageField(upload_to='img/landing/',blank=True,null=True)
    gallery_titulo_4 = models.CharField(max_length=200, null=True, blank=False)
    gallery_descripcion_4 = models.CharField(max_length=200, null=True, blank=False)
    gallery_5_image = models.ImageField(upload_to='img/landing/',blank=True,null=True)
    gallery_titulo_5 = models.CharField(max_length=200, null=True, blank=False)
    gallery_descripcion_5 = models.CharField(max_length=200, null=True, blank=False)
    gallery_6_image = models.ImageField(upload_to='img/landing/',blank=True,null=True)       
    gallery_titulo_6 = models.CharField(max_length=200, null=True, blank=False)
    gallery_descripcion_6 = models.CharField(max_length=200, null=True, blank=False)

    about_us = models.BooleanField(default=False)
    about_us_title = models.CharField(max_length=200, null=True, blank=False)
    about_us_image  = models.ImageField(upload_to='img/landing/',blank=True,null=True) 

    about_us_text_1 = models.CharField(max_length=200, null=True, blank=False)
    about_us_text_2 = models.CharField(max_length=200, null=True, blank=False)
    about_us_text_3 = models.CharField(max_length=200, null=True, blank=False)

    testimonials = models.BooleanField(default=False) 
    testimonials_title = models.CharField(max_length=200, null=True, blank=False)
    comment_1 = models.CharField(max_length=200, null=True, blank=False)
    name_comment_1 = models.CharField(max_length=200, null=True, blank=False)
    comment_2 = models.CharField(max_length=200, null=True, blank=False)
    name_comment_2 = models.CharField(max_length=200, null=True, blank=False)
    comment_3 = models.CharField(max_length=200, null=True, blank=False)
    name_comment_3 = models.CharField(max_length=200, null=True, blank=False)

    features = models.BooleanField(default=False)
    features_title = models.CharField(max_length=200, null=True, blank=False)

    features_icon_1 = models.CharField(max_length=200, null=True, blank=False)
    features_subtitle_1 = models.CharField(max_length=200, null=True, blank=False)
    features_text_1 = models.CharField(max_length=200, null=True, blank=False)

    features_icon_2 = models.CharField(max_length=200, null=True, blank=False)
    features_subtitle_2 = models.CharField(max_length=200, null=True, blank=False)
    features_text_2 = models.CharField(max_length=200, null=True, blank=False)

    features_icon_3 = models.CharField(max_length=200, null=True, blank=False)
    features_subtitle_3 = models.CharField(max_length=200, null=True, blank=False)
    features_text_3 = models.CharField(max_length=200, null=True, blank=False)
    

    cta_section = models.BooleanField(default=False) 
    cta_title = models.CharField(max_length=200, null=True, blank=False)
    cta_text = models.CharField(max_length=200, null=True, blank=False)
    cta_btn_label = models.CharField(max_length=200, null=True, blank=False)
    cta_btn_url = models.CharField(max_length=200, null=True, blank=False)

    newsletter = models.BooleanField(default=False)  
    newsletter_title = models.CharField(max_length=200, null=True, blank=False)
    newsletter_text = models.CharField(max_length=200, null=True, blank=False)
    newsletter_btn_label = models.CharField(max_length=200, null=True, blank=False)

    section_clients = models.BooleanField(default=False)
    clients_title = models.CharField(max_length=200, null=True, blank=False)
    clients_text = models.CharField(max_length=500, null=True, blank=True)
    clients_logo_1 = models.ImageField(upload_to='img/landing/', blank=True, null=True)
    clients_logo_2 = models.ImageField(upload_to='img/landing/', blank=True, null=True)
    clients_logo_3 = models.ImageField(upload_to='img/landing/', blank=True, null=True)
    clients_logo_4 = models.ImageField(upload_to='img/landing/', blank=True, null=True)

    footer_section = models.BooleanField(default=False)
    footer_text = models.CharField(max_length=200, null=True, blank=True)
    footer_icon = models.ImageField(upload_to='img/landing/', blank=True, null=True)
    footer_background_color = models.CharField(
        max_length=7, 
        default="#ffffff",  # Valor por defecto en blanco
        help_text="Color de fondo en formato hexadecimal (ej. #ffffff para blanco)"
    )

    # Nueva sección de banners promocionales
    section_promo_banners = models.BooleanField(default=False)
    banner_1_image = models.ImageField(upload_to='img/landing/', blank=True, null=True)
    banner_1_link = models.URLField(max_length=200, blank=True, null=True)
    banner_2_image = models.ImageField(upload_to='img/landing/', blank=True, null=True)
    banner_2_link = models.URLField(max_length=200, blank=True, null=True)
    banner_3_image = models.ImageField(upload_to='img/landing/', blank=True, null=True)
    banner_3_link = models.URLField(max_length=200, blank=True, null=True)

    # Nueva sección de como trabajamos
    section_how_we_work = models.BooleanField(default=False)
    work_title = models.CharField(max_length=200, null=True, blank=True)
    background_color_hww = models.CharField(
        max_length=7, 
        default="#ffffff",  # Valor por defecto en blanco
        help_text="Color de fondo en formato hexadecimal (ej. #ffffff para blanco)"
    )
    
    step_emoji_1 = models.CharField(max_length=5, null=True, blank=True, default="📞")
    step_title_1 = models.CharField(max_length=100, null=True, blank=True, default="Realiza tu Pedido")
    step_description_1 = models.TextField(null=True, blank=True, default="Llámanos o envíanos un mensaje con tu pedido.")

    step_emoji_2 = models.CharField(max_length=5, null=True, blank=True, default="🥕")
    step_title_2 = models.CharField(max_length=100, null=True, blank=True, default="Preparamos tu Pedido")
    step_description_2 = models.TextField(null=True, blank=True, default="Seleccionamos las verduras frescas que solicitaste.")

    step_emoji_3 = models.CharField(max_length=5, null=True, blank=True, default="✅")
    step_title_3 = models.CharField(max_length=100, null=True, blank=True, default="Confirmación")
    step_description_3 = models.TextField(null=True, blank=True, default="Te enviamos la confirmación de tu pedido.")

    step_emoji_4 = models.CharField(max_length=5, null=True, blank=True, default="🚚")
    step_title_4 = models.CharField(max_length=100, null=True, blank=True, default="Entrega")
    step_description_4 = models.TextField(null=True, blank=True, default="Realizamos la entrega a domicilio martes y jueves.")


    class Meta:
        verbose_name = 'pagina'
        verbose_name_plural ='🖥️ Website'


class Section(models.Model):
    SECTION_CHOICES = [
        ('section_hero', 'Hero Section'),
        ('section_category', 'Category Section'),
        ('banner', 'Banner'),
        ('section_gallery', 'Gallery Section'),
        ('about_us', 'About Us Section'),
        ('testimonials', 'Testimonials Section'),
        ('features', 'Features Section'),
        ('cta_section', 'Call to Action Section'),
        ('como_trabajamos','Como Trabajamos'),
        ('newsletter', 'Newsletter Section'),
        ('section_clients', 'Nuestros Clientes Section'),
        ('footer', 'Footer Section'),
    ]

    name = models.CharField(max_length=255, choices=SECTION_CHOICES)
    order = models.PositiveIntegerField(default=0)  # Define el orden de las secciones
    is_active = models.BooleanField(default=True)  # Activa/desactiva la sección
    landing = models.ForeignKey(Landing, on_delete=models.CASCADE, related_name="section_set")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'orden'
        verbose_name_plural ='🕌 Orden de Secciones'

class CategoryOrder(models.Model):
    landing = models.ForeignKey(Landing, on_delete=models.CASCADE, related_name="category_order_set")
    category = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = "orden de categoría"
        verbose_name_plural = "Orden de Categorías"
        ordering = ['order']  

    def __str__(self):
        return f"{self.category} - Orden: {self.order}"