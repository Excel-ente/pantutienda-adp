import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-z-8vwdxt20k*=r!3(r1r(5*2k391*%!j-5m69op=vfo6z!&=gx'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['127.0.0.1','3.143.128.101','localhost','adelpilar.com.ar','https://adelpilar.com.ar']

CSRF_TRUSTED_ORIGINS = [
    "https://www.adelpilar.com.ar",
    "https://adelpilar.com.ar",
    "http://localhost",
]

# Application definition
INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    #'whitenoise.runserver_nostatic', # agregue aca
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'import_export',
    'front',
    'mensajeria',
    'configuracion',
    'administracion',
    'contabilidad',
    'agenda',
    'compras',
    'fabrica',
    'inventario',
    'pedidos',
    'reportes',
    ]


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware', # agregue aca
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    # Este es mi middelware custom
    'configuracion.middleware.security_middleware.BruteForceProtectionMiddleware',

]

ROOT_URLCONF = 'pantufla.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
            
            ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'pantufla.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'ERROR',  # Puedes cambiar a 'ERROR' si solo quieres registrar errores
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'django_debug_test_new.log'),
            'formatter': 'verbose',  # Usa el formateador 'verbose' para más detalles
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'ERROR',  # Cambia a 'ERROR' para registrar solo errores
            'propagate': True,
        },
    },
}

# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTHENTICATION_LOCKOUT_THRESHOLD = 8 #INTENTOS FALLIDOS PARA BLOQUEAR CUENTA

AUTHENTICATION_LOCKOUT_DURATION = 60 #TIEMPO DE BLOQUEO DE CUENTA

AUTH_PASSWORD_MIN_LENGTH = 8

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {'min_length': 8,},
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]



# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LLANGUAGE_CODE = 'es-ar'

TIME_ZONE = 'America/Argentina/Buenos_Aires'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# settings.py

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

# settings.py

LOGIN_REDIRECT_URL = '/'  # Cambia 'home' por la vista a donde quieras redirigir
LOGOUT_REDIRECT_URL = '/'  # Redirigir después del logout

STATIC_URL = '/static/'
STATIC_ROOT = '/home/ubuntu/aplicaciones/pantutienda-adp/static/'

#STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "staticfiles"),
]

MEDIA_URL = '/media/'
MEDIA_ROOT = '/home/ubuntu/aplicaciones/pantutienda-adp/media/'

DATA_UPLOAD_MAX_NUMBER_FIELDS = 100000

