from pathlib import Path
from django.urls import reverse_lazy
from decouple import config
from django.utils.translation import gettext_lazy as _


BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = config('SECRET_KEY')
APP_DOMAIN = 'http://127.0.0.1:8000'
DEBUG = config('DEBUG')
ALLOWED_HOSTS = []
# SECURE_SSL_REDIRECT = False


# Application definition
INSTALLED_APPS = [
    'django.contrib.humanize',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Apps
    'hospital_extentions',
    'hospital_auth.apps.HospitalAuthConfig',
    'hospital_setting.apps.HospitalSettingConfig',
    'hospital_blog.apps.HospitalBlogConfig',
    'hospital_news.apps.HospitalNewsConfig',
    'hospital_contact.apps.HospitalContactConfig',
    'hospital_website.apps.HospitalWebsiteConfig',
    'hospital_doctor.apps.HospitalDoctorConfig',
    'hospital_panel.apps.HospitalPanelConfig',
    'hospital_units.apps.HospitalUnitsConfig',
    'hospital_ipd.apps.HospitalIpdConfig',

    # Packs
    'widget_tweaks',
    'captcha',
    'jalali_date',
    'ckeditor',
    'django_social_share',
    'django_cleanup.apps.CleanupConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',   # add for translating
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'app_config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [ Path('templates') ],
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

WSGI_APPLICATION = config('WSGI_APPLICATION')


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
LANGUAGES = [
    ('fa', _('Persian')),
    ('en', _('English')),
    ('ar', _('Arabic')),
    ('ru', _('Russia')),
]
LANGUAGE_CODE = config('LANGUAGE_CODE')
TIME_ZONE = config('TIME_ZONE')
USE_I18N = config('USE_I18N')
USE_TZ = config('USE_TZ')


STATIC_URL = '/site_static/'
STATIC_ROOT = Path("static_cdn", "static_root")
MEDIA_URL = '/media/'
MEDIA_ROOT = Path("static_cdn", "media_root")
STATICFILES_DIRS = [ Path("assets") ]

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# ## configs ## #

# user
AUTH_USER_MODEL = config('AUTH_USER_MODEL')
LOGIN_URL = reverse_lazy('auth:signin')

# captcha
CAPTCHA_FONT_SIZE = 30
CAPTCHA_BACKGROUND_COLOR = '#fff'
CAPTCHA_FOREGROUND_COLOR = '#4f98dc'
CAPTCHA_LENGTH = 1
CAPTCHA_IMAGE_SIZE = (100, 50)

# payment1
# payment2

# email
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'peakabot@gmail.com'
EMAIL_HOST_PASSWORD = '1190274442saeed'

# jalali date config
JALALI_DATE_DEFAULTS = {
   'Strftime': {
        'date': '%y/%m/%d',
        'datetime': '%H:%M:%S _ %y/%m/%d',
    },
    'Static': {
        'js': [
            'admin/js/django_jalali.min.js',
        ],
        'css': {
            'all': [
                'admin/jquery.ui.datepicker.jalali/themes/base/jquery-ui.min.css',
            ]
        }
    },
}

# ckeditor config
CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'Custom',
        'toolbar_Custom': [
            ['Bold', 'Italic', 'Underline'],
            ['NumberedList', 'BulletedList', '-', 'Outdent', 'Indent', '-', 'JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock'],
            ['Link', 'Unlink'],
            ['RemoveFormat']
        ]
    }
}