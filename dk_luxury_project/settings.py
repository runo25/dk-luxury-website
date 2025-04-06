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
    # In production, this MUST be set in the environment (e.g., WSGI file)
    # For local dev, it MUST be in .env
    raise ValueError("No SECRET_KEY set for Django application. Set it in your environment or .env file.")

# SECURITY WARNING: don't run with debug turned on in production!
# Defaults to False if not set. Converts string 'True' to boolean True.
DEBUG = os.getenv('DEBUG', 'False') == 'True'

# Get ALLOWED_HOSTS from environment as a comma-separated string, then split it.
# Defaults to empty list if not set. PythonAnywhere domain MUST be in the env var on PA.
allowed_hosts_str = os.getenv('ALLOWED_HOSTS', '')
ALLOWED_HOSTS = [host.strip() for host in allowed_hosts_str.split(',') if host.strip()]
# If running locally and DEBUG is True, add common local hosts automatically
if DEBUG and not ALLOWED_HOSTS:
    ALLOWED_HOSTS = ['127.0.0.1', 'localhost']


# Application definition
INSTALLED_APPS = [
    # My apps
    'services.apps.ServicesConfig', # Or just 'services'
    'contact.apps.ContactConfig',   # Or just 'contact'
    'pages.apps.PagesConfig',       # Or just 'pages'

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    # Add WhiteNoise middleware HERE, after SecurityMiddleware and before SessionMiddleware
    # if you decide to use WhiteNoise later for static files (good practice, but PA handles it too)
    # 'whitenoise.middleware.WhiteNoiseMiddleware',
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
        'DIRS': [BASE_DIR / 'templates'], # Using Pathlib
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
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases
# Keeping SQLite simple for now. For other DBs use dj-database-url and DATABASE_URL env var.
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [ # ... (keep your validators) ...
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images not uploaded by users)
# https://docs.djangoproject.com/en/5.1/howto/static-files/
STATIC_URL = '/static/'
# Directory where collectstatic gathers files for production
STATIC_ROOT = BASE_DIR / 'staticfiles'
# Directories where Django looks for static files initially
STATICFILES_DIRS = [ BASE_DIR / 'static' ]
# Optional: If using WhiteNoise for static file serving in production (besides Django dev server)
# STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


# Media files (User-uploaded content)
# https://docs.djangoproject.com/en/5.1/topics/files/
MEDIA_URL = '/media/'
# Directory where user uploads are stored on the filesystem
MEDIA_ROOT = BASE_DIR / 'mediafiles'


# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# Email Configuration using environment variables
# Defaults are provided for common scenarios but should be set in the environment for production
EMAIL_BACKEND = os.getenv('EMAIL_BACKEND', 'django.core.mail.backends.smtp.EmailBackend')
EMAIL_HOST = os.getenv('EMAIL_HOST', 'smtp.gmail.com')
EMAIL_PORT = int(os.getenv('EMAIL_PORT', 587)) # Convert port to integer
EMAIL_USE_TLS = os.getenv('EMAIL_USE_TLS', 'True') == 'True' # Convert to boolean
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER') # Must be set in environment
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD') # Must be set in environment

# Default email address to use for various automated correspondence (e.g., error reports)
# Uses the sending user by default, or specify another via DEFAULT_FROM_EMAIL env var
DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL', EMAIL_HOST_USER)

# Email address that receives contact form submissions
CONTACT_FORM_RECIPIENT_EMAIL = os.getenv('CONTACT_FORM_RECIPIENT_EMAIL') # Must be set in environment
if not CONTACT_FORM_RECIPIENT_EMAIL:
     # You might want to raise an error or log a warning if this is critical
     print("Warning: CONTACT_FORM_RECIPIENT_EMAIL environment variable is not set.")