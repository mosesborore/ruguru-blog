from pathlib import Path
import warnings
import os


import dj_database_url
from django.core.management.utils import get_random_secret_key


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


def get_list(text):
    return [item.strip() for item in text.split(",")]


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get("SECRET_KEY")

if not SECRET_KEY and DEBUG:
    warnings.warn("SECRET_KEY not configured, using a random temporary key.")
    SECRET_KEY = get_random_secret_key()

__DEFAULT_ALLOWED_HOSTS = "localhost,127.0.0.1"

ALLOWED_CLIENT_HOSTS = os.environ.get("ALLOWED_HOSTS")

if ALLOWED_CLIENT_HOSTS:
    ALLOWED_HOSTS = get_list(ALLOWED_CLIENT_HOSTS)
else:
    ALLOWED_HOSTS = get_list(__DEFAULT_ALLOWED_HOSTS)

AUTH_USER_MODEL = "accounts.Account"

# this to happen when the user tries to authenticate
AUTHENTICATION_BACKENDS = (
    "django.contrib.auth.backends.AllowAllUsersModelBackend",
    "accounts.backends.EmailBackend",
)

# Application definition

INSTALLED_APPS = [
    "blog.apps.BlogConfig",
    "accounts.apps.AccountsConfig",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "whitenoise.runserver_nostatic",
    "django.contrib.staticfiles",
    # 3rd party
    "crispy_forms",
    "widget_tweaks",
    "ckeditor",
    "ckeditor_uploader",
    'versatileimagefield',
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# session settings
CSRF_COOKIE_SECURE =True
SESSION_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = "strict"
SESSION_COOKIE_AGE = 640800

ROOT_URLCONF = "ruguru.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            BASE_DIR.joinpath("templates"),
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "ruguru.wsgi.application"


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases
DATABASES = {}
if os.environ.get("DATABASE_URL"):
    DATABASES["default"] = dj_database_url.config(
        default=os.environ.get("DATABASE_URL")
    )
else:
    DATABASES["default"] = {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": "ruguru_blog",
        "USER": "postgres",
        "PASSWORD": "1234",
        "HOST": "localhost",
        "PORT": "",
    }


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "Africa/Nairobi"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/
# STATIC_URL is the URL location of static files located in STATIC_ROOT
# STATICFILES_DIRS tells Django where to look for static files in a Django project, such as a top-level static folder
# STATIC_ROOT is the folder location of static files when collecstatic is run
# STATICFILES_STORAGE is the file storage engine used when collecting static files with the collecstatic command.

STATIC_URL = "/static/"
STATICFILES_DIRS = (str(BASE_DIR.joinpath("static")),)
STATIC_ROOT = str(BASE_DIR.joinpath("staticfiles"))
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"


# MEDIA
MEDIA_URL = "/media/"
MEDIA_ROOT = str(BASE_DIR.joinpath("media"))

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


LOGIN_URL = "accounts/login/?next=/accounts/profile"


# 3rd PARTY CONFIGURATION

# whitenoise
WHITENOISE_USE_FINDERS = True

# CRISPY-FORMS
CRISPY_TEMPLATE_PACK = "bootstrap4"


# ckeditor
CKEDITOR_CONFIGS = {
    "default": {
        "skin": "office2013",
        "toolbar": "full",
        "update": [
            "image",
            "update",
            "table",
            "horizontalRule",
            "Smiley",
            "SpecialChar",
        ],
        "tabspace": 4,
        "height": 500,
        "width": "100%",
        "filebrowserWindowHeight": 725,
        "filebrowserWindowWidth": 940,
        "toolbarCanCollapse": True,
        "extraPlugins": ",".join(
            [
                "uploadimage",  # the upload image feature
                # your extra plugins here
                "div",
                "autolink",
                "autoembed",
                "embedsemantic",
                "autogrow",
                # 'devtools',
                "widget",
                "lineutils",
                "clipboard",
                "dialog",
                "dialogui",
                "elementspath",
                "pastefromword",
            ]
        ),
    },
}

CKEDITOR_UPLOAD_PATH = "ckeditor/"
CKEDITOR_BROWSE_SHOW_DIRS = True


# VERSATILE SETTINGS
VERSATILEIMAGEFIELD_SETTINGS = {
    # images should be pre-generated
    "create_images_on_demand": False,
}

VERSATILEIMAGEFIELD_RENDITION_KEY_SETS = {
    "image_blog": [
        ("blog_large", 'thumbnail__1080x900'),
        ('hero', 'thumbnail__730x280'),
        ("blog_card", "thumbnail__1045x588"),
        ("blog_card_medium", "thumbnail__350x174"),
    ],
    "user_profile": [
        ('profile_large', 'thumbnail__300x300'),
        ('profile_medium', 'thumbnail__150x150'),
        ("profile_small", "thumbnail__50x50")
    ]
}