JAZZMIN_SETTINGS = {

    # title of the window (Will default to current_admin_site.site_title if absent or None)
    "site_title": "PantuTienda",

    # Title on the login screen (19 chars max) (defaults to current_admin_site.site_header if absent or None)
    "site_header": "PantuTienda",

    # Title on the brand (19 chars max) (defaults to current_admin_site.site_header if absent or None)
    "site_brand": "PantuTienda",

    # Logo to use for your site, must be present in static files, used for brand on top left
    "site_logo": 'logo_pantu.png',

    # Logo to use for your site, must be present in static files, used for login form logo (defaults to site_logo)
    "login_logo": 'logo.png',

    # Logo to use for login form in dark themes (defaults to login_logo)
    "login_logo_dark": None,

    # CSS classes that are applied to the logo above
    "site_logo_classes": "img-rectangle",

    # Relative path to a favicon for your site, will default to site_logo if absent (ideally 32x32 px)
    "site_icon": 'logo.ico',

    # Welcome text on the login screen
    "welcome_sign": "Bienvenido a PantuTienda",

    # Copyright on the footer
    "copyright": "EXCEL-ENTE",

    # List of model admins to search from the search bar, search bar omitted if excluded
    # If you want to use a single search field you dont need to use a list, you can use a simple string 
    "search_model": [],#'contabilidad.CuentasComerciales'

    # Field name on user model that contains avatar ImageField/URLField/Charfield or a callable that receives the user
    "user_avatar": None,

    ############
    # Top Menu #


    #############
    # User Menu #
    #############

    # Additional links to include in the user menu on the top right ("app" url type is not allowed)
    "usermenu_links": [
        {"name": "Settings", "icon" : "fas fa-users-cog","url": "/app/configuracion/configuracion/1/change/", "new_window": True},
        {"model": "auth.user"},
        {"name": "Support","icon" : "fas fa-exclamation-circle", "url": "https://excel-ente.com", "new_window": True},
    ],


        
    "topmenu_links": [
        {"app": "configuracion", "collapsible": True, "icon": "fas fa-app"},
        {"app": "agenda", "collapsible": True, "icon": "fas fa-app"},
        {"app": "compras", "collapsible": True, "icon": "fas fa-app"},
        {"app": "contabilidad", "collapsible": True, "icon": "fas fa-app"},
        {"app": "inventario", "collapsible": True, "icon": "fas fa-app"},
        {"app": "front", "collapsible": True, "icon": "fas fa-app"},                
    ],
    
    #############
    # Side Menu #
    #############

    # Whether to display the side menu
    "show_sidebar": True,

    # Whether to aut expand the menu
    "navigation_expanded": True,

    # Hide these apps when generating side menu e.g (auth)
    "hide_apps": [
        'auth',
        'configuracion',
        'administracion',
        'contabilidad',
        'agenda',
        'fabrica',
        'reportes',
        'mensajeria',
        'front',
        ],

    # Hide these models when generating side menu (e.g auth.user)
    "hide_models": [
        'auth.group',

        'inventario.ProductoPrecio',
        'inventario.Categoria',
        'inventario.Presentacion',
        'inventario.Deposito',
        'inventario.MovimientoProducto',

        'compra.NotaDeCreditoCompra',
        'venta.NotaDeCreditoVenta',

        'venta.CostosDeVenta',
        'configuracion.configuracion',
        'configuracion.monedas',
        'configuracion.categoria',
        'agenda.Presentacion',
        'configuracion.medioDePago',
        'configuracion.medioDeCompra',
        'venta.costoporventa',
        'producto.productoprecio',
        'producto.productoreceta',
        'producto.presentacion',
        'producto.detalleCompra',
        'producto.detalleVenta',
        "producto.Categoria",
        "producto.ListaDePrecio",
        "producto.MovimientoProducto",
        "tesoreria.movimientoscuenta",
        
        "tesoreria.asientos",
        "tesoreria.PuntoDeVenta",
        "tesoreria.AutorizacionPagoPersonal",
        #"tesoreria.AdelantoProveedor",            
        ],

    # List of apps (and/or models) to base side menu ordering off of (does not need to contain all apps/models)
    "order_with_respect_to": ["pedidos","compras","ventas",],

    # Custom links to append to app groups, keyed on app name
    "custom_links": {
        "books": [{
            "name": "Make Messages", 
            "url": "make_messages", 
            "icon": "fas fa-comments",
            "permissions": ["books.view_book"]
        }]
    },

    # Custom icons for side menu apps/models See https://fontawesome.com/icons?d=gallery&m=free&v=5.0.0,5.0.1,5.0.10,5.0.11,5.0.12,5.0.13,5.0.2,5.0.3,5.0.4,5.0.5,5.0.6,5.0.7,5.0.8,5.0.9,5.1.0,5.1.1,5.2.0,5.3.0,5.3.1,5.4.0,5.4.1,5.4.2,5.13.0,5.12.0,5.11.2,5.11.1,5.10.0,5.9.0,5.8.2,5.8.1,5.7.2,5.7.1,5.7.0,5.6.3,5.5.0,5.4.2
    # for the full list of 5.13.0 free icon classes
    # "icons": {
    #     "auth": "fas fa-users-cog",
    #     "auth.user": "fas fa-user",
    #     "auth.Group": "fas fa-users",
    #     "agenda.Asignacion": "fas fa-user-check",
    #     "agenda.Caja": "fas fa-cash-register",
    #     "agenda.Configuracion": "fas fa-cog",
    #     "agenda.Cliente": "far fa-address-card",
    #     "agenda.Gasto":"fas fa-edit",
    #     "agenda.TipoGasto":"fas fa-project-diagram",
    #     "agenda.Retiro":"far fa-money-bill-alt",
    #     "agenda.Viaje":"fas fa-truck",
    #     "agenda.deposito": "fas fa-city",
    #     "agenda.medioDeCompra":"fas fa-cash-register",
    #     "agenda.medioDePago":"fas fa-wallet",
    #     "agenda.categoria": "fas fa-list",
    #     "agenda.proveedor": "fas fa-users",
    #     "agenda.cliente": "fas fa-user",
    #     "agenda.Chofer": "fas fa-car",
    #     "agenda.PrecioPorKilometro": "fas fa-road",
    #     "agenda.PagoDeCliente": "fas fa-dollar-sign",
    #     "agenda.zonas":"fas fa-map",

    #     "producto.Categoria": "fas fa-tasks",
    #     "producto.Producto": "fas fa-boxes",	
    #     "producto.ProductoPrecio": "fas fa-dollar-sign",
    #     "producto.Merma": "fas fa-exclamation-triangle",
    #     "producto.productoReceta": "fas fa-list",
    #     'producto.movimientoproducto':'fas fa-random',

    #     "compra.medioDePagoCompra": "fas fa-file-invoice-dollar",
    #     "compra.Compra":"fas fa-cart-plus",
    #     "producto.detalleCompra": "fas fa-truck-loading",
    #     "compra.NotaDeCreditoCompra": "fas fa-cart-arrow-down",

    #     "venta.Venta":"fas fa-cash-register",
    #     "venta.DetalleVenta":"far fa-file-alt",   
    #     "venta.PagosVentas":"fas fa-money-bill",
    #     "venta.PagosClientes":"fas fa-wallet",
    #     "venta.EntregaVentas":"fas fa-truck",

    #     "cocina.Receta": "fas fa-book",
    #     "cocina.subReceta": "fas fa-book-open",
    #     "cocina.producto": "fas fa-carrot", 
    #     "cocina.categoria_inventario": "fas fa-list",
    #     "cocina.gastosAdicionales": "fas fa-clipboard-list",  

    #     "contabilidad.Asientos": "fas fa-book",
    #     "contabilidad.Cuentas": "fas fa-house-user",
    #     "contabilidad.CuentasComerciales": "fas fa-id-card",
    #     "contabilidad.movimientoscuenta": "fas fa-list",
    #     "contabilidad.IngresoDinero": "fas fa-plus-circle",
    #     "contabilidad.Trasnferencias": "fas fa-random",
    #     "contabilidad.SolicitudCuentas": "fas fa-file-alt",

    #     "tesoreria.PagoProveedor": "fas fa-money-check-alt",
    #     "tesoreria.PagoCliente": "fas fa-bell",
    #     "tesoreria.AutorizacionPagoPersonal": "fas fa-bell",
    #     "tesoreria.PuntoDeVenta":"fas fa-cash-register",
    #     "tesoreria.AdelantoProveedor":"fas fa-dollar-sign",
    # },

    # Icons that are used when one is not manually specified
    "default_icon_parents": '',
    "default_icon_children": '',

    #################
    # Related Modal #
    #################
    # Use modals instead of popups
    "related_modal_active": False,

    #############
    # UI Tweaks #
    #############
    # Relative paths to custom CSS/JS scripts (must be present in static files)
    "custom_css": None,
    "custom_js": None,
    # Whether to link font from fonts.googleapis.com (use custom_css to supply font otherwise)
    "use_google_fonts_cdn": True,
    # Whether to show the UI customizer on the sidebar
    "show_ui_builder": True,

    ###############
    # Change view #
    ###############
    # Render out the change view as a single form, or in tabs, current options are
    # - single
    # - horizontal_tabs (default)
    # - vertical_tabs
    # - collapsible
    # - carousel
    "changeform_format": "horizontal_tabs",
    # override change forms on a per modeladmin basis
    "changeform_format_overrides": {
        "auth.user": "collapsible", 
        "auth.group": "vertical_tabs",
        "pedidos.Pedido": "single",
        "tesoreria.pagoproveedor": "vertical_tabs",
        "tesoreria.pagocliente": "vertical_tabs",
        "compra.compra": "vertical_tabs",
        "compra.NotaDeCreditoCompra": "vertical_tabs",
        "contabilidad.Asientos": "single",
        "venta.venta": "single",
        },
    # Add a language dropdown into the admin
    "language_chooser": False,
}

JAZZMIN_UI_TWEAKS = {
    "navbar_small_text": True,
    "footer_small_text": False,
    "body_small_text": False,
    "brand_small_text": False,
    "brand_colour": "navbar-seccondary",
    "accent": "accent-seccondary",
    "navbar": "navbar-seccondary navbar-dark",
    "no_navbar_border": False,
    "navbar_fixed": True,
    "layout_boxed": False,
    "footer_fixed": False,
    "sidebar_fixed": True,
    "sidebar": "sidebar-dark-info",
    "sidebar_nav_small_text": True,
    "sidebar_disable_expand": False,
    "sidebar_nav_child_indent": False,
    "sidebar_nav_compact_style": True,
    "sidebar_nav_legacy_style": True,
    "sidebar_nav_flat_style": True,
    "theme": "cosmo",
    "dark_mode_theme": "solar",
    "button_classes": {
        "primary": "btn-outline-primary",
        "secondary": "btn-outline-secondary",
        "info": "btn-outline-info",
        "warning": "btn-outline-warning",
        "danger": "btn-outline-danger",
        "success": "btn-outline-success"
    },
    "actions_sticky_top": True
}



