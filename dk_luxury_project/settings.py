# settings.py
import os
import sys # Ensure sys is imported for the debug print
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
# Defaults to False if not set. Converts string 'True' to boolean True.
DEBUG = os.getenv('DEBUG', 'False') == 'True'

# Get ALLOWED_HOSTS from environment
allowed_hosts_str = os.getenv('ALLOWED_HOSTS', '')
ALLOWED_HOSTS = [host.strip() for host in allowed_hosts_str.split(',') if host.strip()]
# If running locally and DEBUG is True, add common local hosts automatically
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

    # Django Apps (Ensure all needed for admin are here)
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    # Ensure all needed for admin are present and in reasonable order
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware', # Required for admin login
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware', # Required for admin users
    'django.contrib.messages.middleware.MessageMiddleware', # Required for admin messages
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'dk_luxury_project.urls'

TEMPLATES = [
    {
        # Ensure this structure is correct for admin templates
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',     # Required for admin
                'django.contrib.messages.context_processors.messages', # Required for admin
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
AUTH_PASSWORD_VALIDATORS = [
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


# --- Static files (CSS, JavaScript, Images NOT uploaded by users) ---
# Configuration remains the same
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [ BASE_DIR / 'static' ]


# --- File Storage Configuration (DEFAULT for Media Files) ---
# -------------------------------------------------------------
# settings.py (Relevant R2/AWS Block)

DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
print(f"SETTINGS.PY: DEFAULT_FILE_STORAGE is set to '{DEFAULT_FILE_STORAGE}'", file=sys.stderr)

AWS_ACCESS_KEY_ID = os.getenv('CLOUDFLARE_R2_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('CLOUDFLARE_R2_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = os.getenv('CLOUDFLARE_R2_BUCKET_NAME')
CLOUDFLARE_ACCOUNT_ID = os.getenv('CLOUDFLARE_ACCOUNT_ID')

# --- Endpoint for API calls (still needed for uploads) ---
AWS_S3_ENDPOINT_URL = f'https://{CLOUDFLARE_ACCOUNT_ID}.r2.cloudflarestorage.com' if CLOUDFLARE_ACCOUNT_ID else None

# --- CHANGE THIS: Use the r2.dev public URL for generated links ---
# Replace the pub-... hex string with the one you were given
AWS_S3_CUSTOM_DOMAIN = 'pub-42a8d0ab2e1f4676b315f613aaea8a82.r2.dev'
# --- END CHANGE ---

AWS_LOCATION = '' # Keep this empty
AWS_S3_REGION_NAME = 'auto'
AWS_S3_SIGNATURE_VERSION = 's3v4'
AWS_DEFAULT_ACL = 'public-read' # Keep this - might still be needed for r2.dev access
AWS_S3_FILE_OVERWRITE = False
AWS_QUERYSTRING_AUTH = False # Keep this False

# --- MEDIA_URL and MEDIA_ROOT are not directly used by S3Boto3Storage ---
# They primarily affect the FileSystemStorage backend.
#  MEDIA_URL = '/media/'
# MEDIA_ROOT = BASE_DIR / 'mediafiles'

# -------------------------------------------------------------
# --- End File Storage Configuration ---


# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# Email Configuration using environment variables
# --- Configuration remains the same ---
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

# --- Optional: Logging Configuration ---
# (Add this if you want more detailed logs, especially for errors)
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'WARNING', # Change to INFO or DEBUG for more verbosity
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'INFO'),
            'propagate': False,
        },
        'storages': { # Add logging for django-storages if needed
            'handlers': ['console'],
            'level': 'DEBUG', # Set to DEBUG to see detailed storage operations
            'propagate': False,
        },
        'boto3': { # Add logging for boto3 if needed
            'handlers': ['console'],
            'level': 'INFO', # Set to DEBUG for very verbose S3 interaction logs
            'propagate': False,
        },
        'botocore': { # Add logging for botocore if needed
            'handlers': ['console'],
            'level': 'INFO', # Set to DEBUG for very verbose S3 interaction logs
            'propagate': False,
        },
    },
}