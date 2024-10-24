from django.db import models
from django.core.exceptions import ValidationError

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
    category_1 = models.CharField(max_length=200, null=True, blank=False)
    category_1_image = models.ImageField(
            upload_to='img/landing/',
            blank=True,
            null=True,
        )
    category_2 = models.CharField(max_length=200, null=True, blank=False)
    category_2_image = models.ImageField(
            upload_to='img/landing/',
            blank=True,
            null=True,
        )
    category_3 = models.CharField(max_length=200, null=True, blank=False)
    category_3_image = models.ImageField(
            upload_to='img/landing/',
            blank=True,
            null=True,
        )
    category_4 = models.CharField(max_length=200, null=True, blank=False)
    category_4_image = models.ImageField(
            upload_to='img/landing/',
            blank=True,
            null=True,
        )

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


    class Meta:
        verbose_name = 'pagina'
        verbose_name_plural ='🖥️ Website'


class Section(models.Model):
    SECTION_CHOICES = [
        ('section_hero', 'Hero Section'),
        ('section_category', 'Category Section'),
        ('section_gallery', 'Gallery Section'),
        ('about_us', 'About Us Section'),
        ('testimonials', 'Testimonials Section'),
        ('features', 'Features Section'),
        ('cta_section', 'Call to Action Section'),
        ('newsletter', 'Newsletter Section')
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
