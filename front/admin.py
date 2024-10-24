from django.contrib import admin
from .models import Landing, Section
from django.utils.html import format_html

class SectionInline(admin.TabularInline):
    model = Section
    extra = 1  # Permitir agregar más secciones


class LandingAdmin(admin.ModelAdmin):
    list_display = ('nombre','section_hero','section_category','section_gallery','about_us','testimonials','features','cta_section','newsletter')
    inlines = [SectionInline,]
    fieldsets = (
        ('Hero Section', {
            'fields': ('section_hero', 'hero_background_image', 'hero_title', 'hero_description'),
            'classes': ('collapse',),
        }),
        ('Category Section', {
            'fields': ('section_category', 'category_1', 'category_1_image', 'category_2', 'category_2_image', 
                       'category_3', 'category_3_image', 'category_4', 'category_4_image'),
            'classes': ('collapse',),
        }),
        ('Gallery Section', {
            'fields': ('section_gallery', 'gallery_1_image', 'gallery_titulo_1', 'gallery_descripcion_1', 
                       'gallery_2_image', 'gallery_titulo_2', 'gallery_descripcion_2', 'gallery_3_image', 
                       'gallery_titulo_3', 'gallery_descripcion_3', 'gallery_4_image', 'gallery_titulo_4', 
                       'gallery_descripcion_4', 'gallery_5_image', 'gallery_titulo_5', 'gallery_descripcion_5',
                       'gallery_6_image', 'gallery_titulo_6', 'gallery_descripcion_6'),
            'classes': ('collapse',),
        }),
        ('About Us Section', {
            'fields': ('about_us', 'about_us_title', 'about_us_image', 'about_us_text_1', 'about_us_text_2', 'about_us_text_3'),
            'classes': ('collapse',),
        }),
        ('Testimonials Section', {
            'fields': ('testimonials', 'testimonials_title', 'comment_1', 'name_comment_1', 'comment_2', 'name_comment_2', 'comment_3', 'name_comment_3'),
            'classes': ('collapse',),
        }),
        ('Features Section', {
            'fields': ('features', 'features_title', 'features_icon_1', 'features_subtitle_1', 'features_text_1', 
                       'features_icon_2', 'features_subtitle_2', 'features_text_2', 'features_icon_3', 'features_subtitle_3', 'features_text_3'),
            'classes': ('collapse',),
        }),
        ('CTA Section', {
            'fields': ('cta_section', 'cta_title', 'cta_text', 'cta_btn_label', 'cta_btn_url'),
            'classes': ('collapse',),
        }),
        ('Newsletter Section', {
            'fields': ('newsletter', 'newsletter_title', 'newsletter_text', 'newsletter_btn_label'),
            'classes': ('collapse',),
        }),
    )

    class Media:
        js = ('js/landing_admin.js',)  # Incluye tu archivo JavaScript

    def has_delete_permission(self, request, obj=None):
        return False
    
admin.site.register(Landing, LandingAdmin)

