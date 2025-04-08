# settings.py
import os
from pathlib import Path
# Import dotenv - it won't cause errors if the module or .env file isn't present
try:
    from dotenv import load_dotenv
except ImportError:
    load_dotenv = None # Define a dummy function if dotenv is not installed

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Load .env file variables into environment (only does something if .env exists and dotenv is installed)
if load_dotenv:
    dotenv_path = BASE_DIR / '.env'
    if dotenv_path.exists():
        load_dotenv(dotenv_path=dotenv_path)

# --- READ FROM ENVIRONMENT VARIABLES ---

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY')
if not SECRET_KEY:
    raise ValueError("No SECRET_KEY set for Django application. Set it in your environment or .env file.")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('DEBUG', 'False') == 'True'

# Get ALLOWED_HOSTS from environment
allowed_hosts_str = os.getenv('ALLOWED_HOSTS', '')
ALLOWED_HOSTS = [host.strip() for host in allowed_hosts_str.split(',') if host.strip()]
if DEBUG and not ALLOWED_HOSTS:
    ALLOWED_HOSTS = ['127.0.0.1', 'localhost']


# Application definition
INSTALLED_APPS = [
    # My apps
    'services.apps.ServicesConfig',
    'contact.apps.ContactConfig',
    'pages.apps.PagesConfig',

    # External Apps
    'storages', # Add django-storages

    # Django Apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'dk_luxury_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'dk_luxury_project.wsgi.application'


# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
AUTH_PASSWORD_VALIDATORS = [ # ... (keep your validators) ...
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]


# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images NOT uploaded by users)
# Configuration remains the same for static files served by PA or WhiteNoise
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [ BASE_DIR / 'static' ]


# --- Media files Configuration for Cloudflare R2 ---
# ----------------------------------------------------

# Use django-storages S3 compatible backend for default file storage (media)
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage' # Correct backend path

# Define required AWS/S3 settings, reading values from environment variables
CLOUDFLARE_ACCOUNT_ID = os.getenv('CLOUDFLARE_ACCOUNT_ID')
AWS_ACCESS_KEY_ID = os.getenv('CLOUDFLARE_R2_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('CLOUDFLARE_R2_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = os.getenv('CLOUDFLARE_R2_BUCKET_NAME')

if not CLOUDFLARE_ACCOUNT_ID:
    print("Warning: CLOUDFLARE_ACCOUNT_ID environment variable not set. R2 endpoint cannot be constructed.")
AWS_S3_ENDPOINT_URL = f'https://{CLOUDFLARE_ACCOUNT_ID}.r2.cloudflarestorage.com' if CLOUDFLARE_ACCOUNT_ID else None

AWS_S3_REGION_NAME = 'auto' # R2 uses 'auto'
AWS_S3_SIGNATURE_VERSION = 's3v4' # Use signature version 4
AWS_DEFAULT_ACL = 'public-read' # Make files public by default (adjust if your bucket is private)
AWS_S3_FILE_OVERWRITE = False # Don't overwrite files with the same name by default
AWS_QUERYSTRING_AUTH = False # Don't add auth parameters to generated URLs (needed for public-read)
# Optional: Custom domain if you set one up in Cloudflare R2
AWS_S3_CUSTOM_DOMAIN = os.getenv('CLOUDFLARE_R2_CUSTOM_DOMAIN', None)

# --- OLD Media settings (Commented out or removed as they are handled by DEFAULT_FILE_STORAGE) ---
MEDIA_URL = '/media/' # This might still be useful depending on URL generation, but often the full R2 URL is used.
# MEDIA_ROOT = BASE_DIR / 'mediafiles' # Django no longer saves media files here directly.

# ----------------------------------------------------
# --- End Media Configuration ---


# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# Email Configuration using environment variables
EMAIL_BACKEND = os.getenv('EMAIL_BACKEND', 'django.core.mail.backends.smtp.EmailBackend')
EMAIL_HOST = os.getenv('EMAIL_HOST', 'smtp.gmail.com')
EMAIL_PORT = int(os.getenv('EMAIL_PORT', 587))
EMAIL_USE_TLS = os.getenv('EMAIL_USE_TLS', 'True') == 'True'
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL', EMAIL_HOST_USER)
CONTACT_FORM_RECIPIENT_EMAIL = os.getenv('CONTACT_FORM_RECIPIENT_EMAIL')
if not CONTACT_FORM_RECIPIENT_EMAIL:
     print("Warning: CONTACT_FORM_RECIPIENT_EMAIL environment variable is not set.")